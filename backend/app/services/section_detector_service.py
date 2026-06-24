from typing import Dict, List
import re
import logging

logger = logging.getLogger(__name__)


class SectionDetectorService:
    """Service to detect and label page sections."""

    SECTION_KEYWORDS = {
        "hero": ["hero", "banner", "header", "welcome", "introduction"],
        "problem": ["problem", "challenge", "pain", "issues", "struggle"],
        "solution": ["solution", "how it works", "features", "benefits", "service"],
        "benefits": ["benefits", "why", "advantages", "results", "outcomes"],
        "features": ["features", "capabilities", "includes", "tools", "platform"],
        "testimonials": ["testimonials", "reviews", "case study", "success story", "customer feedback"],
        "pricing": ["pricing", "plans", "price", "packages", "costs", "billing"],
        "faq": ["faq", "frequently asked", "questions", "support", "help"],
        "cta": ["get started", "sign up", "join", "start free", "try now", "contact us", "demo"]
    }

    @staticmethod
    def detect_sections(headings: List[Dict], visible_text: str) -> Dict:
        """
        Detect sections based on headings and content.
        
        Args:
            headings: List of heading elements
            visible_text: Full visible text from page
            
        Returns:
            Dict with detected sections
        """
        detected_sections = {
            "hero": False,
            "problem": False,
            "solution": False,
            "benefits": False,
            "features": False,
            "testimonials": False,
            "pricing": False,
            "faq": False,
            "cta": False
        }
        
        try:
            # Check headings
            heading_text = " ".join([h["text"].lower() for h in headings])
            
            for section, keywords in SectionDetectorService.SECTION_KEYWORDS.items():
                for keyword in keywords:
                    if keyword.lower() in heading_text:
                        detected_sections[section] = True
                        break
            
            # Check visible text for sections
            text_lower = visible_text.lower()
            
            # Enhanced section detection
            if len(headings) > 0:
                detected_sections["hero"] = True  # Most pages have hero
            
            if "problem" in text_lower or "challenge" in text_lower or "pain" in text_lower:
                detected_sections["problem"] = True
            
            if "solution" in text_lower or "how it works" in text_lower:
                detected_sections["solution"] = True
            
            if "testimonial" in text_lower or "review" in text_lower or "quote" in text_lower:
                detected_sections["testimonials"] = True
            
            if "pricing" in text_lower or "plan" in text_lower or "package" in text_lower:
                detected_sections["pricing"] = True
            
            if "faq" in text_lower or "frequently asked" in text_lower:
                detected_sections["faq"] = True
            
            if "get started" in text_lower or "sign up" in text_lower or "try now" in text_lower:
                detected_sections["cta"] = True
            
            return {
                "detected_sections": detected_sections,
                "total_sections": sum(detected_sections.values()),
                "section_count": len(headings)
            }
            
        except Exception as e:
            logger.error(f"Error detecting sections: {str(e)}")
            return {
                "detected_sections": detected_sections,
                "total_sections": 0,
                "section_count": 0
            }
