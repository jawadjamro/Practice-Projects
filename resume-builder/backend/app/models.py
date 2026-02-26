"""
Data models for internal use.
These are used for data transformation between layers.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PersonalInfoModel:
    """Personal information data model."""

    full_name: str
    email: str
    phone: str
    location: str
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None


@dataclass
class ExperienceModel:
    """Work experience data model."""

    company: str
    role: str
    start_date: str
    end_date: str
    responsibilities: str
    achievements: list[str] = field(default_factory=list)


@dataclass
class EducationModel:
    """Education data model."""

    degree: str
    institution: str
    year: str


@dataclass
class OptimizedResumeData:
    """Optimized resume data returned from AI service."""

    summary: str
    experience: list[ExperienceModel]
    education: list[EducationModel]
    skills: list[str]
    ats_keywords: list[str] = field(default_factory=list)


@dataclass
class GeneratedResume:
    """Complete generated resume with all outputs."""

    optimized_summary: str
    optimized_experience: list[ExperienceModel]
    optimized_education: list[EducationModel]
    optimized_skills: list[str]
    html_content: str
    pdf_path: str
    pdf_filename: str
