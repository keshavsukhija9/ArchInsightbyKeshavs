"""
Project schemas
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, validator


class ProjectCreate(BaseModel):
    """Project creation schema"""
    name: str
    description: Optional[str] = None
    repository_url: Optional[str] = None
    language: Optional[str] = None
    
    @validator('name')
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Project name cannot be empty')
        if len(v) > 100:
            raise ValueError('Project name must be less than 100 characters')
        return v.strip()


class ProjectUpdate(BaseModel):
    """Project update schema"""
    name: Optional[str] = None
    description: Optional[str] = None
    repository_url: Optional[str] = None
    language: Optional[str] = None
    status: Optional[str] = None


class ProjectResponse(BaseModel):
    """Project response schema"""
    id: int
    name: str
    description: Optional[str] = None
    repository_url: Optional[str] = None
    language: Optional[str] = None
    status: str
    owner_id: int
    owner_username: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProjectList(BaseModel):
    """Project list response schema"""
    projects: List[ProjectResponse]
    total: int
    page: int
    size: int
