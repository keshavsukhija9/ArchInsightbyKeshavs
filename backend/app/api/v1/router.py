"""
Main API v1 router
"""

from fastapi import APIRouter

from app.api.v1.endpoints import health, auth, projects, analysis, recommendations

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])