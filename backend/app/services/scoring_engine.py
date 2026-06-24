from typing import Dict
import logging

logger = logging.getLogger(__name__)


class ScoringEngine:
    """Engine to combine analysis outputs into final landing page scores."""

    CATEGORY_WEIGHTS = {
        "design": 0.15,
        "messaging": 0.25,
        "trust": 0.20,
        "clarity": 0.15,
        "conversion": 0.15,
        "ux": 0.10,
    }

    @staticmethod
    def _safe_score(value: float, default: float = 5.0) -> float:
        try:
            if value is None:
                return default
            return float(value)
        except Exception:
            return default

    @staticmethod
    def _average(values: list) -> float:
        if not values:
            return 5.0
        return sum(values) / len(values)

    @classmethod
    def calculate_design(cls, ux_scores: Dict[str, float]) -> float:
        try:
            visual = cls._safe_score(ux_scores.get("visual_hierarchy", 5.0))
            mobile = cls._safe_score(ux_scores.get("mobile_responsiveness", 5.0))
            return round(cls._average([visual, mobile]), 1)
        except Exception as e:
            logger.error(f"Error calculating design score: {e}")
            return 5.0

    @classmethod
    def calculate_messaging(cls, copy_scores: Dict[str, float]) -> float:
        try:
            headline = cls._safe_score(copy_scores.get("headline_strength", 5.0))
            value = cls._safe_score(copy_scores.get("value_proposition", 5.0))
            features = cls._safe_score(copy_scores.get("features_vs_benefits", 5.0))
            cta = cls._safe_score(copy_scores.get("cta_strength", 5.0))
            emotional = cls._safe_score(copy_scores.get("emotional_triggers", 5.0))
            weights = [0.25, 0.30, 0.20, 0.15, 0.10]
            weighted = [headline * weights[0], value * weights[1], features * weights[2], cta * weights[3], emotional * weights[4]]
            return round(sum(weighted) / sum(weights), 1)
        except Exception as e:
            logger.error(f"Error calculating messaging score: {e}")
            return 5.0

    @classmethod
    def calculate_trust(cls, trust_scores: Dict[str, float]) -> float:
        try:
            return round(cls._average([
                cls._safe_score(trust_scores.get("social_proof", 5.0)),
                cls._safe_score(trust_scores.get("authority_signals", 5.0)),
                cls._safe_score(trust_scores.get("security_trust", 5.0)),
                cls._safe_score(trust_scores.get("credibility_signals", 5.0)),
            ]), 1)
        except Exception as e:
            logger.error(f"Error calculating trust score: {e}")
            return 5.0

    @classmethod
    def calculate_clarity(cls, ux_scores: Dict[str, float], copy_scores: Dict[str, float]) -> float:
        try:
            readability = cls._safe_score(ux_scores.get("readability", 5.0))
            density = cls._safe_score(ux_scores.get("information_density", 5.0))
            proposition = cls._safe_score(copy_scores.get("value_proposition", 5.0))
            weights = [0.4, 0.4, 0.2]
            weighted = [readability * weights[0], density * weights[1], proposition * weights[2]]
            return round(sum(weighted) / sum(weights), 1)
        except Exception as e:
            logger.error(f"Error calculating clarity score: {e}")
            return 5.0

    @classmethod
    def calculate_conversion(cls, copy_scores: Dict[str, float], ux_scores: Dict[str, float], sections: Dict) -> float:
        try:
            cta = cls._safe_score(copy_scores.get("cta_strength", 5.0))
            friction = cls._safe_score(ux_scores.get("conversion_friction", 5.0))
            emotional = cls._safe_score(copy_scores.get("emotional_triggers", 5.0))
            section_bonus = 0.0
            if sections and isinstance(sections, dict):
                total = cls._safe_score(sections.get("total_sections", 0), 0.0)
                section_bonus = min(total / 9.0, 1.0) * 2.0
            weights = [0.4, 0.35, 0.15, 0.10]
            weighted = [cta * weights[0], friction * weights[1], emotional * weights[2], section_bonus * weights[3]]
            raw = sum(weighted) / sum(weights)
            return round(min(raw, 10.0), 1)
        except Exception as e:
            logger.error(f"Error calculating conversion score: {e}")
            return 5.0

    @classmethod
    def calculate_ux(cls, ux_scores: Dict[str, float]) -> float:
        try:
            values = [cls._safe_score(v, 5.0) for v in ux_scores.values()]
            return round(cls._average(values), 1)
        except Exception as e:
            logger.error(f"Error calculating UX score: {e}")
            return 5.0

    @classmethod
    def calculate_overall(cls, category_scores: Dict[str, float]) -> float:
        try:
            total = 0.0
            for category, weight in cls.CATEGORY_WEIGHTS.items():
                total += cls._safe_score(category_scores.get(category, 5.0)) * weight
            return round(min(total, 10.0), 1)
        except Exception as e:
            logger.error(f"Error calculating overall score: {e}")
            return 5.0

    @classmethod
    def calculate_final_scores(cls, copy_scores: Dict[str, float], ux_scores: Dict[str, float], trust_scores: Dict[str, float], sections: Dict) -> Dict[str, float]:
        design = cls.calculate_design(ux_scores)
        messaging = cls.calculate_messaging(copy_scores)
        trust = cls.calculate_trust(trust_scores)
        clarity = cls.calculate_clarity(ux_scores, copy_scores)
        conversion = cls.calculate_conversion(copy_scores, ux_scores, sections)
        ux = cls.calculate_ux(ux_scores)
        overall = cls.calculate_overall({
            "design": design,
            "messaging": messaging,
            "trust": trust,
            "clarity": clarity,
            "conversion": conversion,
            "ux": ux,
        })

        return {
            "design": design,
            "messaging": messaging,
            "trust": trust,
            "ux": ux,
            "clarity": clarity,
            "conversion": conversion,
            "overall": overall,
        }
