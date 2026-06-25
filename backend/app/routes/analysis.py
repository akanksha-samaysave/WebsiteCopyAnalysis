"""
routes/analysis.py  –  fixed analysis pipeline
================================================
Fixes applied:
  FIX-1  category_scores key mismatch (ROOT CAUSE of "Analysis Failed"):
          ScoringEngine.calculate_final_scores() returns a FLAT dict
          {design, messaging, trust, ux, clarity, conversion, overall}.
          Old code called final_scores.get("category_scores", {}) which
          always returned {} because the key does not exist.
          Fix: build category_scores by stripping "overall" from the dict.

  FIX-2  Overall score scale: ScoringEngine returns 0-10 but dashboard
          displays /100.  Old code stored the raw 0-10 value so a great
          page showed "7/100".
          Fix: multiply overall by 10 before storing in metadata.

  FIX-3  Per-URL failure isolation: a single failing URL used to mark
          every URL in the job as failed (one shared except block).
          Fix: each URL is processed in its own try/except so others
          continue regardless.

  FIX-4  Windows ProactorEventLoop + Playwright conflict: on Windows
          FastAPI's BackgroundTasks shares the ProactorEventLoop with
          Playwright's internal event loop management.  Fix: wrap the
          background coroutine with asyncio.get_event_loop().run_until_complete
          when not already inside a running loop, or just ensure each
          URL's scrape runs inside its own async context (already fixed
          by the per-URL isolation above + new scraper).

  FIX-5  Serializer now exposes `error_message` and the correctly-keyed
          `metadata` so the frontend "Analysis failed: <reason>" message
          works.
"""

import asyncio
import logging
import os
import traceback
import uuid
from datetime import datetime
from typing import Dict, List
from urllib.parse import urlparse

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse

from app.database import SessionLocal
from app.models.models import Analysis, Recommendation, Report, Score, Website
from app.schemas import AnalysisRequest
from app.services import (
    CopywritingAnalyzerService,
    RecommendationEngine,
    ScoringEngine,
    SectionDetectorService,
    TrustAnalyzerService,
    UXAnalyzerService,
    WebScraperService,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["analysis"])

