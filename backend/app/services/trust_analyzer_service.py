from typing import Dict
import re
import logging

logger = logging.getLogger(__name__)


class TrustAnalyzerService:
    """Service to analyze trust and credibility signals."""

    TRUST_KEYWORDS = {
        "social_proof": ["customer", "client", "user", "rating", "review", "testimonial",
                        "trust", "trusted", "award", "certified", "verified", "approved"],
        "authority": ["expert", "specialist", "leader", "authority", "industry", "years",
                     "experience", "founded", "established", "company"],
        "security": ["secure", "encrypted", "ssl", "privacy", "gdpr", "confidential",
                    "protected", "safe", "security", "safe"],
        "credibility": ["guarantee", "warranty", "money-back", "satisfaction",
                       "no risk", "refund", "promise"]
    }

    @staticmethod
    def detect_social_proof(visible_text: str, headings: list) -> float:
        """
        Score social proof signals (0-10).
        
        Detects testimonials, reviews, ratings, and social proof.
        """
        if not visible_text:
            return 0.0
        
        try:
            score = 0.0
            text_lower = visible_text.lower()
            
            # Check for testimonial section
            if "testimonial" in text_lower or "case study" in text_lower:
                score += 3.0
            
            # Check for review mentions
            review_count = text_lower.count("review") + text_lower.count("rating")
            if review_count >= 3:
                score += 2.0
            elif review_count >= 1:
                score += 1.0
            
            # Check for customer count/stats
            customer_patterns = [
                r'\d+\s*(?:customers|users|clients)',
                r'\d+\s*(?:happy|satisfied|successful)',
            ]
            
            for pattern in customer_patterns:
                if re.search(pattern, text_lower):
                    score += 1.5
                    break
            
            # Check for specific quote marks (indicates testimonials)
            if '"' in visible_text or '"' in visible_text or '„' in visible_text:
                score += 1.5
            
            # Logos/company mentions
            if "logo" in text_lower or "partner" in text_lower or "client" in text_lower:
                score += 1.0
            
            return min(score, 10.0)
            
        except Exception as e:
            logger.error(f"Error detecting social proof: {str(e)}")
            return 0.0

    @staticmethod
    def detect_authority_signals(visible_text: str, headings: list, meta_info: dict) -> float:
        """
        Score authority and credibility (0-10).
        
        Detects expertise, industry leadership, experience, certifications.
        """
        if not visible_text:
            return 0.0
        
        try:
            score = 0.0
            text_lower = visible_text.lower()
            
            # Check for years of experience
            experience_pattern = r'\d+\s*years?\s*(?:of\s*)?(?:experience|industry|business)'
            if re.search(experience_pattern, text_lower):
                score += 2.0
            
            # Check for expertise/expert signals
            if "expert" in text_lower or "specialist" in text_lower:
                score += 1.5
            
            # Industry/leadership signals
            if "leader" in text_lower or "leading" in text_lower or "industry" in text_lower:
                score += 1.5
            
            # Founded/established
            if "founded" in text_lower or "established" in text_lower:
                score += 1.0
            
            # Certifications or awards
            if "certified" in text_lower or "award" in text_lower or "certification" in text_lower:
                score += 1.5
            
            # Team/founder info
            if "team" in text_lower or "founder" in text_lower or "ceo" in text_lower:
                score += 1.0
            
            # Company info in description/title
            if meta_info.get("description"):
                desc_lower = meta_info.get("description", "").lower()
                if any(word in desc_lower for word in ["professional", "trusted", "leading", "expert"]):
                    score += 1.0
            
            return min(score, 10.0)
            
        except Exception as e:
            logger.error(f"Error detecting authority signals: {str(e)}")
            return 0.0

    @staticmethod
    def detect_security_trust(visible_text: str, forms: list) -> float:
        """
        Score security and trust signals (0-10).
        
        Detects encryption mentions, privacy policies, security badges.
        """
        if not visible_text:
            return 0.0
        
        try:
            score = 0.0
            text_lower = visible_text.lower()
            
            # Security mentions
            if "secure" in text_lower or "encrypted" in text_lower or "ssl" in text_lower:
                score += 2.0
            
            # Privacy/GDPR
            if "privacy" in text_lower or "gdpr" in text_lower:
                score += 2.0
            
            # Data protection
            if "data protection" in text_lower or "confidential" in text_lower:
                score += 1.5
            
            # Safety mentions
            if "safe" in text_lower or "safety" in text_lower:
                score += 1.0
            
            # If forms present with security signals = good
            if forms and (score > 0):
                score += 1.0
            
            return min(score, 10.0)
            
        except Exception as e:
            logger.error(f"Error detecting security trust: {str(e)}")
            return 0.0

    @staticmethod
    def detect_credibility_signals(visible_text: str) -> float:
        """
        Score credibility guarantees (0-10).
        
        Detects money-back guarantees, warranties, risk-free trials.
        """
        if not visible_text:
            return 0.0
        
        try:
            score = 0.0
            text_lower = visible_text.lower()
            
            # Money-back guarantee
            if "money-back" in text_lower or "money back" in text_lower:
                score += 3.0
            elif "guarantee" in text_lower:
                score += 2.0
            
            # Risk-free trials/offers
            if "risk-free" in text_lower or "no risk" in text_lower or "free trial" in text_lower:
                score += 2.5
            
            # Satisfaction guarantee
            if "satisfaction" in text_lower or "satisfied" in text_lower:
                score += 1.5
            
            # Refund policy
            if "refund" in text_lower:
                score += 1.5
            
            # Promise/commitment
            if "promise" in text_lower or "committed" in text_lower:
                score += 1.0
            
            return min(score, 10.0)
            
        except Exception as e:
            logger.error(f"Error detecting credibility signals: {str(e)}")
            return 0.0

    @staticmethod
    def analyze_all(visible_text: str, headings: list, forms: list,
                   meta_info: dict) -> Dict[str, float]:
        """
        Perform complete trust analysis.
        
        Returns:
            Dict with scores for all trust metrics
        """
        return {
            "social_proof": TrustAnalyzerService.detect_social_proof(visible_text, headings),
            "authority_signals": TrustAnalyzerService.detect_authority_signals(visible_text, headings, meta_info),
            "security_trust": TrustAnalyzerService.detect_security_trust(visible_text, forms),
            "credibility_signals": TrustAnalyzerService.detect_credibility_signals(visible_text)
        }
