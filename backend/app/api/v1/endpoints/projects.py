"""
Project management endpoints
"""

import logging
from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder

from app.core.database import get_postgres_session
from app.models.user import User
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectList
from app.services.auth import get_current_active_user

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_postgres_session)
):
    """Create a new project"""
    # Check if project name already exists for this user
    stmt = select(Project).where(
        Project.name == project_data.name,
        Project.owner_id == current_user.id
    )
    result = await session.execute(stmt)
    existing_project = result.scalar_one_or_none()
    
    if existing_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project with this name already exists"
        )
    
    # Create new project
    new_project = Project(
        name=project_data.name,
        description=project_data.description,
        repository_url=project_data.repository_url,
        language=project_data.language,
        owner_id=current_user.id,
        status="active"
    )
    
    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)
    
    logger.info(f"Project created: {new_project.name} by user {current_user.username}")
    
    return ProjectResponse(
        id=new_project.id,
        name=new_project.name,
        description=new_project.description,
        repository_url=new_project.repository_url,
        language=new_project.language,
        status=new_project.status,
        owner_id=new_project.owner_id,
        owner_username=current_user.username,
        created_at=new_project.created_at,
        updated_at=new_project.updated_at
    )


@router.get("/", response_model=ProjectList)
async def get_projects(
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_postgres_session),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    search: Optional[str] = Query(None, description="Search term")
):
    """Get user's projects with pagination and search"""
    # Build query
    query = select(Project).where(Project.owner_id == current_user.id)
    
    if search:
        query = query.where(
            Project.name.ilike(f"%{search}%") | 
            Project.description.ilike(f"%{search}%")
        )
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await session.execute(count_query)
    total = total_result.scalar()
    
    # Get paginated results
    query = query.offset((page - 1) * size).limit(size)
    result = await session.execute(query)
    projects = result.scalars().all()
    
    # Convert to response format
    project_responses = []
    for project in projects:
        project_responses.append(ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            repository_url=project.repository_url,
            language=project.language,
            status=project.status,
            owner_id=project.owner_id,
            owner_username=current_user.username,
            created_at=project.created_at,
            updated_at=project.updated_at
        ))
    
    return ProjectList(
        projects=project_responses,
        total=total,
        page=page,
        size=size
    )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_postgres_session)
):
    """Get a specific project"""
    stmt = select(Project).where(
        Project.id == project_id,
        Project.owner_id == current_user.id
    )
    result = await session.execute(stmt)
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        repository_url=project.repository_url,
        language=project.language,
        status=project.status,
        owner_id=project.owner_id,
        owner_username=current_user.username,
        created_at=project.created_at,
        updated_at=project.updated_at
    )


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_postgres_session)
):
    """Update a project"""
    stmt = select(Project).where(
        Project.id == project_id,
        Project.owner_id == current_user.id
    )
    result = await session.execute(stmt)
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Update project fields
    update_data = project_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    await session.commit()
    await session.refresh(project)
    
    logger.info(f"Project updated: {project.name} by user {current_user.username}")
    
    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        repository_url=project.repository_url,
        language=project.language,
        status=project.status,
        owner_id=project.owner_id,
        owner_username=current_user.username,
        created_at=project.created_at,
        updated_at=project.updated_at
    )


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_postgres_session)
):
    """Delete a project"""
    stmt = select(Project).where(
        Project.id == project_id,
        Project.owner_id == current_user.id
    )
    result = await session.execute(stmt)
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    await session.delete(project)
    await session.commit()
    
    logger.info(f"Project deleted: {project.name} by user {current_user.username}")