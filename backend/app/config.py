"""
Application configuration and constants.
"""

import os
from enum import Enum

# Environment
ENV = os.getenv("ENVIRONMENT", "development")
DEBUG = ENV == "development"

# Database
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./analytics.db"
)

# Analysis Settings
MAX_URLS_PER_ANALYSIS = 5
ANALYSIS_TIMEOUT_SECONDS = 300  # 5 minutes per URL
BROWSER_HEADLESS = True

# Scoring Weights (must sum to 1.0)
SCORING_WEIGHTS = {
    "design": 0.15,
    "messaging": 0.25,
    "trust": 0.20,
    "clarity": 0.15,
    "conversion": 0.15,
    "ux": 0.10
}

# Section Types
SECTION_TYPES = [
    "hero",
    "problem",
    "solution",
    "benefits",
    "features",
    "testimonials",
    "pricing",
    "faq",
    "cta"
]

# Score Ranges
MIN_SCORE = 0.0
MAX_SCORE = 10.0
PERFECT_SCORE = 100.0

# Recommendation Priorities
class RecommendationPriority(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

# Analysis Status
class AnalysisStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

# API Configuration
CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "*"  # Allow all in development
]

# Paths
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "reports")
SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "screenshots")

# Create directories if they don't exist
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
