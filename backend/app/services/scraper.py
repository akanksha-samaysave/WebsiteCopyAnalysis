import asyncio
import logging
import re
from typing import Dict, List, Optional

from playwright.async_api import async_playwright, Error as PlaywrightError, TimeoutError as PlaywrightTimeoutError

from app.utils.helpers import clean_html, normalize_text

logger = logging.getLogger(__name__)


class ScraperService:
    """Playwright-based scraper service for loading full JS pages."""

    DEFAULT_TIMEOUT = 30000
    DEFAULT_RETRIES = 2

    @staticmethod
    async def scrape_page(
        url: str,
        timeout: int = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
    ) -> Dict[str, Optional[str]]:
        """Scrape a page with Playwright and return structured content."""
        attempt = 0
        last_error: Optional[Exception] = None

        while attempt <= retries:
            try:
                async with async_playwright() as playwright:
                    browser = await playwright.chromium.launch(
                        headless=True,
                        args=["--no-sandbox", "--disable-setuid-sandbox"],
                    )
                    page = await browser.new_page()
                    page.set_default_navigation_timeout(timeout)
                    page.set_default_timeout(timeout)

                    await page.goto(url, wait_until="networkidle")
                    await page.wait_for_load_state("networkidle")
                    await asyncio.sleep(1)

                    html = await page.content()
                    text = await page.evaluate("() => document.body.innerText || ''")

                    buttons = await page.evaluate(
                        """
                        () => Array.from(document.querySelectorAll('button, a[role="button"], input[type="button"], input[type="submit"], input[type="reset"]'))
                            .map(el => ({
                                text: el.textContent?.trim() || el.value || '',
                                type: el.tagName,
                                id: el.id || '',
                                classes: el.className || ''
                            }))
                            .filter(btn => btn.text.length > 0)
                            .slice(0, 50)
                        """
                    )

                    headings = await page.evaluate(
                        """
                        () => Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'))
                            .map((el, index) => ({
                                level: el.tagName.toLowerCase(),
                                text: el.textContent?.trim() || '',
                                order: index
                            }))
                            .filter(heading => heading.text.length > 0)
                            .slice(0, 30)
                        """
                    )

                    forms = await page.evaluate(
                        """
                        () => Array.from(document.querySelectorAll('form')).map(form => ({
                            id: form.id || '',
                            action: form.action || '',
                            method: form.method || 'get',
                            fields: Array.from(form.querySelectorAll('input, textarea, select')).map(field => ({
                                type: field.type || field.tagName.toLowerCase(),
                                name: field.name || '',
                                placeholder: field.placeholder || '',
                                value: field.value || '',
                                required: field.required || false
                            }))
                        })).slice(0, 20)
                        """
                    )

                    screenshot_bytes = await page.screenshot(full_page=True, type="png")
                    await browser.close()

                    return {
                        "url": url,
                        "html": clean_html(html),
                        "text": normalize_text(text),
                        "buttons": buttons,
                        "headings": headings,
                        "forms": forms,
                        "screenshots": screenshot_bytes.hex() if screenshot_bytes else None,
                    }

            except (PlaywrightTimeoutError, PlaywrightError, Exception) as exc:
                last_error = exc
                logger.warning(
                    "Attempt %s/%s failed for %s: %s",
                    attempt + 1,
                    retries + 1,
                    url,
                    str(exc),
                )
                attempt += 1
                if attempt > retries:
                    break
                await asyncio.sleep(1)

        logger.error("Failed to scrape %s after %s attempts: %s", url, retries + 1, str(last_error))
        return {
            "url": url,
            "html": None,
            "text": None,
            "buttons": [],
            "headings": [],
            "forms": [],
            "screenshots": None,
            "error": str(last_error) if last_error else "unknown error",
        }
