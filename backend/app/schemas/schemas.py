from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl
from .base import BaseSchema


class AnalysisRequest(BaseSchema):
    urls: List[HttpUrl] = Field(
        ..., description="Landing page URLs to analyze"
    )


class AnalysisResponse(BaseSchema):
    job_id: str
    status: str
    website_url: Optional[HttpUrl] = None
    scores: List[Dict[str, Any]] = []
    recommendations: List[Dict[str, Any]] = []
    overall_score: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class ComparisonResponse(BaseSchema):
    job_id: str
    websites: List[Dict[str, Any]]
    ranking: List[Dict[str, Any]]
    best_category: Dict[str, Any]
    worst_category: Dict[str, Any]


class ReportResponse(BaseSchema):
    report_id: str
    status: str
    download_url: str
    created_at: datetime


class SimpleResponse(BaseSchema):
    message: str
