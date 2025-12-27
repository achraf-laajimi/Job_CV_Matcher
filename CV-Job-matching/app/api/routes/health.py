# app/api/routes/health.py
"""Health check and system status endpoints"""
from fastapi import APIRouter
from datetime import datetime
from app.api.models import HealthResponse

router = APIRouter(prefix="", tags=["Health"])


@router.get("/", response_model=dict)
async def root():
    """Welcome endpoint with API information"""
    return {
        "message": "CV-Job Matching API",
        "version": "2.0.0",
        "endpoints": {
            "POST /match": "Match single CV against job description",
            "POST /rank": "Rank multiple CVs against job description",
            "GET /health": "Health check and system status",
            "GET /cache/stats": "Get cache statistics",
            "DELETE /cache": "Clear all cached data",
            "GET /docs": "API documentation"
        }
    }


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint with optimization status"""
    return HealthResponse(
        status="healthy",
        version="2.0.0",
        optimizations={
            "caching": True,
            "text_trimming": True,
            "parallelization": True,
            "token_limits": True
        },
        timestamp=datetime.now().isoformat()
    )
