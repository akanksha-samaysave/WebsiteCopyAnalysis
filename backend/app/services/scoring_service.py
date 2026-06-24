from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class ScoringService:
    """Service to calculate weighted scores and overall ratings."""

    # Weights for each category (must sum to 1.0)
    CATEGORY_WEIGHTS = {
        "design": 0.15,
        "messaging": 0.25,
        "trust": 0.20,
        "clarity": 0.15,
        "conversion": 0.15,
        "ux": 0.10
    }

    @staticmethod
    def calculate_design_score(ux_scores: Dict[str, float]) -> float:
        """
        Calculate design score (0-10).
        
        Based on visual hierarchy and mobile responsiveness.
        """
        try:
            design_metrics = [
                ux_scores.get("visual_hierarchy", 5.0) * 0.5,
                ux_scores.get("mobile_responsiveness", 5.0) * 0.5
            ]
            return sum(design_metrics) / len(design_metrics)
        except Exception as e:
            logger.error(f"Error calculating design score: {str(e)}")
            return 5.0

    @staticmethod
    def calculate_messaging_score(copy_scores: Dict[str, float]) -> float:
        """
        Calculate messaging score (0-10).
        
        Weighted average of copywriting metrics.
        """
        try:
            messaging_metrics = [
                copy_scores.get("headline_strength", 5.0) * 0.25,
                copy_scores.get("value_proposition", 5.0) * 0.35,
                copy_scores.get("features_vs_benefits", 5.0) * 0.25,
                copy_scores.get("cta_strength", 5.0) * 0.15
            ]
            return sum(messaging_metrics) / len(messaging_metrics)
        except Exception as e:
            logger.error(f"Error calculating messaging score: {str(e)}")
            return 5.0

    @staticmethod
    def calculate_trust_score(trust_scores: Dict[str, float]) -> float:
        """
        Calculate trust score (0-10).
        
        Weighted average of trust metrics.
        """
        try:
            trust_metrics = [
                trust_scores.get("social_proof", 5.0) * 0.3,
                trust_scores.get("authority_signals", 5.0) * 0.3,
                trust_scores.get("security_trust", 5.0) * 0.2,
                trust_scores.get("credibility_signals", 5.0) * 0.2
            ]
            return sum(trust_metrics) / len(trust_metrics)
        except Exception as e:
            logger.error(f"Error calculating trust score: {str(e)}")
            return 5.0

    @staticmethod
    def calculate_clarity_score(ux_scores: Dict[str, float], copy_scores: Dict[str, float]) -> float:
        """
        Calculate clarity score (0-10).
        
        Based on readability and information density.
        """
        try:
            clarity_metrics = [
                ux_scores.get("readability", 5.0) * 0.4,
                ux_scores.get("information_density", 5.0) * 0.4,
                copy_scores.get("value_proposition", 5.0) * 0.2
            ]
            return sum(clarity_metrics) / len(clarity_metrics)
        except Exception as e:
            logger.error(f"Error calculating clarity score: {str(e)}")
            return 5.0

    @staticmethod
    def calculate_conversion_score(copy_scores: Dict[str, float],
                                  ux_scores: Dict[str, float],
                                  sections: Dict) -> float:
        """
        Calculate conversion score (0-10).
        
        Based on CTA strength, conversion friction, and emotional triggers.
        """
        try:
            conversion_metrics = [
                copy_scores.get("cta_strength", 5.0) * 0.4,
                ux_scores.get("conversion_friction", 5.0) * 0.3,
                copy_scores.get("emotional_triggers", 5.0) * 0.2,
                5.0 * (sections.get("total_sections", 0) / 9) * 0.1  # Bonus for complete sections
            ]
            score = sum(conversion_metrics) / len(conversion_metrics)
            return min(score, 10.0)
        except Exception as e:
            logger.error(f"Error calculating conversion score: {str(e)}")
            return 5.0

    @staticmethod
    def calculate_ux_score(ux_scores: Dict[str, float]) -> float:
        """
        Calculate UX score (0-10).
        
        Average of all UX metrics.
        """
        try:
            ux_metrics = list(ux_scores.values())
            if not ux_metrics:
                return 5.0
            return sum(ux_metrics) / len(ux_metrics)
        except Exception as e:
            logger.error(f"Error calculating UX score: {str(e)}")
            return 5.0

    @staticmethod
    def calculate_overall_score(category_scores: Dict[str, float]) -> float:
        """
        Calculate weighted overall score (0-100).
        
        Applies weights to each category.
        """
        try:
            weighted_sum = 0.0
            for category, weight in ScoringService.CATEGORY_WEIGHTS.items():
                score = category_scores.get(category, 5.0)
                weighted_sum += score * weight
            
            return round(min(weighted_sum, 10.0) * 10, 1)  # Scale to 0-100
        except Exception as e:
            logger.error(f"Error calculating overall score: {str(e)}")
            return 50.0

    @staticmethod
    def calculate_all_scores(copy_scores: Dict[str, float],
                            ux_scores: Dict[str, float],
                            trust_scores: Dict[str, float],
                            sections: Dict) -> Tuple[Dict[str, float], float]:
        """
        Calculate all category scores and overall score.
        
        Returns:
            Tuple of (category_scores, overall_score)
        """
        try:
            category_scores = {
                "design": ScoringService.calculate_design_score(ux_scores),
                "messaging": ScoringService.calculate_messaging_score(copy_scores),
                "trust": ScoringService.calculate_trust_score(trust_scores),
                "clarity": ScoringService.calculate_clarity_score(ux_scores, copy_scores),
                "conversion": ScoringService.calculate_conversion_score(copy_scores, ux_scores, sections),
                "ux": ScoringService.calculate_ux_score(ux_scores)
            }
            
            overall_score = ScoringService.calculate_overall_score(category_scores)
            
            return category_scores, overall_score
            
        except Exception as e:
            logger.error(f"Error calculating all scores: {str(e)}")
            return {cat: 5.0 for cat in ["design", "messaging", "trust", "clarity", "conversion", "ux"]}, 50.0
