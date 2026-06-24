import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy()
    )
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core import logger, settings
from app.database import Base, engine
from app.routes import analysis_router

app = FastAPI(
    title=settings.app_name,
    description="Backend skeleton for Landing Page Intelligence & CRO Analyzer",
    version="0.1.0",
)

allowed_origins = ["*"] if settings.allowed_hosts == "*" else [origin.strip() for origin in settings.allowed_hosts.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis_router)


@app.get("/")
async def root():
    return JSONResponse(
        content={
            "status": "ok",
            "app": settings.app_name,
            "health": "/health",
            "docs": "/docs",
        }
    )


@app.get("/health")
async def health_check():
    logger.info("Health check requested")
    return JSONResponse(
        content={
            "status": "ok",
            "app": settings.app_name,
            "environment": settings.environment,
        }
    )


@app.on_event("startup")
async def on_startup():
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ensured")
    logger.info("Backend startup complete")


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Backend shutdown complete")
