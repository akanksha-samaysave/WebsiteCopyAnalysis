from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """Rules-based recommendation engine for landing page improvements."""

    @staticmethod
    def _safe_score(score: float, default: float = 5.0) -> float:
        try:
            if score is None:
                return default
            return float(score)
        except Exception:
            return default

    @staticmethod
    def _average(values: List[float]) -> float:
        if not values:
            return 5.0
        return sum(values) / len(values)

    @staticmethod
    def _cta_count(buttons: List[Dict]) -> int:
        if not buttons:
            return 0
        return sum(1 for btn in buttons if btn.get("text"))

    @classmethod
    def generate_recommendations(
        cls,
        copy_scores: Dict[str, float],
        ux_scores: Dict[str, float],
        trust_scores: Dict[str, float],
        sections: Dict,
        visible_text: str = "",
        headings: List[Dict] = None,
        buttons: List[Dict] = None,
        forms: List[Dict] = None,
    ) -> List[Dict[str, str]]:
        headings = headings or []
        buttons = buttons or []
        forms = forms or []
        sections = sections or {}

        recommendations: List[Dict[str, str]] = []

        try:
            def add(issue: str, recommendation: str, impact: str):
                if len(recommendations) >= 10:
                    return
                recommendations.append({
                    "issue": issue,
                    "recommendation": recommendation,
                    "impact": impact,
                })

            def trust_average() -> float:
                return cls._average([
                    cls._safe_score(trust_scores.get("social_proof")),
                    cls._safe_score(trust_scores.get("authority_signals")),
                    cls._safe_score(trust_scores.get("security_trust")),
                    cls._safe_score(trust_scores.get("credibility_signals")),
                ])

            def ux_average() -> float:
                return cls._average([
                    cls._safe_score(ux_scores.get("readability")),
                    cls._safe_score(ux_scores.get("visual_hierarchy")),
                    cls._safe_score(ux_scores.get("mobile_responsiveness")),
                    cls._safe_score(ux_scores.get("information_density")),
                    cls._safe_score(ux_scores.get("conversion_friction")),
                ])

            cta_strength = cls._safe_score(copy_scores.get("cta_strength"))
            headline_strength = cls._safe_score(copy_scores.get("headline_strength"))
            value_proposition = cls._safe_score(copy_scores.get("value_proposition"))
            emotional_triggers = cls._safe_score(copy_scores.get("emotional_triggers"))
            social_proof = cls._safe_score(trust_scores.get("social_proof"))
            credibility = cls._safe_score(trust_scores.get("credibility_signals"))
            authority = cls._safe_score(trust_scores.get("authority_signals"))
            mobile_responsiveness = cls._safe_score(ux_scores.get("mobile_responsiveness"))
            readability = cls._safe_score(ux_scores.get("readability"))
            information_density = cls._safe_score(ux_scores.get("information_density"))
            conversion_friction = cls._safe_score(ux_scores.get("conversion_friction"))
            total_sections = int(cls._safe_score(sections.get("total_sections", 0), 0))
            cta_count = cls._cta_count(buttons)
            form_fields = sum(len(form.get("fields", [])) for form in forms)

            if cta_strength < 6.0 or cta_count < 2:
                add(
                    "Weak or few CTA elements",
                    "Add stronger, action-oriented CTAs like 'Get Started' and place at least two prominent buttons above and below the fold.",
                    "High",
                )

            if trust_average() < 6.0:
                add(
                    "Low trust signals",
                    "Add testimonials, customer logos, user counts, reviews, and social proof to build credibility.",
                    "High",
                )

            if ux_average() < 6.0:
                add(
                    "UI/UX feels cluttered or hard to scan",
                    "Reduce text density, increase whitespace, and break content into shorter sections with subheadings and bullets.",
                    "High",
                )

            if value_proposition < 6.0:
                add(
                    "Unclear value proposition",
                    "Rewrite the hero message to state what you do, who you help, and the main benefit in one sentence.",
                    "High",
                )

            if headline_strength < 6.0:
                add(
                    "Headline is not compelling enough",
                    "Make the primary headline more specific by adding a key result, time frame, or measurable benefit.",
                    "Medium",
                )

            if readability < 6.0:
                add(
                    "Page content is hard to read",
                    "Shorten paragraphs, use more headings, and add bullet lists for key benefits and steps.",
                    "Medium",
                )

            if information_density > 7.0:
                add(
                    "Information overload",
                    "Lower text density by removing repetition and using clear section headings for each user need.",
                    "Medium",
                )

            if sections and total_sections < 6:
                add(
                    "Missing key page sections",
                    "Add or expand sections for problem, solution, benefits, testimonials, FAQ, and pricing or next steps.",
                    "Medium",
                )

            if social_proof < 6.0:
                add(
                    "Lack of visible social proof",
                    "Show real customer quotes, star ratings, or 'trusted by' logos to reassure new visitors.",
                    "Medium",
                )

            if credibility < 5.0:
                add(
                    "Low credibility or risk reversal",
                    "Offer a money-back guarantee, free trial, or satisfaction promise to reduce purchase anxiety.",
                    "Medium",
                )

            if authority < 5.0:
                add(
                    "Insufficient authority signals",
                    "Highlight experience, certifications, awards, or press mentions to establish expertise.",
                    "Low",
                )

            if mobile_responsiveness < 6.0:
                add(
                    "Mobile experience may be weak",
                    "Ensure the page uses a responsive layout, mobile-friendly buttons, and readable text sizes on phones.",
                    "Medium",
                )

            if conversion_friction < 6.0 and form_fields > 3:
                add(
                    "High conversion friction",
                    "Simplify forms by asking only for essential information and offer alternative contact options.",
                    "Medium",
                )

            if emotional_triggers < 5.0:
                add(
                    "Low emotional engagement",
                    "Add language that speaks to customer pain points, desires, and urgency to make the page more persuasive.",
                    "Low",
                )

            if len(recommendations) < 5:
                required = [
                    {
                        "issue": "Improve first impression",
                        "recommendation": "Make the hero section immediately clear with a strong headline, short supporting copy, and a clear CTA.",
                        "impact": "High",
                    },
                    {
                        "issue": "Add trust signals",
                        "recommendation": "Display customer proof points or badges near the top of the page to increase credibility.",
                        "impact": "Medium",
                    },
                    {
                        "issue": "Improve navigation of content",
                        "recommendation": "Use section headings and spacing to make the page easier to scan for visitors.",
                        "impact": "Medium",
                    },
                    {
                        "issue": "Clarify next step",
                        "recommendation": "Make the next action clear with a simple CTA and expected outcome.",
                        "impact": "Medium",
                    },
                    {
                        "issue": "Review page length",
                        "recommendation": "Keep supporting content concise and focused on the main benefit and conversion path.",
                        "impact": "Low",
                    },
                ]
                for item in required:
                    if len(recommendations) >= 5:
                        break
                    if item["issue"] not in [r["issue"] for r in recommendations]:
                        recommendations.append(item)

            return recommendations[:10]

        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return [
                {
                    "issue": "Unable to generate recommendations",
                    "recommendation": "Review the analysis inputs and try again.",
                    "impact": "Low",
                }
            ]
