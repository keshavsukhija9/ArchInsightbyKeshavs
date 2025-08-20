"""
Health check endpoints
"""

from fastapi import APIRouter, status
from app.core.database import get_db_health
from app.core.config import settings

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }


@router.get("/detailed", status_code=status.HTTP_200_OK)
async def detailed_health_check():
    """Detailed health check including database connections"""
    db_health = await get_db_health()
    
    overall_status = "healthy" if db_health["overall"] else "unhealthy"
    status_code = status.HTTP_200_OK if db_health["overall"] else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return {
        "status": overall_status,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "databases": db_health,
        "services": {
            "api": "healthy",
            "postgres": "healthy" if db_health["postgres"] else "unhealthy",
            "neo4j": "healthy" if db_health["neo4j"] else "unhealthy",
            "redis": "healthy" if db_health["redis"] else "unhealthy",
        }
    }