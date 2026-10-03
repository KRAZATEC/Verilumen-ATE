"""
Verilumen ATE Intelligence Platform - FastAPI Application
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.api import upload, dashboard, investigation, prediction, analysis


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        description="Semiconductor ATE Intelligence Platform - Yield Analysis, Failure Diagnosis, Anomaly Detection & ML Prediction",
    )

    # CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Permits flexible local dev between Next.js and FastAPI
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check
    @application.get("/health")
    def health_check():
        return {
            "status": "healthy",
            "service": settings.PROJECT_NAME,
            "version": "1.0.0"
        }

    # Include routers under /api
    application.include_router(upload.router, prefix=settings.API_V1_STR)
    application.include_router(dashboard.router, prefix=settings.API_V1_STR)
    application.include_router(investigation.router, prefix=settings.API_V1_STR)
    application.include_router(prediction.router, prefix=settings.API_V1_STR)
    application.include_router(analysis.router, prefix=settings.API_V1_STR)

    logger.info("FastAPI application instantiated successfully with all routes configured.")
    return application


app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
