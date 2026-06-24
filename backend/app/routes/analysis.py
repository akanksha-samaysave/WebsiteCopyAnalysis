import traceback
import os
import uuid
from datetime import datetime
from typing import Dict, List
from urllib.parse import urlparse

from fastapi import APIRouter, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.models import Website, Analysis, Score, Recommendation, Report
from app.schemas import AnalysisRequest, ReportResponse

from app.services import (
    WebScraperService,
    SectionDetectorService,
    CopywritingAnalyzerService,
    UXAnalyzerService,
    TrustAnalyzerService,
    ScoringEngine,
    RecommendationEngine,
    PDFReportService,
)

router = APIRouter(prefix="/api", tags=["analysis"])

REPORT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "reports")
)


# -----------------------------
# Helpers
# -----------------------------

def _job_status(analyses: List[Analysis]) -> str:
    statuses = {a.status for a in analyses}
    if "processing" in statuses:
        return "processing"
    if "pending" in statuses:
        return "pending"
    if "failed" in statuses and "completed" not in statuses:
        return "failed"
    if "failed" in statuses:
        return "partial"
    return "completed"


def _recommendation_category(issue: str) -> str:
    issue = (issue or "").lower()
    if "cta" in issue or "conversion" in issue:
        return "conversion"
    if "trust" in issue or "testimonial" in issue:
        return "trust"
    if "ux" in issue or "readability" in issue:
        return "ux"
    if "headline" in issue or "copy" in issue:
        return "copywriting"
    return "general"


def _serialize_analysis(analysis: Analysis) -> Dict:
    return {
        "analysis_id": analysis.job_id,
        "website_url": analysis.website.url if analysis.website else None,
        "status": analysis.status,
        "scores": [
            {
                "category": s.category,
                "score": s.score,
                "details": s.details,
            }
            for s in analysis.scores
        ],
        "recommendations": [
            {
                "priority": r.priority,
                "title": r.title,
                "description": r.description,
                "reasoning": r.reasoning,
                "category": r.category,
            }
            for r in analysis.recommendations
        ],
        "sections": analysis.sections or {},
        "metadata": analysis.analysis_metadata or {},
        "created_at": analysis.created_at.isoformat() + "Z"
        if analysis.created_at else None,
        "updated_at": analysis.updated_at.isoformat() + "Z"
        if analysis.updated_at else None,
    }


# -----------------------------
# Background Processing
# -----------------------------

async def _process_analysis_job(job_id: str):
    db = SessionLocal()
    try:
        analyses = db.query(Analysis).filter(Analysis.job_id == job_id).all()
        if not analyses:
            return

        for analysis in analyses:
            analysis.status = "processing"
            db.commit()

            website = analysis.website
            if not website:
                analysis.status = "failed"
                analysis.error_message = "Website missing"
                db.commit()
                continue

            scrape = await WebScraperService.scrape_page(website.url)

            if scrape.get("status") != "success":
                analysis.status = "failed"
                analysis.error_message = scrape.get("error", "Scrape failed")
                db.commit()
                continue

            text = scrape.get("visible_text", "") or ""
            headings = scrape.get("headings", []) or []
            buttons = scrape.get("buttons", []) or []
            forms = scrape.get("forms", []) or []
            meta = scrape.get("meta_info", {}) or {}

            sections = SectionDetectorService.detect_sections(headings, text)

            copy_scores = CopywritingAnalyzerService.analyze_all(headings, text, buttons)
            ux_scores = UXAnalyzerService.analyze_all(text, headings, buttons, forms, meta)
            trust_scores = TrustAnalyzerService.analyze_all(text, headings, forms, meta)

            final_scores = ScoringEngine.calculate_final_scores(
                copy_scores, ux_scores, trust_scores, sections
            )

            recommendations = RecommendationEngine.generate_recommendations(
                copy_scores, ux_scores, trust_scores,
                sections, text, headings, buttons, forms
            )

            analysis.raw_html = scrape.get("raw_html", "")[:10000]
            analysis.visible_text = text
            analysis.sections = sections

            analysis.analysis_metadata = {
                "copy_scores": copy_scores,
                "ux_scores": ux_scores,
                "trust_scores": trust_scores,
                "category_scores": final_scores.get("category_scores", {}),
                "overall_score": final_scores.get("overall", 0.0),
            }

            analysis.status = "completed"
            analysis.error_message = None

            db.add(analysis)
            db.commit()

            # scores
            db.query(Score).filter(Score.analysis_id == analysis.id).delete()
            for cat, score in analysis.analysis_metadata["category_scores"].items():
                db.add(Score(
                    analysis_id=analysis.id,
                    category=cat,
                    score=score,
                    details={}
                ))

            # recommendations
            db.query(Recommendation).filter(
                Recommendation.analysis_id == analysis.id
            ).delete()

            for rec in recommendations:
                db.add(Recommendation(
                    analysis_id=analysis.id,
                    priority=rec.get("impact", "Medium"),
                    title=rec.get("issue", ""),
                    description=rec.get("recommendation", ""),
                    reasoning=f"Based on {rec.get('issue', '')}",
                    category=_recommendation_category(rec.get("issue", "")),
                ))

            db.commit()

    except Exception as e:
        print("Analysis Error:", e)
        traceback.print_exc()

        for a in db.query(Analysis).filter(
            Analysis.job_id == job_id
        ).all():
            a.status = "failed"
            a.error_message = str(e)

        db.commit()

    finally:
        db.close()


