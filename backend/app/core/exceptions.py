"""
Custom exceptions for ArchInsight application
"""

from typing import Any, Dict, Optional


class AppException(Exception):
    """Base application exception"""
    
    def __init__(
        self,
        message: str,
        error_code: str = "app_error",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(AppException):
    """Validation error exception"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="validation_error",
            status_code=422,
            details=details,
        )


class AuthenticationError(AppException):
    """Authentication error exception"""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            error_code="authentication_error",
            status_code=401,
        )


class AuthorizationError(AppException):
    """Authorization error exception"""
    
    def __init__(self, message: str = "Access denied"):
        super().__init__(
            message=message,
            error_code="authorization_error",
            status_code=403,
        )


class NotFoundError(AppException):
    """Resource not found exception"""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            message=message,
            error_code="not_found",
            status_code=404,
        )


class ConflictError(AppException):
    """Resource conflict exception"""
    
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(
            message=message,
            error_code="conflict",
            status_code=409,
        )


class DatabaseError(AppException):
    """Database operation error"""
    
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(
            message=message,
            error_code="database_error",
            status_code=500,
        )


class ExternalServiceError(AppException):
    """External service error"""
    
    def __init__(self, message: str = "External service error", service: str = "unknown"):
        super().__init__(
            message=message,
            error_code="external_service_error",
            status_code=502,
            details={"service": service},
        )


class RateLimitError(AppException):
    """Rate limit exceeded exception"""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(
            message=message,
            error_code="rate_limit_exceeded",
            status_code=429,
        )


class FileUploadError(AppException):
    """File upload error exception"""
    
    def __init__(self, message: str = "File upload failed"):
        super().__init__(
            message=message,
            error_code="file_upload_error",
            status_code=400,
        )


class CodeAnalysisError(AppException):
    """Code analysis error exception"""
    
    def __init__(self, message: str = "Code analysis failed"):
        super().__init__(
            message=message,
            error_code="code_analysis_error",
            status_code=422,
        )


class MLModelError(AppException):
    """ML model error exception"""
    
    def __init__(self, message: str = "ML model operation failed"):
        super().__init__(
            message=message,
            error_code="ml_model_error",
            status_code=500,
        )