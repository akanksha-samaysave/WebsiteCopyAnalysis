import logging
import re
from typing import Dict, List

logger = logging.getLogger(__name__)


class SectionDetector:
    """Deterministic section detection engine based on text, HTML, and headings."""

    SECTION_PATTERNS = {
        "hero": [
            r"\b(hero|banner|welcome|hero section|above the fold|landing page)\b",
            r"<header[^>]*>",
            r"class=[\"'].*?(hero|banner).*?[\"']",
        ],
        "problem": [
            r"\b(problem|challenge|pain|issue|struggle|frustration|difficulty)s?\b",
            r"\b(are you tired|do you struggle|having trouble)\b",
        ],
        "solution": [
            r"\b(solution|solve|how it works|our approach|we help|we solve)\b",
            r"\b(get started with|introduced|presenting|delivers)\b",
        ],
        "benefits": [
            r"\b(benefits|advantages|reasons to choose|results|outcomes|gains|value)\b",
            r"\b(you will|you can|helps you|lets you)\b",
        ],
        "features": [
            r"\b(features|capabilities|includes|what you get|powered by|built for)\b",
            r"\b(available features|key features|product features)\b",
        ],
        "testimonials": [
            r"\b(testimonials|reviews|case studies|success stories|customer stories|client stories|customer feedback|what our customers say)\b",
            r"\b(quote|said|rated|★★★★★|5-star)\b",
        ],
        "pricing": [
            r"\b(pricing|price|plans|packages|cost|subscription|monthly|annual|free trial)\b",
            r"\b(starting at|from \$|per month|per year|billing)\b",
        ],
        "faq": [
            r"\b(faq|frequently asked questions|frequently asked|questions and answers|q&a|common questions)\b",
            r"\b(how do i|what is the|why should i|where can i)\b",
        ],
        "cta": [
            r"\b(get started|sign up|start free|try now|book demo|request demo|buy now|download now|learn more|contact us|schedule a demo)\b",
            r"<button[^>]*>(.*?)</button>",
        ],
    }

    @staticmethod
    def detect_sections(text: str, html: str, headings: List[Dict[str, str]]) -> Dict[str, bool]:
        """Detect page sections using keywords, regex, and heading analysis."""
        try:
            normalized_text = text.lower() if text else ""
            normalized_html = html.lower() if html else ""
            heading_text = " ".join(
                [str(item.get("text", "")).lower() for item in headings if item.get("text")]
            )

            detected: Dict[str, bool] = {
                "hero": False,
                "problem": False,
                "solution": False,
                "benefits": False,
                "features": False,
                "testimonials": False,
                "pricing": False,
                "faq": False,
                "cta": False,
            }

            def matches_any(patterns: List[str], source: str) -> bool:
                return any(re.search(pattern, source, flags=re.IGNORECASE) for pattern in patterns)

            # Heading analysis helps detect section presence.
            for section, patterns in SectionDetector.SECTION_PATTERNS.items():
                if matches_any(patterns, heading_text):
                    detected[section] = True

            # Text and HTML detection for each section.
            for section, patterns in SectionDetector.SECTION_PATTERNS.items():
                if not detected[section]:
                    if matches_any(patterns, normalized_text) or matches_any(patterns, normalized_html):
                        detected[section] = True

            # Special heuristics for hero and cta.
            if not detected["hero"]:
                if headings and any(re.search(r"\b(h1|h2|hero|welcome|landing)\b", h.get("text", "").lower()) for h in headings):
                    detected["hero"] = True
                elif re.search(r"class=[\"'].*?(hero|banner|masthead|hero-section).*?[\"']", normalized_html):
                    detected["hero"] = True

            if not detected["cta"]:
                if re.search(r"<a[^>]+(href|role)=['\"]?(.*?sign[- ]?up|.*?start[- ]?free|.*?try[- ]?now|.*?book[- ]?demo|.*?buy[- ]?now)['\"]?", normalized_html):
                    detected["cta"] = True
                elif re.search(r"<button[^>]*>.*?(sign up|get started|try now|book demo|learn more|download now|request demo).*?</button>", normalized_html, flags=re.IGNORECASE | re.DOTALL):
                    detected["cta"] = True

            return detected

        except Exception as exc:
            logger.error("Section detection failed: %s", str(exc))
            return {
                "hero": False,
                "problem": False,
                "solution": False,
                "benefits": False,
                "features": False,
                "testimonials": False,
                "pricing": False,
                "faq": False,
                "cta": False,
            }