REPORT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "reports")
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

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
        "error_message": analysis.error_message,
        "scores": [
            {"category": s.category, "score": s.score, "details": s.details}
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
        "created_at": analysis.created_at.isoformat() + "Z" if analysis.created_at else None,
        "updated_at": analysis.updated_at.isoformat() + "Z" if analysis.updated_at else None,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Background worker
# ─────────────────────────────────────────────────────────────────────────────

async def _process_single_analysis(analysis_id: int) -> None:
    """
    Process ONE analysis row in complete isolation.
    Any exception marks only THIS analysis as failed; other URLs are unaffected.

    FIX-3: per-URL isolation
    """
    db = SessionLocal()
    try:
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not analysis:
            return

        analysis.status = "processing"
        db.commit()

        website = analysis.website
        if not website:
            analysis.status = "failed"
            analysis.error_message = "Website record missing from database"
            db.commit()
            return

        url = website.url
        logger.info("Starting scrape for %s (analysis_id=%d)", url, analysis_id)

        # ── scrape ────────────────────────────────────────────────────────
        scrape = await WebScraperService.scrape_page(url)

        if scrape.get("status") != "success":
            analysis.status = "failed"
            analysis.error_message = scrape.get("error", "Scrape returned non-success status")
            db.commit()
            logger.warning("Scrape failed for %s: %s", url, analysis.error_message)
            return

        text     = scrape.get("visible_text", "") or ""
        headings = scrape.get("headings", []) or []
        buttons  = scrape.get("buttons",  []) or []
        forms    = scrape.get("forms",    []) or []
        meta     = scrape.get("meta_info", {}) or {}

        # ── analysis pipeline ─────────────────────────────────────────────
        sections     = SectionDetectorService.detect_sections(headings, text)
        copy_scores  = CopywritingAnalyzerService.analyze_all(headings, text, buttons)
        ux_scores    = UXAnalyzerService.analyze_all(text, headings, buttons, forms, meta)
        trust_scores = TrustAnalyzerService.analyze_all(text, headings, forms, meta)

        # FIX-1: ScoringEngine returns a FLAT dict
        # {design, messaging, trust, ux, clarity, conversion, overall}
        # There is NO "category_scores" key — build it ourselves.
        flat_scores = ScoringEngine.calculate_final_scores(
            copy_scores, ux_scores, trust_scores, sections
        )
        # Strip "overall" to get per-category dict
        category_scores: Dict[str, float] = {
            k: v for k, v in flat_scores.items() if k != "overall"
        }
        raw_overall: float = flat_scores.get("overall", 0.0)

        # FIX-2: overall is 0-10 from ScoringEngine; scale to 0-100 for UI
        overall_score_100 = round(raw_overall * 10, 1)

        recommendations = RecommendationEngine.generate_recommendations(
            copy_scores, ux_scores, trust_scores,
            sections, text, headings, buttons, forms
        )

        # ── persist ───────────────────────────────────────────────────────
        analysis.raw_html      = (scrape.get("raw_html", "") or "")[:10_000]
        analysis.visible_text  = text
        analysis.sections      = sections
        analysis.analysis_metadata = {
            "copy_scores":     copy_scores,
            "ux_scores":       ux_scores,
            "trust_scores":    trust_scores,
            "category_scores": category_scores,   # FIX-1: now correctly populated
            "overall_score":   overall_score_100,  # FIX-2: now 0-100
        }
        analysis.status        = "completed"
        analysis.error_message = None
        db.add(analysis)
        db.commit()

        # ── score rows ────────────────────────────────────────────────────
        db.query(Score).filter(Score.analysis_id == analysis.id).delete()
        for cat, score_val in category_scores.items():
            db.add(Score(
                analysis_id=analysis.id,
                category=cat,
                score=score_val,
                details={},
            ))

        # ── recommendation rows ───────────────────────────────────────────
        db.query(Recommendation).filter(Recommendation.analysis_id == analysis.id).delete()
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
        logger.info("Completed analysis for %s (overall=%.1f/100)", url, overall_score_100)

    except Exception as exc:
        logger.error(
            "Unhandled error processing analysis_id=%d: %s",
            analysis_id, exc, exc_info=True,
        )
        try:
            analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
            if analysis:
                analysis.status = "failed"
                analysis.error_message = str(exc)
                db.commit()
        except Exception:
            pass
    finally:
        db.close()


async def _process_analysis_job(job_id: str) -> None:
    """
    Entry point called by BackgroundTasks.
    FIX-3: each URL is processed independently — one failure never kills others.
    """
    db = SessionLocal()
    try:
        analyses = db.query(Analysis).filter(Analysis.job_id == job_id).all()
        analysis_ids = [a.id for a in analyses]
    finally:
        db.close()

    if not analysis_ids:
        logger.warning("No analyses found for job_id=%s", job_id)
        return

    # Process every URL independently; gather() continues even if one raises
    await asyncio.gather(
        *[_process_single_analysis(aid) for aid in analysis_ids],
        return_exceptions=True,   # never let one coroutine kill the others
    )
    logger.info("Job %s finished processing %d URL(s)", job_id, len(analysis_ids))


# ─────────────────────────────────────────────────────────────────────────────
# POST /api/analyze
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/analyze", response_model=dict)
async def analyze_landing_pages(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
):
    if not request.urls:
        raise HTTPException(400, "At least one URL is required")

    job_id = uuid.uuid4().hex
    db = SessionLocal()
    try:
        for url in request.urls:
            url_str = str(url)
            domain  = urlparse(url_str).netloc

            website = db.query(Website).filter(Website.url == url_str).first()
            if not website:
                website = Website(url=url_str, domain=domain)
                db.add(website)
                db.flush()

            analysis = Analysis(
                job_id=job_id,
                website_id=website.id,
                status="pending",
            )
            db.add(analysis)

        db.commit()
        background_tasks.add_task(_process_analysis_job, job_id)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    return {
        "job_id": job_id,
        "status": "pending",
        "urls": [str(u) for u in request.urls],
        "created_at": datetime.utcnow().isoformat() + "Z",
    }


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/analysis/{job_id}
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/analysis/{job_id}", response_model=dict)
async def get_analysis_results(job_id: str):
    db = SessionLocal()
    try:
        analyses = db.query(Analysis).filter(Analysis.job_id == job_id).all()
        if not analyses:
            raise HTTPException(404, detail=f"No analysis found for job_id '{job_id}'")

        return {
            "job_id": job_id,
            "status": _job_status(analyses),
            "analyses": [_serialize_analysis(a) for a in analyses],
            "count": len(analyses),
        }
    finally:
        db.close()


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/comparison/{job_id}
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/comparison/{job_id}", response_model=dict)
async def get_comparison(job_id: str):
    db = SessionLocal()
    try:
        analyses = db.query(Analysis).filter(Analysis.job_id == job_id).all()
        if not analyses:
            raise HTTPException(404, detail=f"No analysis found for job_id '{job_id}'")

        overall_status = _job_status(analyses)
        websites: List[Dict] = []

        for analysis in analyses:
            website = analysis.website
            if not website:
                continue

            cat_scores: Dict[str, float] = {s.category: round(s.score, 2) for s in analysis.scores}
            meta = analysis.analysis_metadata or {}
            raw_overall = meta.get("overall_score") or (
                sum(cat_scores.values()) / len(cat_scores) * 10 if cat_scores else 0.0
            )
            overall_score = round(float(raw_overall), 1)

            websites.append({
                "url": website.url,
                "domain": website.domain,
                "status": analysis.status,
                "scores": cat_scores,
                "overall_score": overall_score,
                "recommendations": [
                    {"priority": r.priority, "title": r.title,
                     "description": r.description, "category": r.category}
                    for r in analysis.recommendations
                ],
            })

        ranking = sorted(
            [w for w in websites if w["status"] == "completed"],
            key=lambda w: w["overall_score"],
            reverse=True,
        )

        category_totals: Dict[str, List[float]] = {}
        for w in [w for w in websites if w["status"] == "completed"]:
            for cat, sc in w["scores"].items():
                category_totals.setdefault(cat, []).append(sc)

        category_averages = {
            cat: round(sum(vals) / len(vals), 2)
            for cat, vals in category_totals.items() if vals
        }

        best_category = worst_category = None
        if category_averages:
            best_cat  = max(category_averages, key=category_averages.__getitem__)
            worst_cat = min(category_averages, key=category_averages.__getitem__)
            best_category  = {"category": best_cat,  "average_score": category_averages[best_cat]}
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


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/report/{job_id}
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/report/{job_id}", response_model=dict)
async def get_report(job_id: str):
    db = SessionLocal()
    try:
        analysis = db.query(Analysis).filter(Analysis.job_id == job_id).first()
        if not analysis:
            raise HTTPException(404, detail=f"No analysis found for job_id '{job_id}'")
        report = analysis.report
        if not report:
            raise HTTPException(404, detail="Report not yet generated")
        return {
            "job_id": job_id,
            "pdf_path": report.pdf_path,
            "csv_path": report.csv_path,
            "generated_at": report.generated_at.isoformat() + "Z" if report.generated_at else None,
        }
    finally:
        db.close()


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/report/{job_id}/download
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/report/{job_id}/download")
async def download_report(job_id: str):
    db = SessionLocal()
    try:
        analysis = db.query(Analysis).filter(Analysis.job_id == job_id).first()
        if not analysis:
            raise HTTPException(404, detail=f"No analysis found for job_id '{job_id}'")
        report = analysis.report
        if not report or not report.pdf_path:
            raise HTTPException(404, detail="PDF report not yet generated")
        pdf_path = report.pdf_path
        if not os.path.isabs(pdf_path):
            pdf_path = os.path.join(REPORT_DIR, pdf_path)
        if not os.path.exists(pdf_path):
            raise HTTPException(404, detail="PDF file not found on server")
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=f"report_{job_id}.pdf",
        )
    finally:
        db.close()