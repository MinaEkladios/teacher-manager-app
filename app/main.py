"""
TeacherManager FastAPI Application.

Main entry point for the FastAPI application.
Create the app factory and define lifecycle events.
"""

from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings


def init_sentry() -> None:
    """Initialize Sentry APM if configured."""
    if settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            traces_sample_rate=settings.sentry_traces_sample_rate,
            environment=settings.app_env,
        )
        print(f"Sentry initialized: {settings.app_env} environment")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifecycle: startup and shutdown."""
    # Startup
    print(f"Starting {settings.app_name} (env={settings.app_env})")
    yield
    # Shutdown
    print(f"Shutting down {settings.app_name}")


def create_app() -> FastAPI:
    """Create and configure FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    # Initialize APM
    init_sentry()

    # Create app
    app = FastAPI(
        title=settings.app_name,
        description="A PWA web application for managing classroom attendance, "
        "student profiles, schedules, resources, alerts, reporting, and analytics.",
        version="0.1.0",
        debug=settings.debug,
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "ok",
            "app": settings.app_name,
            "environment": settings.app_env,
        }

    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint."""
        return {
            "message": f"Welcome to {settings.app_name}",
            "docs": "/docs",
            "openapi": "/openapi.json",
        }

    return app


# Create the app instance
app = create_app()
