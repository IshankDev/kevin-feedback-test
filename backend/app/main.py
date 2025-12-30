"""Main FastAPI application."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from .config import settings
from .core.logging_config import setup_logging
from .core.middleware import LoggingMiddleware
from .core.errors import (
    not_found_handler,
    ai_service_error_handler,
    database_error_handler,
    validation_error_handler,
    sqlalchemy_error_handler,
    generic_exception_handler
)
from .core.exceptions import FeedbackNotFoundError, AIServiceError, DatabaseError
from .api.routes import router
from .database import engine, Base
from sqlalchemy.exc import SQLAlchemyError


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    setup_logging(debug=settings.debug)
    logger = __import__("logging").getLogger(__name__)
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")


app = FastAPI(
    title=settings.app_name,
    description="API for exploring and summarizing customer feedback using AI",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Add middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time"],
)

# Register error handlers
app.add_exception_handler(FeedbackNotFoundError, not_found_handler)
app.add_exception_handler(AIServiceError, ai_service_error_handler)
app.add_exception_handler(DatabaseError, database_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include routers
app.include_router(router, prefix=settings.api_prefix)


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint."""
    return {
        "message": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }


@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": settings.app_name}

