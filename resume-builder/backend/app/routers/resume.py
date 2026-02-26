"""
Resume API router.
Defines endpoints for resume generation and management.
"""

import logging

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.models import PersonalInfoModel
from app.schemas import (
    ResumeRequest,
    ResumeResponse,
    OptimizedExperienceItem,
    OptimizedEducationItem,
    ErrorResponse,
)
from app.services.resume_builder import ResumeBuilder
from app.services.pdf_service import PDFService, PDFServiceError

logger = logging.getLogger(__name__)

# Create router with prefix
router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post(
    "/generate-resume",
    response_model=ResumeResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request data"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Generate Resume",
    description="Generate a resume with HTML and PDF outputs.",
)
async def generate_resume(request: ResumeRequest) -> ResumeResponse:
    """
    Generate a resume based on user input.

    This endpoint:
    1. Generates a professional HTML resume from user data
    2. Creates a downloadable PDF version

    Args:
        request: ResumeRequest containing personal info, summary, experience, education,
                 skills, and optional job description.

    Returns:
        ResumeResponse with resume content, HTML, and PDF download URL.

    Raises:
        HTTPException: 400 for validation errors, 500 for service errors.
    """
    try:
        # Initialize services
        resume_builder = ResumeBuilder()
        pdf_service = PDFService()

        # Convert personal info to model
        personal_info = PersonalInfoModel(
            full_name=request.personal_info.full_name,
            email=request.personal_info.email,
            phone=request.personal_info.phone,
            location=request.personal_info.location,
            linkedin=request.personal_info.linkedin,
            portfolio=request.personal_info.portfolio,
        )

        # Generate HTML resume directly from user input
        try:
            html_content = resume_builder.build_resume_from_request(
                personal_info=personal_info,
                summary=request.summary,
                experience=request.experience,
                education=request.education,
                skills=request.skills,
                template=request.template,
            )
        except Exception as e:
            logger.exception("HTML generation failed: %s", str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"HTML generation failed: {str(e)}",
            )

        # Generate PDF
        try:
            pdf_filename, pdf_path = pdf_service.generate_pdf(
                html_content=html_content,
                candidate_name=personal_info.full_name,
            )
        except PDFServiceError as e:
            logger.exception("PDF generation failed: %s", str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"PDF generation failed: {str(e)}",
            )

        # Build experience items with achievements
        optimized_experience_items = [
            OptimizedExperienceItem(
                company=exp.company,
                role=exp.role,
                start_date=exp.start_date,
                end_date=exp.end_date,
                responsibilities=exp.responsibilities,
                achievements=[],
            )
            for exp in request.experience
        ]

        # Build education items
        optimized_education_items = [
            OptimizedEducationItem(
                degree=edu.degree,
                institution=edu.institution,
                year=edu.year,
            )
            for edu in request.education
        ]

        response = ResumeResponse(
            optimized_summary=request.summary,
            optimized_experience=optimized_experience_items,
            optimized_education=optimized_education_items,
            optimized_skills=request.skills,
            resume_html=html_content,
            pdf_download_url=pdf_service.get_download_url(pdf_filename),
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error in generate_resume: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )


@router.get(
    "/download/{filename}",
    summary="Download Resume PDF",
    description="Download a generated resume PDF file.",
)
async def download_resume_pdf(filename: str):
    """
    Download a generated resume PDF.

    Args:
        filename: The PDF filename to download.

    Returns:
        FileResponse with the PDF file.

    Raises:
        HTTPException: 404 if file not found, 400 if invalid filename.
    """
    # Validate filename to prevent path traversal
    if not filename or ".." in filename or filename.startswith("/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid filename",
        )

    if not filename.endswith(".pdf"):
        filename = f"{filename}.pdf"

    pdf_service = PDFService()
    file_path = pdf_service.get_file_path(filename)

    if not pdf_service.file_exists(filename):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File not found: {filename}",
        )

    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Cache-Control": "no-cache",
        },
    )


@router.get(
    "/health",
    summary="Health Check",
    description="Check if the resume service is operational.",
)
async def health_check():
    """
    Health check endpoint.

    Returns:
        Simple status response.
    """
    return {
        "status": "healthy",
        "service": "resume-builder",
    }
