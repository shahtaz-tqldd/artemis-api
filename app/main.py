from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.db.session import init_db, close_db
from app.middleware.error_handlers import (
    api_error_handler,
    http_error_handler,
    http422_error_handler,
    unhandled_exception_handler,
)
from app.core.exceptions import APIError
from app.api.router import api_router
from app.middleware import register_middlewares

# Initialize logger
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting up application...")
    await init_db()
    logger.info("Database initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    await close_db()
    logger.info("Application shutdown complete")


def create_application() -> FastAPI:
    """Application factory pattern"""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description=f"{settings.app_name} API",
        debug=settings.debug,
        openapi_url=f"{settings.api_v1_prefix}/openapi.json" if settings.debug else None,
        docs_url=f"{settings.api_v1_prefix}/docs" if settings.debug else None,
        redoc_url=f"{settings.api_v1_prefix}/redoc" if settings.debug else None,
        lifespan=lifespan,
    )
    
    # Register middlewares
    register_middlewares(app)
    
    # Register exception handlers
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)
    app.add_exception_handler(APIError, api_error_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
    
    # Include API router
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    
    logger.info(f"Application initialized in {settings.app_env} mode")
    
    return app


app = create_application()
