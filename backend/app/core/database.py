"""
Database configuration and connection management
"""

import asyncio
import logging
from typing import AsyncGenerator, Optional

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker
from neo4j import AsyncGraphDatabase, AsyncDriver
import redis.asyncio as redis

from app.core.config import settings

logger = logging.getLogger(__name__)

# SQLAlchemy setup
Base = declarative_base()
metadata = MetaData()

# Database engines
postgres_engine = None
async_postgres_engine = None
SessionLocal = None
AsyncSessionLocal = None

# Neo4j driver
neo4j_driver: Optional[AsyncDriver] = None

# Redis client
redis_client: Optional[redis.Redis] = None


async def init_db() -> None:
    """Initialize all database connections"""
    global postgres_engine, async_postgres_engine, SessionLocal, AsyncSessionLocal
    global neo4j_driver, redis_client
    
    try:
        # Initialize PostgreSQL
        logger.info("Initializing PostgreSQL connection...")
        
        # Convert sync URL to async URL
        async_database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        
        # Create async engine
        async_postgres_engine = create_async_engine(
            async_database_url,
            echo=settings.DEBUG,
            pool_pre_ping=True,
            pool_recycle=300,
        )
        
        # Create sync engine for migrations
        postgres_engine = create_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,
            pool_pre_ping=True,
            pool_recycle=300,
        )
        
        # Create session factories
        AsyncSessionLocal = async_sessionmaker(
            async_postgres_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=postgres_engine,
        )
        
        logger.info("PostgreSQL connection initialized successfully")
        
        # Initialize Neo4j
        logger.info("Initializing Neo4j connection...")
        neo4j_driver = AsyncGraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
            max_connection_lifetime=3600,
            max_connection_pool_size=50,
            connection_acquisition_timeout=60,
        )
        
        # Test Neo4j connection
        async with neo4j_driver.session() as session:
            result = await session.run("RETURN 1 as test")
            await result.single()
        
        logger.info("Neo4j connection initialized successfully")
        
        # Initialize Redis
        logger.info("Initializing Redis connection...")
        redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            max_connections=20,
        )
        
        # Test Redis connection
        await redis_client.ping()
        
        logger.info("Redis connection initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize databases: {e}")
        raise


async def close_db() -> None:
    """Close all database connections"""
    global postgres_engine, async_postgres_engine, neo4j_driver, redis_client
    
    try:
        if async_postgres_engine:
            await async_postgres_engine.dispose()
            logger.info("PostgreSQL async engine disposed")
        
        if postgres_engine:
            postgres_engine.dispose()
            logger.info("PostgreSQL sync engine disposed")
        
        if neo4j_driver:
            await neo4j_driver.close()
            logger.info("Neo4j driver closed")
        
        if redis_client:
            await redis_client.close()
            logger.info("Redis client closed")
            
    except Exception as e:
        logger.error(f"Error closing database connections: {e}")


async def get_postgres_session() -> AsyncGenerator[AsyncSession, None]:
    """Get PostgreSQL async session"""
    if not AsyncSessionLocal:
        raise RuntimeError("Database not initialized")
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_neo4j_session():
    """Get Neo4j session"""
    if not neo4j_driver:
        raise RuntimeError("Neo4j driver not initialized")
    
    return neo4j_driver.session()


async def get_redis_client() -> redis.Redis:
    """Get Redis client"""
    if not redis_client:
        raise RuntimeError("Redis client not initialized")
    
    return redis_client


# Health check functions
async def check_postgres_health() -> bool:
    """Check PostgreSQL connection health"""
    try:
        if not async_postgres_engine:
            return False
        
        async with async_postgres_engine.begin() as conn:
            await conn.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"PostgreSQL health check failed: {e}")
        return False


async def check_neo4j_health() -> bool:
    """Check Neo4j connection health"""
    try:
        if not neo4j_driver:
            return False
        
        async with neo4j_driver.session() as session:
            result = await session.run("RETURN 1 as test")
            await result.single()
        return True
    except Exception as e:
        logger.error(f"Neo4j health check failed: {e}")
        return False


async def check_redis_health() -> bool:
    """Check Redis connection health"""
    try:
        if not redis_client:
            return False
        
        await redis_client.ping()
        return True
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        return False


async def get_db_health() -> dict:
    """Get overall database health status"""
    postgres_healthy = await check_postgres_health()
    neo4j_healthy = await check_neo4j_health()
    redis_healthy = await check_redis_health()
    
    return {
        "postgres": postgres_healthy,
        "neo4j": neo4j_healthy,
        "redis": redis_healthy,
        "overall": postgres_healthy and neo4j_healthy and redis_healthy,
    }