from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class RecommendationService:
    """Service to generate actionable CRO recommendations."""

    @staticmethod
    def generate_recommendations(copy_scores: Dict[str, float],
                               ux_scores: Dict[str, float],
                               trust_scores: Dict[str, float],
                               sections: Dict,
                               visible_text: str,
                               headings: list,
                               buttons: list,
                               forms: list) -> List[Dict[str, str]]:
        """
        Generate at least 5 actionable CRO recommendations.
        
        Returns:
            List of recommendations with priority, title, description, reasoning, category
        """
        recommendations = []
        
        try:
            # Copywriting recommendations
            if copy_scores.get("headline_strength", 5.0) < 6.0:
                recommendations.append({
                    "priority": "High",
                    "title": "Strengthen Primary Headline",
                    "description": "Rewrite your main headline to include a specific number, outcome, or benefit. Add emotional triggers or power words.",
                    "reasoning": f"Headline strength score is only {copy_scores.get('headline_strength', 5.0):.1f}/10. Strong headlines are 3-15 words and include specific outcomes.",
                    "category": "copywriting"
                })
            
            if copy_scores.get("cta_strength", 5.0) < 5.0:
                recommendations.append({
                    "priority": "High",
                    "title": "Add Prominent, Action-Oriented CTAs",
                    "description": "Add 2-3 high-visibility CTAs with action words like 'Get Started', 'Claim Access', or 'Start Free Trial'. Place them above and below the fold.",
                    "reasoning": f"CTA strength is {copy_scores.get('cta_strength', 5.0):.1f}/10. Weak CTAs significantly reduce conversions.",
                    "category": "conversion"
                })
            
            if copy_scores.get("value_proposition", 5.0) < 6.0:
                recommendations.append({
                    "priority": "High",
                    "title": "Clarify Core Value Proposition",
                    "description": "Clearly state within the first heading what problem you solve and the primary benefit. Avoid jargon.",
                    "reasoning": f"Value proposition score is {copy_scores.get('value_proposition', 5.0):.1f}/10. Users should understand your value in seconds.",
                    "category": "copywriting"
                })
            
            if copy_scores.get("emotional_triggers", 5.0) < 5.0:
                recommendations.append({
                    "priority": "Medium",
                    "title": "Inject Emotional Triggers",
                    "description": "Add pain point references (what customers struggle with), desire language (benefits/dreams), and urgency (scarcity, deadlines).",
                    "reasoning": f"Emotional trigger score is {copy_scores.get('emotional_triggers', 5.0):.1f}/10. Emotional engagement improves conversion rates.",
                    "category": "copywriting"
                })
            
            if copy_scores.get("features_vs_benefits", 5.0) < 6.0:
                recommendations.append({
                    "priority": "Medium",
                    "title": "Reframe Features as Benefits",
                    "description": "For each feature listed, explain the benefit to the user. Use outcome-focused language (How does this improve their life?).",
                    "reasoning": f"Benefits-focused messaging score is {copy_scores.get('features_vs_benefits', 5.0):.1f}/10. Users care more about outcomes than features.",
                    "category": "copywriting"
                })
            
            # UX recommendations
            if ux_scores.get("readability", 5.0) < 6.0:
                recommendations.append({
                    "priority": "High",
                    "title": "Improve Content Readability",
                    "description": "Break text into shorter paragraphs (3-4 sentences), add subheadings every 100 words, use bullet points for lists.",
                    "reasoning": f"Readability score is {ux_scores.get('readability', 5.0):.1f}/10. Scannable content improves engagement and conversion.",
                    "category": "ux"
                })
            
            if ux_scores.get("visual_hierarchy", 5.0) < 6.0:
                recommendations.append({
                    "priority": "High",
                    "title": "Establish Clear Visual Hierarchy",
                    "description": "Use distinct heading sizes (H1 > H2 > H3), consistent spacing, and visual contrast between sections.",
                    "reasoning": f"Visual hierarchy score is {ux_scores.get('visual_hierarchy', 5.0):.1f}/10. Clear hierarchy guides user attention to key elements.",
                    "category": "design"
                })
            
            if ux_scores.get("conversion_friction", 5.0) < 6.0:
                recommendations.append({
                    "priority": "High",
                    "title": "Reduce Form Friction",
                    "description": f"Minimize form fields (aim for 1-3 essential fields). Offer multiple conversion paths (live chat, email, demo).",
                    "reasoning": f"Conversion friction score is {ux_scores.get('conversion_friction', 5.0):.1f}/10. Each form field reduces conversion rates by ~3-5%.",
                    "category": "conversion"
                })
            
            if ux_scores.get("information_density", 5.0) < 6.0:
                recommendations.append({
                    "priority": "Medium",
                    "title": "Optimize Information Density",
                    "description": "Aim for 1000-2000 words on the page. Too little doesn't convince; too much overwhelms. Add sections for different user types.",
                    "reasoning": f"Information density score is {ux_scores.get('information_density', 5.0):.1f}/10. Balance detail with scanability.",
                    "category": "ux"
                })
            
            if ux_scores.get("mobile_responsiveness", 5.0) < 7.0:
                recommendations.append({
                    "priority": "High",
                    "title": "Ensure Full Mobile Responsiveness",
                    "description": "Test on actual devices. Use mobile-friendly viewport meta tag. Stack columns vertically. Make buttons thumb-friendly (44x44px).",
                    "reasoning": f"Mobile responsiveness score is {ux_scores.get('mobile_responsiveness', 5.0):.1f}/10. 60%+ traffic is mobile; poor mobile UX kills conversions.",
                    "category": "design"
                })
            
            # Trust recommendations
            if trust_scores.get("social_proof", 5.0) < 6.0:
                recommendations.append({
                    "priority": "Medium",
                    "title": "Add Social Proof Section",
                    "description": "Include customer testimonials, reviews, ratings, customer count, case studies, or 'as seen in' logos.",
                    "reasoning": f"Social proof score is {trust_scores.get('social_proof', 5.0):.1f}/10. Third-party validation increases trust and conversion.",
                    "category": "trust"
                })
            
            if trust_scores.get("authority_signals", 5.0) < 6.0:
                recommendations.append({
                    "priority": "Medium",
                    "title": "Establish Authority and Expertise",
                    "description": "Mention years of experience, team expertise, industry awards, certifications, or featured media mentions.",
                    "reasoning": f"Authority score is {trust_scores.get('authority_signals', 5.0):.1f}/10. Authority signals reduce purchase risk perception.",
                    "category": "trust"
                })
            
            if trust_scores.get("credibility_signals", 5.0) < 5.0:
                recommendations.append({
                    "priority": "Medium",
                    "title": "Add Risk Reversal Guarantees",
                    "description": "Offer money-back guarantee, risk-free trial, satisfaction guarantee, or 30-day refund policy.",
                    "reasoning": f"Credibility signals score is {trust_scores.get('credibility_signals', 5.0):.1f}/10. Risk reversal removes conversion barriers.",
                    "category": "trust"
                })
            
            # Section recommendations
            if sections.get("total_sections", 0) < 6:
                recommendations.append({
                    "priority": "Medium",
                    "title": "Add Missing Page Sections",
                    "description": f"Current page has {sections.get('total_sections', 0)} main sections. Add sections for: Problem, Solution, Benefits, Testimonials, FAQ.",
                    "reasoning": f"Complete landing pages have 6-9 sections. Missing sections = lost sales opportunities.",
                    "category": "copywriting"
                })
            
            if not sections.get("detected_sections", {}).get("testimonials"):
                recommendations.append({
                    "priority": "Medium",
                    "title": "Create Testimonials/Reviews Section",
                    "description": "Add a dedicated section with 3-5 customer testimonials, including name, photo, and result achieved.",
                    "reasoning": "Testimonials are one of the strongest conversion drivers. Even 1-2 testimonials increase conversions by 20%+.",
                    "category": "trust"
                })
            
            if not sections.get("detected_sections", {}).get("faq"):
                recommendations.append({
                    "priority": "Low",
                    "title": "Add FAQ Section",
                    "description": "Anticipate and answer common objections and questions. This reduces friction and builds trust.",
                    "reasoning": "FAQs address objections without sales pressure, improving conversion and reducing support tickets.",
                    "category": "ux"
                })
            
            # Limit to 10 most important recommendations
            # Sort by priority
            priority_order = {"High": 0, "Medium": 1, "Low": 2}
            recommendations.sort(key=lambda x: (priority_order.get(x["priority"], 3), recommendations.index(x)))
            
            recommendations = recommendations[:10]
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return []
