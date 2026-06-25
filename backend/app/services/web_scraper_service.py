"""
web_scraper_service.py  –  production-ready Playwright scraper
=================================================================
Fixes applied:
  FIX-A  wait_until="networkidle" timed out on JS-heavy pages.
          Strategy: try "domcontentloaded" first (fast), then fall back
          to "load" if content is missing, never rely on "networkidle".
  FIX-B  No retry logic – added 3 attempts with back-off.
  FIX-C  Missing stealth headers – many sites (vikramanand.in, etc.)
          block headless Chromium; we now set a real User-Agent and
          extra headers so the page renders properly.
  FIX-D  Browser was never explicitly closed on error paths – fixed.
  FIX-E  screenshot stored as hex string was enormous; now stored as
          base64 which is ~33% smaller and directly usable in <img src>.
"""

import asyncio
import base64
import logging
from typing import Dict, Optional

from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeout,
    Error as PlaywrightError,
)

logger = logging.getLogger(__name__)

# Realistic desktop UA so anti-bot middleware lets us through
_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

_EXTRA_HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
}

# How long (ms) to wait for navigation
_NAV_TIMEOUT = 45_000
# Extra settle time (seconds) after navigation for JS to paint
_SETTLE_SECS = 2
# Number of scrape attempts before giving up
_MAX_RETRIES = 3


class WebScraperService:
    """Playwright-based scraper.  Single public method: scrape_page(url)."""

    @staticmethod
    async def scrape_page(url: str) -> Dict:
        """
        Scrape *url* and return a structured dict.

        Always returns a dict; on failure ``status`` is ``"error"``
        and ``error`` contains the exception message.
        """
        last_error: Optional[Exception] = None

        for attempt in range(1, _MAX_RETRIES + 1):
            browser = None
            try:
                async with async_playwright() as pw:
                    # FIX-C: launch with stealth args
                    browser = await pw.chromium.launch(
                        headless=True,
                        args=[
                            "--no-sandbox",
                            "--disable-setuid-sandbox",
                            "--disable-blink-features=AutomationControlled",
                            "--disable-dev-shm-usage",
                        ],
                    )
                    ctx = await browser.new_context(
                        user_agent=_USER_AGENT,
                        extra_http_headers=_EXTRA_HEADERS,
                        viewport={"width": 1280, "height": 800},
                        java_script_enabled=True,
                    )
                    page = await ctx.new_page()

                    # Hide webdriver flag (basic stealth)
                    await page.add_init_script(
                        "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
                    )

                    # FIX-A: use domcontentloaded (never hangs), then settle
                    try:
                        await page.goto(
                            url,
                            wait_until="domcontentloaded",
                            timeout=_NAV_TIMEOUT,
                        )
                    except PlaywrightTimeout:
                        # Page is really slow — try with "load" as last resort
                        await page.goto(
                            url,
                            wait_until="load",
                            timeout=_NAV_TIMEOUT,
                        )

                    # Let JS frameworks render their content
                    await asyncio.sleep(_SETTLE_SECS)

                    # ── content extraction ──────────────────────────────
                    raw_html = await page.content()

                    visible_text: str = await page.evaluate(
                        "() => document.body ? document.body.innerText : ''"
                    ) or ""

                    buttons = await page.evaluate("""
                        () => Array.from(document.querySelectorAll(
                            'button, a[role="button"], input[type="button"], input[type="submit"]'
                        )).map(el => ({
                            text: (el.textContent || el.value || '').trim(),
                            class: el.className || '',
                            id: el.id || ''
                        })).filter(b => b.text.length > 0).slice(0, 30)
                    """) or []

                    forms = await page.evaluate("""
                        () => Array.from(document.querySelectorAll('form')).map(f => ({
                            id: f.id || '',
                            fields: Array.from(f.querySelectorAll('input,textarea,select')).map(el => ({
                                type: el.type || el.tagName.toLowerCase(),
                                name: el.name || '',
                                placeholder: el.placeholder || ''
                            }))
                        })).slice(0, 10)
                    """) or []

                    headings = await page.evaluate("""
                        () => Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6'))
                            .map((el, idx) => ({
                                level: el.tagName,
                                text: (el.textContent || '').trim(),
                                order: idx
                            }))
                            .filter(h => h.text.length > 0)
                            .slice(0, 30)
                    """) or []

                    meta_info = await page.evaluate("""
                        () => ({
                            title: document.title || '',
                            description: (document.querySelector('meta[name="description"]') || {}).content || '',
                            keywords:    (document.querySelector('meta[name="keywords"]')    || {}).content || '',
                            viewport:    (document.querySelector('meta[name="viewport"]')    || {}).content || '',
                            ogImage:     (document.querySelector('meta[property="og:image"]')|| {}).content || ''
                        })
                    """) or {}

                    # FIX-E: store screenshot as base64
                    screenshot_bytes = await page.screenshot(
                        full_page=True, type="png"
                    )
                    screenshot_b64 = (
                        base64.b64encode(screenshot_bytes).decode()
                        if screenshot_bytes
                        else None
                    )

                    await browser.close()
                    browser = None

                    logger.info("Scraped %s successfully (attempt %d)", url, attempt)
                    return {
                        "url": url,
                        "status": "success",
                        "raw_html": raw_html,
                        "visible_text": visible_text,
                        "buttons": buttons,
                        "forms": forms,
                        "headings": headings,
                        "meta_info": meta_info,
                        "screenshot": screenshot_b64,
                        "error": None,
                    }

            except (PlaywrightTimeout, PlaywrightError, Exception) as exc:
                last_error = exc
                logger.warning(
                    "Attempt %d/%d failed for %s: %s",
                    attempt, _MAX_RETRIES, url, exc,
                )
                if browser:
                    try:
                        await browser.close()
                    except Exception:
                        pass
                    browser = None
                if attempt < _MAX_RETRIES:
                    await asyncio.sleep(attempt * 2)  # back-off: 2s, 4s

        # All retries exhausted
        error_msg = str(last_error) if last_error else "Unknown scrape error"
        logger.error("Failed to scrape %s after %d attempts: %s", url, _MAX_RETRIES, error_msg)
        return {
            "url": url,
            "status": "error",
            "raw_html": None,
            "visible_text": None,
            "buttons": [],
            "forms": [],
            "headings": [],
            "meta_info": {},
            "screenshot": None,
            "error": error_msg,
        }