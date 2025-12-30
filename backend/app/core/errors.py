"""Error handlers and utilities."""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import logging

from .exceptions import FeedbackNotFoundError, AIServiceError, DatabaseError

logger = logging.getLogger(__name__)


async def not_found_handler(request: Request, exc: FeedbackNotFoundError):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc), "type": "not_found"}
    )


async def ai_service_error_handler(request: Request, exc: AIServiceError):
    """Handle AI service errors."""
    logger.error(f"AI Service Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "AI service temporarily unavailable", "type": "ai_service_error"}
    )


async def database_error_handler(request: Request, exc: DatabaseError):
    """Handle database errors."""
    logger.error(f"Database Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database operation failed", "type": "database_error"}
    )


async def validation_error_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "type": "validation_error"
        }
    )


async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """Handle SQLAlchemy errors."""
    logger.error(f"SQLAlchemy Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database error occurred", "type": "database_error"}
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions."""
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred", "type": "internal_error"}
    )

