from typing import Dict
import re
import logging

logger = logging.getLogger(__name__)


class UXAnalyzerService:
    """Service to analyze UX principles and conversion friction."""

    @staticmethod
    def analyze_readability(visible_text: str, headings: list) -> float:
        """
        Score readability (0-10).
        
        Criteria:
        - Text length per section (should be scannable)
        - Heading structure
        - Paragraph length
        - Line breaks/spacing
        """
        if not visible_text or not headings:
            return 0.0
        
        try:
            score = 0.0
            
            # Good structure: more headings = better scanability
            heading_ratio = len(headings) / max(1, len(visible_text.split()) / 100)
            
            if heading_ratio > 0.5:
                score += 3.0
            elif heading_ratio > 0.3:
                score += 2.0
            else:
                score += 1.0
            
            # Check paragraph length
            paragraphs = [p.strip() for p in visible_text.split("\n") if p.strip()]
            avg_para_length = sum(len(p.split()) for p in paragraphs) / len(paragraphs) if paragraphs else 0
            
            if 50 < avg_para_length < 150:
                score += 2.5  # Ideal
            elif 30 < avg_para_length < 200:
                score += 1.5
            else:
                score += 0.5
            
            # Text exists and is substantial
            if len(visible_text) > 1000:
                score += 2.0
            elif len(visible_text) > 500:
                score += 1.0
            
            # Heading hierarchy
            if len(headings) >= 3:
                score += 1.5
            
            return min(score, 10.0)
            
        except Exception as e:
            logger.error(f"Error analyzing readability: {str(e)}")
            return 5.0

    @staticmethod
    def analyze_visual_hierarchy(headings: list, buttons: list) -> float:
        """
        Score visual hierarchy (0-10).
        
        Criteria:
        - Clear heading structure (H1 -> H2 -> H3)
        - CTA prominence
        - Information organization
        """
        if not headings:
            return 0.0
        
        try:
            score = 0.0
            
            # Check heading hierarchy
            heading_levels = [h["level"] for h in headings]
            
            if "H1" in heading_levels:
                score += 2.0
            if "H2" in heading_levels:
                score += 2.0
            if "H3" in heading_levels:
                score += 1.5
            
            # Variety in heading levels (good structure)
            unique_levels = len(set(heading_levels))
            if unique_levels >= 2:
                score += 2.0
            
            # Clear section separation (multiple H2s indicate sections)
            h2_count = heading_levels.count("H2")
            if h2_count >= 3:
                score += 2.0
            elif h2_count >= 1:
                score += 1.0
            
            # CTA prominence (should have buttons)
            if buttons:
                score += 1.5
            
            return min(score, 10.0)
            
        except Exception as e:
            logger.error(f"Error analyzing visual hierarchy: {str(e)}")
            return 5.0

    @staticmethod
    def analyze_mobile_responsiveness(meta_info: dict) -> float:
        """
        Score mobile responsiveness signals (0-10).
        
        Checks for viewport meta tag and responsive design indicators.
        """
        try:
            score = 0.0
            
            # Viewport meta tag presence
            if meta_info.get("viewport"):
                score += 3.0
                # Check for mobile-friendly viewport settings
                viewport = meta_info.get("viewport", "").lower()
                if "width=device-width" in viewport:
                    score += 2.0
                if "initial-scale" in viewport:
                    score += 1.0
            
            # OG image tag (suggests responsive design consideration)
            if meta_info.get("ogImage"):
                score += 2.0
            
            # Keywords and description tags suggest SEO/mobile awareness
            if meta_info.get("keywords"):
                score += 1.0
            if meta_info.get("description"):
                score += 1.0
            
            return min(score, 10.0)
            
        except Exception as e:
            logger.error(f"Error analyzing mobile responsiveness: {str(e)}")
            return 5.0

    @staticmethod
    def analyze_information_density(visible_text: str) -> float:
        """
        Score information density (0-10).
        
        Checks if content is well-distributed (not too much, not too little).
        """
        if not visible_text:
            return 0.0
        
        try:
            text_length = len(visible_text)
            word_count = len(visible_text.split())
            
            # Ideal landing page: 500-5000 words
            if 800 <= text_length <= 4000:
                score = 8.0
            elif 500 <= text_length <= 5000:
                score = 6.0
            elif text_length > 5000:
                score = 4.0  # Too dense
            else:
                score = 3.0  # Too sparse
            
            # Lines (paragraphs)
            paragraphs = [p for p in visible_text.split("\n") if p.strip()]
            if 5 <= len(paragraphs) <= 20:
                score += 2.0
            
            return min(score, 10.0)
            
        except Exception as e:
            logger.error(f"Error analyzing information density: {str(e)}")
            return 5.0

    @staticmethod
    def analyze_conversion_friction(forms: list, buttons: list) -> float:
        """
        Score conversion friction (0-10). Higher = less friction.
        
        Criteria:
        - Form field count (fewer is better)
        - CTA clarity
        - Multiple conversion paths
        """
        try:
            score = 10.0
            
            # Check form complexity
            total_fields = 0
            for form in forms:
                fields = form.get("fields", [])
                total_fields += len(fields)
            
            # Penalize for too many form fields
            if total_fields > 10:
                score -= 4.0
            elif total_fields > 5:
                score -= 2.0
            elif total_fields > 3:
                score -= 1.0
            
            # Reward for multiple CTAs (multiple paths)
            if len(buttons) >= 3:
                score += 1.0
            
            # Reward for clear button text
            cta_count = 0
            for btn in buttons:
                text_lower = btn.get("text", "").lower()
                if any(word in text_lower for word in ["get", "start", "sign", "join", "try", "contact"]):
                    cta_count += 1
            
            if cta_count >= 2:
                score += 2.0
            
            return max(min(score, 10.0), 0.0)
            
        except Exception as e:
            logger.error(f"Error analyzing conversion friction: {str(e)}")
            return 5.0

    @staticmethod
    def analyze_all(visible_text: str, headings: list, buttons: list,
                   forms: list, meta_info: dict) -> Dict[str, float]:
        """
        Perform complete UX analysis.
        
        Returns:
            Dict with scores for all UX metrics
        """
        return {
            "readability": UXAnalyzerService.analyze_readability(visible_text, headings),
            "visual_hierarchy": UXAnalyzerService.analyze_visual_hierarchy(headings, buttons),
            "mobile_responsiveness": UXAnalyzerService.analyze_mobile_responsiveness(meta_info),
            "information_density": UXAnalyzerService.analyze_information_density(visible_text),
            "conversion_friction": UXAnalyzerService.analyze_conversion_friction(forms, buttons)
        }
