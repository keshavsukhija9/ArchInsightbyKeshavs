"""
Application configuration settings
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "ArchInsight"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # Security
    JWT_SECRET_KEY: str = "dev_secret_key_change_in_production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    
    # Database URLs
    DATABASE_URL: str = "postgresql://archinsight:archinsight_dev_password@localhost:5432/archinsight"
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "archinsight_dev_password"
    REDIS_URL: str = "redis://localhost:6379"
    
    # External APIs
    OPENAI_API_KEY: Optional[str] = None
    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # File Upload
    MAX_UPLOAD_SIZE: str = "100MB"
    ALLOWED_EXTENSIONS: List[str] = [
        ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cpp", ".c", 
        ".h", ".hpp", ".cs", ".php", ".rb", ".go", ".rs", ".swift", ".kt"
    ]
    UPLOAD_DIR: str = "./uploads"
    CACHE_DIR: str = "./cache"
    
    # ML Model Settings
    MODEL_PATH: str = "./data/models"
    BATCH_SIZE: int = 32
    LEARNING_RATE: float = 0.001
    EPOCHS: int = 100
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    GITHUB_API_RATE_LIMIT: int = 5000
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    PROMETHEUS_PORT: int = 9090
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("ALLOWED_EXTENSIONS", pre=True)
    def assemble_allowed_extensions(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("MAX_UPLOAD_SIZE")
    def validate_upload_size(cls, v):
        """Convert upload size to bytes"""
        if isinstance(v, str):
            if v.upper().endswith("MB"):
                return int(v[:-2]) * 1024 * 1024
            elif v.upper().endswith("GB"):
                return int(v[:-2]) * 1024 * 1024 * 1024
            else:
                return int(v)
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()