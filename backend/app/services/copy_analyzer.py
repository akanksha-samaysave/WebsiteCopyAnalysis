import logging
import re
from typing import Dict, List

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from app.utils.helpers import clean_text, normalize_text

logger = logging.getLogger(__name__)


class CopyAnalyzer:
    """Deterministic copywriting analysis engine using TextBlob and VADER."""

    ACTION_WORDS = [
        "get", "start", "join", "discover", "learn", "try", "explore", "create",
        "build", "launch", "transform", "revolutionize", "unlock", "access",
        "claim", "sign", "grab", "buy", "order", "download", "subscribe"
    ]

    PAIN_WORDS = [
        "struggle", "pain", "frustrated", "failed", "failure", "tired", "problem",
        "issue", "challenge", "lost", "stuck", "overwhelmed", "frustration"
    ]

    DESIRE_WORDS = [
        "achieve", "success", "dream", "vision", "growth", "wealth", "happiness",
        "freedom", "better", "win", "improve", "gain", "maximize", "power"
    ]

    URGENCY_WORDS = [
        "now", "today", "urgent", "limited", "exclusive", "hurry", "soon",
        "before", "last chance", "act now", "don\'t miss", "ends soon"
    ]

    VALUE_WORDS = [
        "save", "reduce", "increase", "improve", "simplify", "streamline", "boost",
        "accelerate", "optimize", "protect", "secure", "grow", "gain"
    ]

    FEATURE_WORDS = [
        "feature", "capability", "tool", "platform", "system", "dashboard", "integration",
        "module", "functionality", "app", "software", "supports"
    ]

    BUTTON_KEYWORDS = [
        "sign up", "get started", "try now", "join", "start free", "book demo",
        "request demo", "buy now", "download", "learn more", "subscribe", "claim"
    ]

    analyzer = SentimentIntensityAnalyzer()

    @staticmethod
    def headline_quality(headings: List[Dict[str, str]]) -> float:
        if not headings:
            return 0.0

        headline = normalize_text(headings[0].get("text", ""))
        if not headline:
            return 0.0

        score = 0.0
        max_score = 10.0

        words = headline.split()
        word_count = len(words)

        # Clarity: direct language and short enough
        if 5 <= word_count <= 15:
            score += 3.0
        elif 3 <= word_count <= 20:
            score += 2.0

        # Specificity: numeric or concrete benefit
        if re.search(r"\d+", headline) or any(word in headline for word in ["save", "reduce", "increase", "grow", "boost"]):
            score += 2.0

        # Outcome orientation: benefit oriented language
        if any(word in headline for word in ["results", "better", "faster", "more", "improve", "boost"]):
            score += 2.0

        # Sentiment positivity suggests strong headline
        try:
            blob = TextBlob(headline)
            if blob.sentiment.polarity > 0.05:
                score += 1.5
        except Exception as exc:
            logger.warning("Headline sentiment failed: %s", exc)

        # Add a small bonus if there is a clear action or benefit word
        if any(word in headline for word in CopyAnalyzer.ACTION_WORDS + CopyAnalyzer.VALUE_WORDS):
            score += 1.5

        return min((score / max_score) * 10.0, 10.0)

    @staticmethod
    def emotional_triggers(text: str) -> float:
        text = normalize_text(text)
        if not text:
            return 0.0

        score = 0.0
        found = set()

        for word in CopyAnalyzer.PAIN_WORDS:
            if word in text:
                score += 1.0
                found.add("pain")
        for word in CopyAnalyzer.DESIRE_WORDS:
            if word in text:
                score += 1.0
                found.add("desire")
        for word in CopyAnalyzer.URGENCY_WORDS:
            if word in text:
                score += 1.5
                found.add("urgency")

        # VADER sentiment adjustment
        try:
            vader_scores = CopyAnalyzer.analyzer.polarity_scores(text)
            score += max(0.0, vader_scores["pos"] * 2.0)
            score += max(0.0, vader_scores["compound"] * 1.5)
        except Exception as exc:
            logger.warning("VADER sentiment failed: %s", exc)

        return min(score, 10.0)

    @staticmethod
    def value_proposition(text: str, headings: List[Dict[str, str]]) -> float:
        text_content = normalize_text(text)
        heading_text = " ".join([normalize_text(h.get("text", "")) for h in headings[:3]])

        score = 0.0

        if any(word in heading_text for word in CopyAnalyzer.VALUE_WORDS):
            score += 3.0
        if any(word in text_content for word in CopyAnalyzer.VALUE_WORDS):
            score += 3.0

        if any(word in heading_text for word in ["easy", "simple", "fast", "secure", "trusted"]):
            score += 2.0

        if len(heading_text) > 30:
            score += 1.0

        return min(score, 10.0)

    @staticmethod
    def features_vs_benefits(text: str) -> float:
        text = normalize_text(text)
        if not text:
            return 5.0

        benefit_count = sum(text.count(word) for word in CopyAnalyzer.VALUE_WORDS)
        feature_count = sum(text.count(word) for word in CopyAnalyzer.FEATURE_WORDS)

        if benefit_count + feature_count == 0:
            return 5.0

        ratio = benefit_count / (benefit_count + feature_count)
        score = ratio * 10.0
        return min(score, 10.0)

    @staticmethod
    def cta_strength(buttons: List[Dict[str, str]], text: str) -> float:
        if not buttons:
            return 0.0

        score = 0.0
        cta_count = 0
        text_lower = normalize_text(text)

        for button in buttons:
            btn_text = normalize_text(button.get("text", ""))
            if not btn_text:
                continue
            if any(keyword in btn_text for keyword in CopyAnalyzer.BUTTON_KEYWORDS):
                cta_count += 1
                if any(action in btn_text for action in CopyAnalyzer.ACTION_WORDS):
                    score += 2.0
                if any(urgency in btn_text for urgency in CopyAnalyzer.URGENCY_WORDS):
                    score += 1.5

        if cta_count >= 3:
            score += 3.0
        elif cta_count == 2:
            score += 2.0
        elif cta_count == 1:
            score += 1.0

        # Count all CTA-like verbs in page text to improve visibility score
        visibility_score = sum(text_lower.count(word) for word in CopyAnalyzer.ACTION_WORDS)
        score += min(visibility_score, 3.0)

        return min(score, 10.0)

    @staticmethod
    def analyze_all(headings: List[Dict[str, str]], text: str, buttons: List[Dict[str, str]]) -> Dict[str, float]:
        headline = CopyAnalyzer.headline_quality(headings)
        emotion = CopyAnalyzer.emotional_triggers(text)
        cta = CopyAnalyzer.cta_strength(buttons, text)
        value = CopyAnalyzer.value_proposition(text, headings)
        ratio = CopyAnalyzer.features_vs_benefits(text)

        overall = round((headline * 0.25 + emotion * 0.20 + value * 0.20 + ratio * 0.15 + cta * 0.20), 1)

        return {
            "headline_score": round(headline, 1),
            "emotion_score": round(emotion, 1),
            "value_prop_score": round(value, 1),
            "features_vs_benefits_score": round(ratio, 1),
            "cta_score": round(cta, 1),
            "overall": overall,
        }
