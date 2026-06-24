from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from datetime import datetime
import logging
from typing import List, Dict
import os

logger = logging.getLogger(__name__)


class PDFReportService:
    """Service to generate PDF reports."""

    @staticmethod
    def generate_report(output_path: str,
                       website_url: str,
                       category_scores: Dict[str, float],
                       overall_score: float,
                       sections: Dict,
                       recommendations: List[Dict],
                       copy_scores: Dict[str, float],
                       ux_scores: Dict[str, float],
                       trust_scores: Dict[str, float]) -> str:
        """
        Generate a comprehensive PDF report.
        
        Args:
            output_path: Path to save PDF
            website_url: The analyzed website URL
            category_scores: Dict of category scores
            overall_score: Overall weighted score (0-100)
            sections: Detected sections info
            recommendations: List of recommendations
            copy_scores: Copywriting metrics
            ux_scores: UX metrics
            trust_scores: Trust metrics
            
        Returns:
            Path to generated PDF
        """
        try:
            # Create output directory if needed
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Create PDF
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            elements = []
            
            # Styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1F2937'),
                spaceAfter=12,
                alignment=1
            )
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#374151'),
                spaceAfter=8,
                spaceBefore=12
            )
            
            # Title and Date
            elements.append(Paragraph("Landing Page Analysis Report", title_style))
            elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            elements.append(Spacer(1, 0.3 * inch))
            
            # Website URL
            elements.append(Paragraph(f"<b>Website:</b> {website_url}", styles['Normal']))
            elements.append(Spacer(1, 0.2 * inch))
            
            # Executive Summary - Overall Score
            elements.append(Paragraph("Executive Summary", heading_style))
            score_color = PDFReportService._get_score_color(overall_score)
            elements.append(Paragraph(
                f"<b>Overall Score: <font color='{score_color}'>{overall_score:.0f}/100</font></b>",
                styles['Normal']
            ))
            elements.append(Spacer(1, 0.2 * inch))
            
            # Category Scores Table
            elements.append(Paragraph("Category Breakdown", heading_style))
            category_data = [["Category", "Score", "Rating"]]
            for category, score in category_scores.items():
                rating = PDFReportService._get_rating(score)
                category_data.append([
                    category.replace("_", " ").title(),
                    f"{score:.1f}/10",
                    rating
                ])
            
            category_table = Table(category_data, colWidths=[2*inch, 1.5*inch, 2*inch])
            category_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F2937')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(category_table)
            elements.append(Spacer(1, 0.3 * inch))
            
            # Copywriting Analysis
            elements.append(Paragraph("Copywriting Analysis", heading_style))
            copy_data = [["Metric", "Score"]]
            for metric, score in copy_scores.items():
                copy_data.append([
                    metric.replace("_", " ").title(),
                    f"{score:.1f}/10"
                ])
            
            copy_table = Table(copy_data, colWidths=[3*inch, 1.5*inch])
            copy_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F2937')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(copy_table)
            elements.append(Spacer(1, 0.3 * inch))
            
            # UX Analysis
            elements.append(Paragraph("UX Analysis", heading_style))
            ux_data = [["Metric", "Score"]]
            for metric, score in ux_scores.items():
                ux_data.append([
                    metric.replace("_", " ").title(),
                    f"{score:.1f}/10"
                ])
            
            ux_table = Table(ux_data, colWidths=[3*inch, 1.5*inch])
            ux_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F2937')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(ux_table)
            elements.append(PageBreak())
            
            # Trust Analysis
            elements.append(Paragraph("Trust & Credibility Analysis", heading_style))
            trust_data = [["Metric", "Score"]]
            for metric, score in trust_scores.items():
                trust_data.append([
                    metric.replace("_", " ").title(),
                    f"{score:.1f}/10"
                ])
            
            trust_table = Table(trust_data, colWidths=[3*inch, 1.5*inch])
            trust_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F2937')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(trust_table)
            elements.append(Spacer(1, 0.3 * inch))
            
            # Sections Detected
            elements.append(Paragraph("Page Sections Detected", heading_style))
            detected = sections.get("detected_sections", {})
            section_text = ", ".join([s.replace("_", " ").title() for s, v in detected.items() if v])
            if not section_text:
                section_text = "No major sections detected"
            elements.append(Paragraph(f"<b>Sections:</b> {section_text}", styles['Normal']))
            elements.append(Spacer(1, 0.2 * inch))
            elements.append(Paragraph(
                f"<b>Total Sections:</b> {sections.get('total_sections', 0)}/9",
                styles['Normal']
            ))
            elements.append(PageBreak())
            
            # Recommendations
            elements.append(Paragraph("Actionable Recommendations", heading_style))
            
            high_recs = [r for r in recommendations if r.get("priority") == "High"]
            med_recs = [r for r in recommendations if r.get("priority") == "Medium"]
            low_recs = [r for r in recommendations if r.get("priority") == "Low"]
            
            if high_recs:
                elements.append(Paragraph("<b>HIGH PRIORITY</b>", ParagraphStyle(
                    'HighPriority', parent=styles['Normal'], textColor=colors.red, fontSize=11
                )))
                for i, rec in enumerate(high_recs[:5], 1):
                    elements.append(Paragraph(
                        f"<b>{i}. {rec.get('title')}</b><br/>{rec.get('description', '')}",
                        styles['Normal']
                    ))
                    elements.append(Spacer(1, 0.1 * inch))
            
            if med_recs:
                elements.append(Spacer(1, 0.2 * inch))
                elements.append(Paragraph("<b>MEDIUM PRIORITY</b>", ParagraphStyle(
                    'MedPriority', parent=styles['Normal'], textColor=colors.orange, fontSize=11
                )))
                for i, rec in enumerate(med_recs[:5], 1):
                    elements.append(Paragraph(
                        f"<b>{i}. {rec.get('title')}</b><br/>{rec.get('description', '')}",
                        styles['Normal']
                    ))
                    elements.append(Spacer(1, 0.1 * inch))
            
            if low_recs:
                elements.append(Spacer(1, 0.2 * inch))
                elements.append(Paragraph("<b>LOW PRIORITY</b>", ParagraphStyle(
                    'LowPriority', parent=styles['Normal'], textColor=colors.green, fontSize=11
                )))
                for i, rec in enumerate(low_recs[:3], 1):
                    elements.append(Paragraph(
                        f"<b>{i}. {rec.get('title')}</b><br/>{rec.get('description', '')}",
                        styles['Normal']
                    ))
                    elements.append(Spacer(1, 0.1 * inch))
            
            # Build PDF
            doc.build(elements)
            logger.info(f"PDF report generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating PDF report: {str(e)}")
            raise

    @staticmethod
    def _get_score_color(score: float) -> str:
        """Get color based on score."""
        if score >= 80:
            return "#10B981"  # Green
        elif score >= 60:
            return "#F59E0B"  # Amber
        else:
            return "#EF4444"  # Red

    @staticmethod
    def _get_rating(score: float) -> str:
        """Get rating label based on score."""
        if score >= 8.5:
            return "Excellent"
        elif score >= 7.0:
            return "Good"
        elif score >= 5.0:
            return "Average"
        elif score >= 3.0:
            return "Fair"
        else:
            return "Poor"