# -----------------------------
# POST /api/analyze  — start a job
# -----------------------------

@router.post("/analyze", response_model=dict)
async def analyze_landing_pages(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks
):
    if not request.urls:
        raise HTTPException(400, "At least one URL required")

    job_id = uuid.uuid4().hex
    db = SessionLocal()

    try:
        for url in request.urls:
            url_str = str(url)
            domain = urlparse(url_str).netloc

            website = db.query(Website).filter(
                Website.url == url_str
            ).first()

            if not website:
                website = Website(
                    url=url_str,
                    domain=domain
                )
                db.add(website)
                db.flush()

            analysis = Analysis(
                job_id=job_id,
                website_id=website.id,
                status="pending"
            )
            db.add(analysis)

        db.commit()

        background_tasks.add_task(_process_analysis_job, job_id)

    finally:
        db.close()

    return {
        "job_id": job_id,
        "status": "pending",
        "urls": [str(u) for u in request.urls],
        "created_at": datetime.utcnow().isoformat() + "Z"
    }


# -----------------------------
# FIX 1 — GET /api/analysis/{job_id}
# The frontend calls this to poll a single job's status/results.
# It was completely missing from the backend.
# -----------------------------

@router.get("/analysis/{job_id}", response_model=dict)
async def get_analysis_results(job_id: str):
    db = SessionLocal()
    try:
        analyses = (
            db.query(Analysis)
            .filter(Analysis.job_id == job_id)
            .all()
        )
        if not analyses:
            raise HTTPException(
                status_code=404,
                detail=f"No analysis found for job_id '{job_id}'"
            )

        overall_status = _job_status(analyses)

        return {
            "job_id": job_id,
            "status": overall_status,
            "analyses": [_serialize_analysis(a) for a in analyses],
            "count": len(analyses),
        }
    finally:
        db.close()


# -----------------------------
# FIX 2 — GET /api/comparison/{job_id}   ← ROOT CAUSE OF THE 404
#
# The frontend (ComparisonPage.jsx + api.js) calls:
#   GET /api/comparison/<jobId>
# but this endpoint never existed in the backend.  The fix adds it.
#
# The endpoint aggregates every completed Analysis that belongs to the
# job, computes per-website category scores and an overall score, ranks
# the websites, and identifies the best/worst scoring category — exactly
# the shape ComparisonPage.jsx expects:
#
#   { ranking, websites, best_category, worst_category }
# -----------------------------

