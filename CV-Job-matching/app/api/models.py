# app/api/models.py
"""Pydantic models for API requests and responses"""
from pydantic import BaseModel
from typing import List, Optional, Union, Any


class MatchResult(BaseModel):
    score: float
    recommendation: str
    strengths: List[Union[dict, str, Any]]
    gaps: List[Union[dict, str, Any]]
    processing_time: Optional[float] = None


class RankingResult(BaseModel):
    filename: str
    score: float
    recommendation: str
    strengths: List[Union[dict, str, Any]]
    gaps: List[Union[dict, str, Any]]
    processing_time: Optional[float] = None


class BulkRankingResponse(BaseModel):
    total_cvs: int
    total_time: float
    average_time: float
    results: List[RankingResult]


class HealthResponse(BaseModel):
    status: str
    version: str
    optimizations: dict
    timestamp: str


class CacheStats(BaseModel):
    cached_cvs: int
    cache_size_mb: float
    status: str
