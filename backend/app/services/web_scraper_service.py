import asyncio
from playwright.async_api import async_playwright
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class WebScraperService:
    """Service to scrape and extract content from landing pages using Playwright."""

    @staticmethod
    async def scrape_page(url: str) -> Dict:
        """
        Scrape a landing page and extract content.
        
        Args:
            url: The URL to scrape
            
        Returns:
            Dict containing raw_html, visible_text, buttons, forms, headings, sections
        """
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # Navigate to URL
                await page.goto(url, wait_until="networkidle", timeout=30000)
                
                # Wait for content to render
                await asyncio.sleep(2)
                
                # Extract raw HTML
                raw_html = await page.content()
                
                # Extract visible text
                visible_text = await page.evaluate("""
                    () => {
                        return document.body.innerText || '';
                    }
                """)
                
                # Extract buttons
                buttons = await page.evaluate("""
                    () => {
                        return Array.from(document.querySelectorAll('button, a[role="button"], input[type="button"], input[type="submit"]'))
                            .map(el => ({
                                text: el.textContent?.trim() || el.value || '',
                                class: el.className || '',
                                id: el.id || ''
                            }))
                            .filter(btn => btn.text.length > 0)
                            .slice(0, 20);
                    }
                """)
                
                # Extract forms
                forms = await page.evaluate("""
                    () => {
                        return Array.from(document.querySelectorAll('form'))
                            .map(form => ({
                                id: form.id || '',
                                fields: Array.from(form.querySelectorAll('input, textarea, select'))
                                    .map(field => ({
                                        type: field.type || field.tagName,
                                        name: field.name || '',
                                        placeholder: field.placeholder || ''
                                    }))
                            }))
                            .slice(0, 10);
                    }
                """)
                
                # Extract headings
                headings = await page.evaluate("""
                    () => {
                        return Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'))
                            .map((el, idx) => ({
                                level: el.tagName,
                                text: el.textContent?.trim() || '',
                                order: idx
                            }))
                            .filter(h => h.text.length > 0)
                            .slice(0, 30);
                    }
                """)
                
                # Extract meta information
                meta_info = await page.evaluate("""
                    () => {
                        return {
                            title: document.title || '',
                            description: document.querySelector('meta[name="description"]')?.content || '',
                            keywords: document.querySelector('meta[name="keywords"]')?.content || '',
                            viewport: document.querySelector('meta[name="viewport"]')?.content || '',
                            ogImage: document.querySelector('meta[property="og:image"]')?.content || ''
                        };
                    }
                """)
                
                # Take screenshot
                screenshot_data = await page.screenshot(full_page=True, type="png")
                
                await browser.close()
                
                return {
                    "url": url,
                    "status": "success",
                    "raw_html": raw_html,
                    "visible_text": visible_text,
                    "buttons": buttons,
                    "forms": forms,
                    "headings": headings,
                    "meta_info": meta_info,
                    "screenshot": screenshot_data.hex() if screenshot_data else None
                }
                
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return {
                "url": url,
                "status": "error",
                "error": str(e),
                "raw_html": None,
                "visible_text": None,
                "buttons": [],
                "forms": [],
                "headings": [],
                "meta_info": {},
                "screenshot": None
            }
