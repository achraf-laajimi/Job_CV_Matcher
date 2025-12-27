# app/api/routes/__init__.py
"""API routes"""
from fastapi import APIRouter
from app.api.routes import health, matching, cache

# Create main router
api_router = APIRouter()

# Include all route modules
api_router.include_router(health.router)
api_router.include_router(matching.router)
api_router.include_router(cache.router)
