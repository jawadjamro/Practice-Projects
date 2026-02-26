"""
FastAPI application entry point.
Main application configuration and startup.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import API_PREFIX, ALLOWED_ORIGINS, GENERATED_DIR, DEBUG
from app.routers import resume_router


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    application = FastAPI(
        title="AI Resume Builder API",
        description="""
## AI Resume Builder Backend API

This API provides intelligent resume generation and optimization services.

### Features:
- **AI-Powered Optimization**: Uses OpenAI/Claude to optimize resume content
- **ATS-Friendly**: Optimizes for Applicant Tracking Systems
- **Multiple Templates**: Support for different resume styles
- **PDF Generation**: High-quality PDF output using WeasyPrint
- **Secure**: Input validation, CORS protection, and secure file handling

### Quick Start:
1. Send POST request to `/api/resume/generate-resume` with resume data
2. Receive optimized content, HTML, and PDF download URL
3. Download PDF using the provided URL

### Authentication:
Currently no authentication required. Add API key validation for production use.
        """,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Configure CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount static files for PDF downloads
    application.mount(
        "/generated",
        StaticFiles(directory=str(GENERATED_DIR)),
        name="generated",
    )

    # Include routers
    application.include_router(resume_router, prefix=API_PREFIX)

    # Health check at root
    @application.get("/", tags=["Root"])
    async def root():
        """Root endpoint with API information."""
        return {
            "name": "AI Resume Builder API",
            "version": "1.0.0",
            "status": "running",
            "docs": "/docs",
        }

    # Startup event
    @application.on_event("startup")
    async def startup_event():
        """Execute on application startup."""
        # Ensure generated directory exists
        GENERATED_DIR.mkdir(parents=True, exist_ok=True)
        if DEBUG:
            print("Application started successfully")

    # Shutdown event
    @application.on_event("shutdown")
    async def shutdown_event():
        """Execute on application shutdown."""
        if DEBUG:
            print("Application shutting down")

    return application


# Create application instance
app = create_application()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        port=8000,
        reload=DEBUG,
    )
