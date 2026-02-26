"""
Pydantic schemas for request/response validation.
"""

from typing import Optional
from pydantic import BaseModel, Field, EmailStr


# =============================================================================
# Input Schemas
# =============================================================================


class PersonalInfo(BaseModel):
    """Personal information section of the resume."""

    full_name: str = Field(..., min_length=1, description="Full name of the candidate")
    email: EmailStr = Field(..., description="Email address")
    phone: str = Field(..., description="Phone number")
    location: str = Field(..., description="City, State/Country")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    portfolio: Optional[str] = Field(None, description="Portfolio or personal website URL")


class ExperienceItem(BaseModel):
    """Work experience entry."""

    company: str = Field(..., min_length=1, description="Company name")
    role: str = Field(..., min_length=1, description="Job title/role")
    start_date: str = Field(..., description="Start date (e.g., 'Jan 2020' or '2020-01')")
    end_date: str = Field(..., description="End date or 'Present'")
    responsibilities: str = Field(..., description="Job responsibilities and achievements")


class EducationItem(BaseModel):
    """Education entry."""

    degree: str = Field(..., min_length=1, description="Degree or certification")
    institution: str = Field(..., min_length=1, description="Institution name")
    year: str = Field(..., description="Graduation year or date range")


class ResumeRequest(BaseModel):
    """Complete resume generation request."""

    personal_info: PersonalInfo = Field(..., description="Personal information")
    summary: str = Field(..., description="Professional summary")
    skills: list[str] = Field(default_factory=list, description="List of skills")
    experience: list[ExperienceItem] = Field(
        default_factory=list, description="Work experience"
    )
    education: list[EducationItem] = Field(
        default_factory=list, description="Education history"
    )
    job_description: str = Field(
        "", description="Target job description for optimization"
    )
    template: str = Field(default="modern", description="Resume template style")


# =============================================================================
# Output Schemas
# =============================================================================


class OptimizedExperienceItem(BaseModel):
    """Optimized work experience entry."""

    company: str
    role: str
    start_date: str
    end_date: str
    responsibilities: str
    achievements: list[str] = Field(
        default_factory=list, description="Key achievements with metrics"
    )


class OptimizedEducationItem(BaseModel):
    """Optimized education entry."""

    degree: str
    institution: str
    year: str


class ResumeResponse(BaseModel):
    """Resume generation response."""

    optimized_summary: str = Field(..., description="AI-optimized professional summary")
    optimized_experience: list[OptimizedExperienceItem] = Field(
        ..., description="Optimized work experience"
    )
    optimized_education: list[OptimizedEducationItem] = Field(
        ..., description="Optimized education"
    )
    optimized_skills: list[str] = Field(..., description="Optimized skills list")
    resume_html: str = Field(..., description="HTML formatted resume")
    pdf_download_url: str = Field(..., description="URL to download PDF")


class ErrorResponse(BaseModel):
    """Error response schema."""

    detail: str = Field(..., description="Error message")