@router.get("/comparison/{job_id}", response_model=dict)
async def get_comparison(job_id: str):
    db = SessionLocal()
    try:
        analyses = (
            db.query(Analysis)
            .filter(Analysis.job_id == job_id)
            .all()
        )
        if not analyses:
            raise HTTPException(
                status_code=404,
                detail=f"No analysis found for job_id '{job_id}'"
            )

        overall_status = _job_status(analyses)

        # Build per-website data from completed analyses only
        websites = []
        for analysis in analyses:
            website = analysis.website
            if not website:
                continue

            # Gather category scores (stored in the Score rows)
            cat_scores: Dict[str, float] = {}
            for s in analysis.scores:
                cat_scores[s.category] = round(s.score, 2)

            # Overall score stored in metadata; fall back to mean of categories
            meta = analysis.analysis_metadata or {}
            raw_overall = meta.get("overall_score", None)
            if raw_overall is None and cat_scores:
                raw_overall = sum(cat_scores.values()) / len(cat_scores)
            overall_score = round(float(raw_overall or 0), 2)

            websites.append({
                "url": website.url,
                "domain": website.domain,
                "status": analysis.status,
                "scores": cat_scores,
                "overall_score": overall_score,
                "recommendations": [
                    {
                        "priority": r.priority,
                        "title": r.title,
                        "description": r.description,
                        "category": r.category,
                    }
                    for r in analysis.recommendations
                ],
            })

        # Rank completed websites by overall score descending
        ranking = sorted(
            [w for w in websites if w["status"] == "completed"],
            key=lambda w: w["overall_score"],
            reverse=True,
        )

        # Compute average score per category across all completed sites
        category_totals: Dict[str, List[float]] = {}
        for w in websites:
            if w["status"] != "completed":
                continue
            for cat, score in w["scores"].items():
                category_totals.setdefault(cat, []).append(score)

        category_averages = {
            cat: round(sum(vals) / len(vals), 2)
            for cat, vals in category_totals.items()
            if vals
        }

        best_category = None
        worst_category = None
        if category_averages:
            best_cat = max(category_averages, key=category_averages.__getitem__)
            worst_cat = min(category_averages, key=category_averages.__getitem__)
            best_category = {"category": best_cat, "average_score": category_averages[best_cat]}
            worst_category = {"category": worst_cat, "average_score": category_averages[worst_cat]}

        return {
            "job_id": job_id,
            "status": overall_status,
            "ranking": ranking,
            "websites": websites,
            "best_category": best_category,
            "worst_category": worst_category,
            "category_averages": category_averages,
        }
    finally:
        db.close()


# -----------------------------
# FIX 3 — GET /api/report/{job_id}
# The frontend api.js also calls this; it was missing too.
# Returns paths/metadata for any generated report.
# -----------------------------

@router.get("/report/{job_id}", response_model=dict)
async def get_report(job_id: str):
    db = SessionLocal()
    try:
        analysis = (
            db.query(Analysis)
            .filter(Analysis.job_id == job_id)
            .first()
        )
        if not analysis:
            raise HTTPException(
                status_code=404,
                detail=f"No analysis found for job_id '{job_id}'"
            )

        report = analysis.report
        if not report:
            raise HTTPException(
                status_code=404,
                detail="Report not yet generated for this job"
            )

        return {
            "job_id": job_id,
            "pdf_path": report.pdf_path,
            "csv_path": report.csv_path,
            "generated_at": report.generated_at.isoformat() + "Z"
            if report.generated_at else None,
        }
    finally:
        db.close()


# -----------------------------
# FIX 4 — GET /api/report/{job_id}/download
# The frontend api.js calls this for blob download; was also missing.
# -----------------------------

from fastapi.responses import FileResponse

@router.get("/report/{job_id}/download")
async def download_report(job_id: str):
    db = SessionLocal()
    try:
        analysis = (
            db.query(Analysis)
            .filter(Analysis.job_id == job_id)
            .first()
        )
        if not analysis:
            raise HTTPException(
                status_code=404,
                detail=f"No analysis found for job_id '{job_id}'"
            )

        report = analysis.report
        if not report or not report.pdf_path:
            raise HTTPException(
                status_code=404,
                detail="PDF report not yet generated for this job"
            )

        pdf_path = report.pdf_path
        if not os.path.isabs(pdf_path):
            pdf_path = os.path.join(REPORT_DIR, pdf_path)

        if not os.path.exists(pdf_path):
            raise HTTPException(
                status_code=404,
                detail="PDF file not found on server"
            )

        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=f"report_{job_id}.pdf",
        )
    finally:
        db.close()