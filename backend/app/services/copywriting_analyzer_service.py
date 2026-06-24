from typing import Dict, Tuple
import re
import logging
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

logger = logging.getLogger(__name__)
analyzer = SentimentIntensityAnalyzer()


class CopywritingAnalyzerService:
    """Service to analyze copywriting quality and psychology."""

    EMOTIONAL_TRIGGERS = {
        "pain": ["struggle", "pain", "frustrated", "fail", "broke", "lost", "stuck", "overwhelmed"],
        "desire": ["achieve", "success", "dream", "vision", "growth", "wealth", "happiness", "freedom"],
        "urgency": ["now", "limited", "exclusive", "today", "hurry", "soon", "before", "last chance", "urgent", "act now"]
    }

    ACTION_WORDS = [
        "get", "start", "join", "discover", "learn", "try", "explore", "create",
        "build", "launch", "transform", "revolutionize", "unlock", "access",
        "claim", "sign", "grab", "buy", "order", "download", "subscribe"
    ]

    @staticmethod
    def analyze_headline(headings: list) -> float:
        """
        Score headline strength (0-10).
        
        Criteria:
        - Clarity: Is it clear what the product does?
        - Specificity: Does it mention specific benefits?
        - Emotional hooks: Does it trigger emotion?
        """
        if not headings:
            return 0.0
        
        try:
            main_headline = headings[0]["text"] if headings else ""
            
            if not main_headline:
                return 0.0
            
            score = 0.0
            max_score = 10.0
            
            # Length check (3-15 words is ideal)
            word_count = len(main_headline.split())
            if 3 <= word_count <= 15:
                score += 2.0
            elif 2 <= word_count <= 20:
                score += 1.0
            
            # Check for numbers/specificity
            if re.search(r'\d+', main_headline):
                score += 2.0
            
            # Check for power words
            text_lower = main_headline.lower()
            for word in CopywritingAnalyzerService.ACTION_WORDS:
                if word in text_lower:
                    score += 1.0
                    break
            
            # Sentiment analysis
            blob = TextBlob(main_headline)
            sentiment = blob.polarity
            if sentiment > 0.1:  # Positive
                score += 2.0
            
            # Length bonus for longer headlines
            if len(main_headline) > 30:
                score += 1.0
            
            return min(score / max_score * 10, 10.0)
            
        except Exception as e:
            logger.error(f"Error analyzing headline: {str(e)}")
            return 5.0

    @staticmethod
    def analyze_emotional_triggers(visible_text: str) -> float:
        """
        Score emotional triggers (0-10).
        
        Checks for pain, desire, and urgency triggers.
        """
        if not visible_text:
            return 0.0
        
        try:
            text_lower = visible_text.lower()
            score = 0.0
            trigger_count = 0
            
            for trigger_type, triggers in CopywritingAnalyzerService.EMOTIONAL_TRIGGERS.items():
                for trigger in triggers:
                    if trigger in text_lower:
                        trigger_count += 1
                        if trigger_type == "pain":
                            score += 1.5
                        elif trigger_type == "desire":
                            score += 1.5
                        elif trigger_type == "urgency":
                            score += 2.0
            
            # Cap the score
            return min(score, 10.0)
            
        except Exception as e:
            logger.error(f"Error analyzing emotional triggers: {str(e)}")
            return 5.0

    @staticmethod
    def analyze_value_proposition(visible_text: str, headings: list) -> float:
        """
        Score value proposition clarity (0-10).
        
        Checks if the core value is clear within first few headings.
        """
        if not headings:
            return 0.0
        
        try:
            first_headings = " ".join([h["text"] for h in headings[:3]]).lower()
            
            score = 0.0
            
            # Check for clear value indicators
            if "transform" in first_headings or "revolutionize" in first_headings:
                score += 3.0
            if "save" in first_headings or "reduce" in first_headings:
                score += 2.0
            if "increase" in first_headings or "grow" in first_headings:
                score += 2.0
            if "easy" in first_headings or "simple" in first_headings or "fast" in first_headings:
                score += 1.5
            
            # Check visible text
            text_lower = visible_text.lower()
            if first_headings and len(visible_text) > 500:
                # Text exists, value must be there
                score += 1.5
            
            return min(score, 10.0)
            
        except Exception as e:
            logger.error(f"Error analyzing value proposition: {str(e)}")
            return 5.0

    @staticmethod
    def analyze_features_vs_benefits(visible_text: str) -> float:
        """
        Score benefits focus vs features focus (0-10).
        
        Better pages focus on benefits (how it helps) vs features (what it does).
        """
        if not visible_text:
            return 0.0
        
        try:
            text_lower = visible_text.lower()
            
            # Benefit keywords (outcomes/results)
            benefit_words = ["achieve", "get", "save", "reduce", "increase", "transform",
                           "improve", "success", "results", "outcome", "benefit", "advantage"]
            
            # Feature keywords (capabilities)
            feature_words = ["includes", "has", "features", "capability", "tool",
                           "platform", "system", "software", "app", "solution"]
            
            benefit_count = sum(1 for word in benefit_words if word in text_lower)
            feature_count = sum(1 for word in feature_words if word in text_lower)
            
            if benefit_count + feature_count == 0:
                return 5.0
            
            benefit_ratio = benefit_count / (benefit_count + feature_count)
            
            # More benefits is better (target 70%+ benefits)
            score = benefit_ratio * 10
            
            return min(score, 10.0)
            
        except Exception as e:
            logger.error(f"Error analyzing features vs benefits: {str(e)}")
            return 5.0

    @staticmethod
    def analyze_cta_strength(buttons: list, visible_text: str) -> float:
        """
        Score CTA strength (0-10).
        
        Criteria:
        - Action words
        - Visibility (size, position)
        - Frequency
        - Clear value proposition
        """
        if not buttons:
            return 0.0
        
        try:
            score = 0.0
            cta_buttons = []
            
            # Find CTA buttons
            cta_keywords = ["sign up", "get started", "try", "join", "start", "buy",
                          "order", "subscribe", "contact", "demo", "claim"]
            
            for button in buttons:
                text_lower = button.get("text", "").lower()
                if any(keyword in text_lower for keyword in cta_keywords):
                    cta_buttons.append(button)
            
            # Check if CTAs exist
            if not cta_buttons:
                return 2.0  # Weak - no clear CTAs
            
            # Score based on number of CTAs
            cta_count = len(cta_buttons)
            if cta_count >= 3:
                score += 3.0  # Good visibility
            elif cta_count >= 1:
                score += 1.5
            
            # Check CTA text quality
            for cta in cta_buttons:
                text_lower = cta.get("text", "").lower().strip()
                if len(text_lower) > 20:
                    continue  # Too long
                if any(word in text_lower for word in CopywritingAnalyzerService.ACTION_WORDS):
                    score += 2.0
                    break
            
            # Check for urgency in CTA
            if any("now" in btn.get("text", "").lower() or "limited" in btn.get("text", "").lower() 
                   for btn in cta_buttons):
                score += 2.0
            
            return min(score, 10.0)
            
        except Exception as e:
            logger.error(f"Error analyzing CTA strength: {str(e)}")
            return 5.0

    @staticmethod
    def analyze_all(headings: list, visible_text: str, buttons: list) -> Dict[str, float]:
        """
        Perform complete copywriting analysis.
        
        Returns:
            Dict with scores for all copywriting metrics
        """
        return {
            "headline_strength": CopywritingAnalyzerService.analyze_headline(headings),
            "emotional_triggers": CopywritingAnalyzerService.analyze_emotional_triggers(visible_text),
            "value_proposition": CopywritingAnalyzerService.analyze_value_proposition(visible_text, headings),
            "features_vs_benefits": CopywritingAnalyzerService.analyze_features_vs_benefits(visible_text),
            "cta_strength": CopywritingAnalyzerService.analyze_cta_strength(buttons, visible_text)
        }
