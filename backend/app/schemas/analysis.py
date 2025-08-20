"""
Analysis schemas
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, validator


class AnalysisCreate(BaseModel):
    """Analysis creation schema"""
    project_id: int
    analysis_type: str = "dependency"  # dependency, complexity, security
    options: Optional[Dict[str, Any]] = None
    
    @validator('analysis_type')
    def validate_analysis_type(cls, v):
        allowed_types = ["dependency", "complexity", "security", "full"]
        if v not in allowed_types:
            raise ValueError(f'Analysis type must be one of: {", ".join(allowed_types)}')
        return v


class AnalysisResponse(BaseModel):
    """Analysis response schema"""
    id: int
    project_id: int
    project_name: str
    analysis_type: str
    status: str  # pending, running, completed, failed
    progress: int = 0  # 0-100
    results: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class AnalysisList(BaseModel):
    """Analysis list response schema"""
    analyses: List[AnalysisResponse]
    total: int
    page: int
    size: int


class DependencyNode(BaseModel):
    """Dependency graph node"""
    id: str
    name: str
    type: str  # file, class, function, module
    language: str
    path: str
    complexity: Optional[float] = None
    lines_of_code: Optional[int] = None


class DependencyEdge(BaseModel):
    """Dependency graph edge"""
    source: str
    target: str
    type: str  # imports, calls, inherits, etc.
    weight: Optional[float] = None


class DependencyGraph(BaseModel):
    """Dependency graph structure"""
    nodes: List[DependencyNode]
    edges: List[DependencyEdge]
    metadata: Dict[str, Any]


class AnalysisResults(BaseModel):
    """Complete analysis results"""
    dependency_graph: DependencyGraph
    complexity_metrics: Dict[str, Any]
    risk_score: float
    recommendations: List[str]
    summary: str
