"""
Code analysis endpoints
"""

import logging
import asyncio
from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from fastapi.responses import StreamingResponse

from app.core.database import get_postgres_session
from app.models.user import User
from app.models.project import Project
from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisCreate, AnalysisResponse, AnalysisList
from app.services.auth import get_current_active_user
from app.services.code_analyzer import CodeAnalyzer

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def create_analysis(
    analysis_data: AnalysisCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_postgres_session)
):
    """Create a new code analysis"""
    # Verify project exists and user has access
    stmt = select(Project).where(
        Project.id == analysis_data.project_id,
        Project.owner_id == current_user.id
    )
    result = await session.execute(stmt)
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check if project has code files
    # TODO: Implement code file checking
    
    # Create analysis record
    new_analysis = Analysis(
        project_id=analysis_data.project_id,
        analysis_type=analysis_data.analysis_type,
        status="pending",
        progress=0,
        options=analysis_data.options or {}
    )
    
    session.add(new_analysis)
    await session.commit()
    await session.refresh(new_analysis)
    
    # Start analysis in background
    background_tasks.add_task(
        run_analysis,
        analysis_id=new_analysis.id,
        project_id=analysis_data.project_id,
        analysis_type=analysis_data.analysis_type,
        options=analysis_data.options or {}
    )
    
    logger.info(f"Analysis created: {new_analysis.id} for project {project.name}")
    
    return AnalysisResponse(
        id=new_analysis.id,
        project_id=new_analysis.project_id,
        project_name=project.name,
        analysis_type=new_analysis.analysis_type,
        status=new_analysis.status,
        progress=new_analysis.progress,
        results=new_analysis.results,
        error_message=new_analysis.error_message,
        started_at=new_analysis.started_at,
        completed_at=new_analysis.completed_at,
        created_at=new_analysis.created_at
    )


@router.get("/", response_model=AnalysisList)
async def get_analyses(
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_postgres_session),
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size")
):
    """Get user's analyses with filtering and pagination"""
    # Build base query - get analyses for user's projects
    project_subquery = select(Project.id).where(Project.owner_id == current_user.id)
    
    query = select(Analysis).join(Project).where(
        Analysis.project_id.in_(project_subquery)
    )
    
    # Apply filters
    if project_id:
        query = query.where(Analysis.project_id == project_id)
    
    if status:
        query = query.where(Analysis.status == status)
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await session.execute(count_query)
    total = total_result.scalar()
    
    # Get paginated results
    query = query.order_by(Analysis.created_at.desc()).offset((page - 1) * size).limit(size)
    result = await session.execute(query)
    analyses = result.scalars().all()
    
    # Convert to response format
    analysis_responses = []
    for analysis in analyses:
        analysis_responses.append(AnalysisResponse(
            id=analysis.id,
            project_id=analysis.project_id,
            project_name=analysis.project.name,
            analysis_type=analysis.analysis_type,
            status=analysis.status,
            progress=analysis.progress,
            results=analysis.results,
            error_message=analysis.error_message,
            started_at=analysis.started_at,
            completed_at=analysis.completed_at,
            created_at=analysis.created_at
        ))
    
    return AnalysisList(
        analyses=analysis_responses,
        total=total,
        page=page,
        size=size
    )


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_postgres_session)
):
    """Get a specific analysis"""
    # Get analysis with project info
    stmt = select(Analysis).join(Project).where(
        Analysis.id == analysis_id,
        Project.owner_id == current_user.id
    )
    result = await session.execute(stmt)
    analysis = result.scalar_one_or_none()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    return AnalysisResponse(
        id=analysis.id,
        project_id=analysis.project_id,
        project_name=analysis.project.name,
        analysis_type=analysis.analysis_type,
        status=analysis.status,
        progress=analysis.progress,
        results=analysis.results,
        error_message=analysis.error_message,
        started_at=analysis.started_at,
        completed_at=analysis.completed_at,
        created_at=analysis.created_at
    )


@router.get("/{analysis_id}/progress")
async def get_analysis_progress(
    analysis_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_postgres_session)
):
    """Get real-time analysis progress (SSE)"""
    # Verify access
    stmt = select(Analysis).join(Project).where(
        Analysis.id == analysis_id,
        Project.owner_id == current_user.id
    )
    result = await session.execute(stmt)
    analysis = result.scalar_one_or_none()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    async def progress_stream():
        """Stream progress updates"""
        while analysis.status in ["pending", "running"]:
            # Get latest progress
            await session.refresh(analysis)
            
            data = {
                "id": analysis.id,
                "status": analysis.status,
                "progress": analysis.progress,
                "error_message": analysis.error_message
            }
            
            yield f"data: {data}\n\n"
            
            if analysis.status in ["completed", "failed"]:
                break
            
            await asyncio.sleep(2)  # Update every 2 seconds
    
    return StreamingResponse(
        progress_stream(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )


@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_postgres_session)
):
    """Cancel a running analysis"""
    stmt = select(Analysis).join(Project).where(
        Analysis.id == analysis_id,
        Project.owner_id == current_user.id
    )
    result = await session.execute(stmt)
    analysis = result.scalar_one_or_none()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    if analysis.status not in ["pending", "running"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only cancel pending or running analyses"
        )
    
    # Cancel analysis
    analysis.status = "cancelled"
    await session.commit()
    
    logger.info(f"Analysis cancelled: {analysis_id} by user {current_user.username}")


async def run_analysis(
    analysis_id: int,
    project_id: int,
    analysis_type: str,
    options: dict
):
    """Background task to run code analysis"""
    # This would be implemented in a separate worker process in production
    # For now, we'll simulate the analysis process
    
    logger.info(f"Starting analysis {analysis_id} for project {project_id}")
    
    # TODO: Implement actual code analysis using CodeAnalyzer service
    # This is a placeholder implementation
    
    await asyncio.sleep(5)  # Simulate analysis time
    
    logger.info(f"Analysis {analysis_id} completed")