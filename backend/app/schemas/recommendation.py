"""
Recommendation schemas
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, validator


class RecommendationResponse(BaseModel):
    """Recommendation response schema"""
    id: int
    analysis_id: int
    type: str  # refactoring, security, performance, maintainability
    title: str
    description: str
    severity: str  # low, medium, high, critical
    confidence: float  # 0.0 - 1.0
    code_snippet: Optional[str] = None
    suggested_changes: Optional[Dict[str, Any]] = None
    impact_score: float  # 0.0 - 1.0
    effort_estimate: str  # low, medium, high
    created_at: datetime
    
    class Config:
        from_attributes = True


class RecommendationList(BaseModel):
    """Recommendation list response schema"""
    recommendations: List[RecommendationResponse]
    total: int
    page: int
    size: int


class RecommendationCreate(BaseModel):
    """Recommendation creation schema"""
    analysis_id: int
    type: str
    title: str
    description: str
    severity: str
    confidence: float
    code_snippet: Optional[str] = None
    suggested_changes: Optional[Dict[str, Any]] = None
    impact_score: float
    effort_estimate: str
    
    @validator('severity')
    def validate_severity(cls, v):
        allowed_severities = ["low", "medium", "high", "critical"]
        if v not in allowed_severities:
            raise ValueError(f'Severity must be one of: {", ".join(allowed_severities)}')
        return v
    
    @validator('confidence', 'impact_score')
    def validate_score(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Score must be between 0.0 and 1.0')
        return v
    
    @validator('effort_estimate')
    def validate_effort(cls, v):
        allowed_efforts = ["low", "medium", "high"]
        if v not in allowed_efforts:
            raise ValueError(f'Effort estimate must be one of: {", ".join(allowed_efforts)}')
        return v
