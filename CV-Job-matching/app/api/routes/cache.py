# app/api/routes/cache.py
"""Cache management endpoints"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pathlib import Path

from app.pipeline import clear_cache
from app.api.models import CacheStats

router = APIRouter(prefix="/cache", tags=["Cache"])


@router.get("/stats", response_model=CacheStats)
async def get_cache_stats():
    """Get cache statistics"""
    cache_dir = Path(".cache")
    
    if not cache_dir.exists():
        return CacheStats(
            cached_cvs=0,
            cache_size_mb=0,
            status="empty"
        )
    
    cache_files = list(cache_dir.glob("*.json"))
    total_size = sum(f.stat().st_size for f in cache_files)
    
    return CacheStats(
        cached_cvs=len(cache_files),
        cache_size_mb=round(total_size / (1024 * 1024), 2),
        status="active"
    )


@router.delete("")
async def clear_cv_cache(background_tasks: BackgroundTasks):
    """
    Clear all cached CV data
    
    This will force re-processing of all CVs on next request
    """
    try:
        background_tasks.add_task(clear_cache)
        return {
            "message": "Cache cleared successfully",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing cache: {str(e)}")
