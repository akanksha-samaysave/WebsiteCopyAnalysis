from typing import Dict
import logging

logger = logging.getLogger(__name__)


class UXAnalyzerService:
    """Service to analyze UX principles and conversion friction."""

    @staticmethod
    def analyze_readability(visible_text: str, headings: list) -> float:
        if not visible_text or not headings:
            return 0.0

        score = 0.0
        word_count = len(visible_text.split())
        paragraphs = [p.strip() for p in visible_text.split("\n") if p.strip()]
        avg_para_words = sum(len(p.split()) for p in paragraphs) / len(paragraphs) if paragraphs else 0

        heading_density = len(headings) / max(1.0, word_count / 120.0)
        if heading_density >= 0.5:
            score += 3.0
        elif heading_density >= 0.25:
            score += 2.0
        else:
            score += 1.0

        if 40 <= avg_para_words <= 120:
            score += 3.0
        elif 20 <= avg_para_words <= 150:
            score += 2.0
        else:
            score += 1.0

        if word_count >= 800:
            score += 2.0
        elif word_count >= 350:
            score += 1.0

        if len(headings) >= 3:
            score += 1.5

        return min(score, 10.0)

    @staticmethod
    def analyze_visual_hierarchy(headings: list, buttons: list) -> float:
        if not headings:
            return 0.0

        score = 0.0
        levels = [h.get("level", "H2").upper() for h in headings if isinstance(h, dict)]

        if "H1" in levels:
            score += 2.0
        if "H2" in levels:
            score += 2.0
        if "H3" in levels:
            score += 1.0

        unique_levels = len(set(levels))
        if unique_levels >= 3:
            score += 2.5
        elif unique_levels == 2:
            score += 1.5

        h2_count = levels.count("H2")
        if h2_count >= 3:
            score += 1.5
        elif h2_count >= 1:
            score += 0.75

        if buttons:
            score += 1.0
            prominent_ctas = sum(1 for btn in buttons if btn.get("text") and len(btn["text"]) > 5)
            if prominent_ctas >= 1:
                score += 0.5

        return min(score, 10.0)

    @staticmethod
    def analyze_mobile_responsiveness(meta_info: dict) -> float:
        score = 0.0
        viewport = meta_info.get("viewport", "").lower() if meta_info else ""

        if viewport:
            score += 3.0
            if "width=device-width" in viewport:
                score += 2.0
            if "initial-scale" in viewport or "maximum-scale" in viewport:
                score += 1.0

        if meta_info.get("description"):
            score += 1.0
        if meta_info.get("keywords"):
            score += 0.5
        if meta_info.get("ogImage") or meta_info.get("og:image"):
            score += 1.5

        return min(score, 10.0)

    @staticmethod
    def analyze_information_density(visible_text: str) -> float:
        if not visible_text:
            return 0.0

        score = 0.0
        word_count = len(visible_text.split())
        paragraphs = [p for p in visible_text.split("\n") if p.strip()]

        if 700 <= word_count <= 3500:
            score += 5.0
        elif 400 <= word_count <= 5000:
            score += 3.5
        elif word_count > 5000:
            score += 2.0
        else:
            score += 1.5

        if 5 <= len(paragraphs) <= 18:
            score += 2.5
        elif len(paragraphs) <= 25:
            score += 1.5

        return min(score, 10.0)

    @staticmethod
    def analyze_conversion_friction(forms: list, buttons: list) -> float:
        score = 8.0

        total_fields = 0
        if forms:
            for form in forms:
                total_fields += len(form.get("fields", []))

        if total_fields > 10:
            score -= 4.0
        elif total_fields > 6:
            score -= 2.5
        elif total_fields > 3:
            score -= 1.0

        cta_texts = [btn.get("text", "").lower() for btn in buttons if btn.get("text")]
        clear_ctas = sum(1 for text in cta_texts if any(word in text for word in ["get", "start", "sign", "join", "try", "contact", "book"]))
        if clear_ctas >= 2:
            score += 1.5
        elif clear_ctas == 1:
            score += 0.75

        if len(buttons) >= 3:
            score += 1.0

        return max(min(score, 10.0), 0.0)

    @staticmethod
    def analyze_all(visible_text: str, headings: list, buttons: list, forms: list, meta_info: dict) -> Dict[str, float]:
        return {
            "readability": UXAnalyzerService.analyze_readability(visible_text, headings),
            "visual_hierarchy": UXAnalyzerService.analyze_visual_hierarchy(headings, buttons),
            "mobile_responsiveness": UXAnalyzerService.analyze_mobile_responsiveness(meta_info),
            "information_density": UXAnalyzerService.analyze_information_density(visible_text),
            "conversion_friction": UXAnalyzerService.analyze_conversion_friction(forms, buttons),
        }
