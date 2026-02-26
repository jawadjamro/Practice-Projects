"""
Resume Builder Service.
Generates clean, professional HTML resumes from user data.
"""

from typing import Optional

from app.models import OptimizedResumeData, PersonalInfoModel
from app.schemas import ExperienceItem, EducationItem


class ResumeBuilder:
    """
    Builds HTML resumes from resume data.
    Supports multiple templates with inline CSS for PDF generation.
    """

    # Template configurations
    TEMPLATES = {
        "modern": {
            "primary_color": "#2563eb",
            "secondary_color": "#64748b",
            "font_family": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
            "section_spacing": "24px",
        },
        "classic": {
            "primary_color": "#1f2937",
            "secondary_color": "#4b5563",
            "font_family": "Georgia, 'Times New Roman', serif",
            "section_spacing": "20px",
        },
        "minimal": {
            "primary_color": "#000000",
            "secondary_color": "#666666",
            "font_family": "'Helvetica Neue', Helvetica, Arial, sans-serif",
            "section_spacing": "16px",
        },
    }

    def build_resume_from_request(
        self,
        personal_info: PersonalInfoModel,
        summary: str,
        skills: list[str],
        experience: list[ExperienceItem],
        education: list[EducationItem],
        template: str = "modern",
    ) -> str:
        """
        Build a complete HTML resume from request data.

        Args:
            personal_info: Personal information.
            summary: Professional summary.
            skills: List of skills.
            experience: Work experience list.
            education: Education list.
            template: Template style name.

        Returns:
            Complete HTML string.
        """
        template_config = self.TEMPLATES.get(template, self.TEMPLATES["modern"])

        html = self._generate_html_from_request(
            personal_info=personal_info,
            summary=summary,
            skills=skills,
            experience=experience,
            education=education,
            config=template_config,
        )

        return html

    def build_resume(
        self,
        personal_info: PersonalInfoModel,
        optimized_data: OptimizedResumeData,
        template: str = "modern",
    ) -> str:
        """
        Build a complete HTML resume.

        Args:
            personal_info: Personal information.
            optimized_data: AI-optimized resume data.
            template: Template style name.

        Returns:
            Complete HTML string.
        """
        template_config = self.TEMPLATES.get(template, self.TEMPLATES["modern"])

        html = self._generate_html(
            personal_info=personal_info,
            optimized_data=optimized_data,
            config=template_config,
        )

        return html

    def _generate_html_from_request(
        self,
        personal_info: PersonalInfoModel,
        summary: str,
        skills: list[str],
        experience: list[ExperienceItem],
        education: list[EducationItem],
        config: dict,
    ) -> str:
        """
        Generate HTML content with inline styles from request data.

        Args:
            personal_info: Personal information.
            summary: Professional summary.
            skills: List of skills.
            experience: Work experience list.
            education: Education list.
            config: Template configuration.

        Returns:
            HTML string.
        """
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{personal_info.full_name} - Resume</title>
</head>
<body style="margin: 0; padding: 40px; background-color: #ffffff; font-family: {config['font_family']}; color: #1f2937; line-height: 1.6;">
    <div style="max-width: 800px; margin: 0 auto;">
        {self._build_header(personal_info, config)}
        {self._build_summary(summary, config)}
        {self._build_skills_section(skills, config)}
        {self._build_experience_section_from_request(experience, config)}
        {self._build_education_section_from_request(education, config)}
    </div>
</body>
</html>"""

        return html

    def _generate_html(
        self,
        personal_info: PersonalInfoModel,
        optimized_data: OptimizedResumeData,
        config: dict,
    ) -> str:
        """
        Generate HTML content with inline styles.

        Args:
            personal_info: Personal information.
            optimized_data: Optimized resume data.
            config: Template configuration.

        Returns:
            HTML string.
        """
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{personal_info.full_name} - Resume</title>
</head>
<body style="margin: 0; padding: 40px; background-color: #ffffff; font-family: {config['font_family']}; color: #1f2937; line-height: 1.6;">
    <div style="max-width: 800px; margin: 0 auto;">
        {self._build_header(personal_info, config)}
        {self._build_summary(optimized_data.summary, config)}
        {self._build_skills_section(optimized_data.skills, config)}
        {self._build_experience_section(optimized_data.experience, config)}
        {self._build_education_section(optimized_data.education, config)}
    </div>
</body>
</html>"""

        return html

    def _build_header(
        self, personal_info: PersonalInfoModel, config: dict
    ) -> str:
        """Build the header section with name and contact info."""
        contact_items = []

        # Email
        contact_items.append(
            f'<span style="color: {config["secondary_color"]};">📧 {personal_info.email}</span>'
        )

        # Phone
        contact_items.append(
            f'<span style="color: {config["secondary_color"]};">📱 {personal_info.phone}</span>'
        )

        # Location
        contact_items.append(
            f'<span style="color: {config["secondary_color"]};">📍 {personal_info.location}</span>'
        )

        # LinkedIn (optional)
        if personal_info.linkedin:
            contact_items.append(
                f'<span style="color: {config["secondary_color"]};">💼 {personal_info.linkedin}</span>'
            )

        # Portfolio (optional)
        if personal_info.portfolio:
            contact_items.append(
                f'<span style="color: {config["secondary_color"]};">🌐 {personal_info.portfolio}</span>'
            )

        contact_html = " &nbsp;|&nbsp; ".join(contact_items)

        return f"""
        <!-- Header Section -->
        <header style="text-align: center; margin-bottom: {config['section_spacing']}; padding-bottom: 24px; border-bottom: 2px solid {config['primary_color']};">
            <h1 style="margin: 0 0 12px 0; font-size: 32px; font-weight: 700; color: {config['primary_color']}; letter-spacing: -0.5px;">
                {personal_info.full_name}
            </h1>
            <div style="font-size: 14px; color: {config['secondary_color']};">
                {contact_html}
            </div>
        </header>
        """

    def _build_summary(self, summary: str, config: dict) -> str:
        """Build the professional summary section."""
        return f"""
        <!-- Summary Section -->
        <section style="margin-bottom: {config['section_spacing']};">
            <h2 style="font-size: 18px; font-weight: 600; color: {config['primary_color']}; margin: 0 0 12px 0; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #e5e7eb; padding-bottom: 8px;">
                Professional Summary
            </h2>
            <p style="margin: 0; color: #374151; font-size: 14px; text-align: justify;">
                {summary}
            </p>
        </section>
        """

    def _build_skills_section(self, skills: list[str], config: dict) -> str:
        """Build the skills section."""
        if not skills:
            return ""

        # Group skills (first 6 as primary, rest as secondary if many skills)
        skills_html = ""
        for skill in skills:
            skills_html += f"""
            <span style="display: inline-block; background-color: #f3f4f6; color: #374151; padding: 6px 14px; margin: 4px; border-radius: 4px; font-size: 13px; font-weight: 500;">
                {skill}
            </span>"""

        return f"""
        <!-- Skills Section -->
        <section style="margin-bottom: {config['section_spacing']};">
            <h2 style="font-size: 18px; font-weight: 600; color: {config['primary_color']}; margin: 0 0 12px 0; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #e5e7eb; padding-bottom: 8px;">
                Skills
            </h2>
            <div style="line-height: 2;">
                {skills_html}
            </div>
        </section>
        """

    def _build_experience_section(
        self, experience: list, config: dict
    ) -> str:
        """Build the work experience section."""
        if not experience:
            return ""

        experience_html = ""
        for exp in experience:
            # Build achievements list
            achievements_html = ""

            # Parse responsibilities for bullet points
            responsibilities = exp.responsibilities
            bullet_points = []

            # Check if responsibilities already has bullet points
            if "•" in responsibilities or "-" in responsibilities:
                lines = responsibilities.split("\n")
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith(("•", "-")):
                        # This might be a header, add as is
                        if line.endswith(":"):
                            bullet_points.append(
                                f'<strong>{line}</strong>'
                            )
                        else:
                            bullet_points.append(line)
                    elif line:
                        # Clean up bullet point
                        cleaned = line.lstrip("•-").strip()
                        if cleaned:
                            bullet_points.append(cleaned)
            else:
                # Treat as paragraph, split by sentences
                bullet_points = [responsibilities]

            # Add explicit achievements
            if exp.achievements:
                for achievement in exp.achievements:
                    if achievement not in bullet_points:
                        bullet_points.insert(0, achievement)

            # Build bullet points HTML
            for point in bullet_points:
                if point.strip():
                    achievements_html += f"""
                    <li style="margin-bottom: 6px; color: #374151; font-size: 14px;">
                        {point.strip()}
                    </li>"""

            experience_html += f"""
            <!-- Experience Item -->
            <div style="margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
                    <h3 style="font-size: 16px; font-weight: 600; color: #1f2937; margin: 0;">
                        {exp.role}
                    </h3>
                    <span style="font-size: 13px; color: {config['secondary_color']}; font-weight: 500;">
                        {exp.start_date} – {exp.end_date}
                    </span>
                </div>
                <div style="font-size: 14px; font-weight: 600; color: {config['primary_color']}; margin-bottom: 8px;">
                    {exp.company}
                </div>
                <ul style="margin: 0; padding-left: 20px;">
                    {achievements_html}
                </ul>
            </div>
            """

        return f"""
        <!-- Experience Section -->
        <section style="margin-bottom: {config['section_spacing']};">
            <h2 style="font-size: 18px; font-weight: 600; color: {config['primary_color']}; margin: 0 0 16px 0; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #e5e7eb; padding-bottom: 8px;">
                Work Experience
            </h2>
            {experience_html}
        </section>
        """

    def _build_experience_section_from_request(
        self, experience: list, config: dict
    ) -> str:
        """Build the work experience section from request data."""
        if not experience:
            return ""

        experience_html = ""
        for exp in experience:
            # Parse responsibilities for bullet points
            responsibilities = exp.responsibilities
            bullet_points = []

            # Check if responsibilities already has bullet points
            if "•" in responsibilities or "-" in responsibilities:
                lines = responsibilities.split("\n")
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith(("•", "-")):
                        if line.endswith(":"):
                            bullet_points.append(f'<strong>{line}</strong>')
                        else:
                            bullet_points.append(line)
                    elif line:
                        cleaned = line.lstrip("•-").strip()
                        if cleaned:
                            bullet_points.append(cleaned)
            else:
                bullet_points = [responsibilities]

            # Build bullet points HTML
            achievements_html = ""
            for point in bullet_points:
                if point.strip():
                    achievements_html += f"""
                    <li style="margin-bottom: 6px; color: #374151; font-size: 14px;">
                        {point.strip()}
                    </li>"""

            experience_html += f"""
            <!-- Experience Item -->
            <div style="margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
                    <h3 style="font-size: 16px; font-weight: 600; color: #1f2937; margin: 0;">
                        {exp.role}
                    </h3>
                    <span style="font-size: 13px; color: {config['secondary_color']}; font-weight: 500;">
                        {exp.start_date} – {exp.end_date}
                    </span>
                </div>
                <div style="font-size: 14px; font-weight: 600; color: {config['primary_color']}; margin-bottom: 8px;">
                    {exp.company}
                </div>
                <ul style="margin: 0; padding-left: 20px;">
                    {achievements_html}
                </ul>
            </div>
            """

        return f"""
        <!-- Experience Section -->
        <section style="margin-bottom: {config['section_spacing']};">
            <h2 style="font-size: 18px; font-weight: 600; color: {config['primary_color']}; margin: 0 0 16px 0; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #e5e7eb; padding-bottom: 8px;">
                Work Experience
            </h2>
            {experience_html}
        </section>
        """

    def _build_education_section(
        self, education: list, config: dict
    ) -> str:
        """Build the education section."""
        if not education:
            return ""

        education_html = ""
        for edu in education:
            education_html += f"""
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                    <div>
                        <span style="font-size: 15px; font-weight: 600; color: #1f2937;">
                            {edu.degree}
                        </span>
                        <span style="color: {config['secondary_color']}; font-size: 14px; margin-left: 8px;">
                            | {edu.institution}
                        </span>
                    </div>
                    <span style="font-size: 13px; color: {config['secondary_color']}; font-weight: 500;">
                        {edu.year}
                    </span>
                </div>
            </div>
            """

        return f"""
        <!-- Education Section -->
        <section style="margin-bottom: {config['section_spacing']};">
            <h2 style="font-size: 18px; font-weight: 600; color: {config['primary_color']}; margin: 0 0 12px 0; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #e5e7eb; padding-bottom: 8px;">
                Education
            </h2>
            {education_html}
        </section>
        """

    def _build_education_section_from_request(
        self, education: list, config: dict
    ) -> str:
        """Build the education section from request data."""
        if not education:
            return ""

        education_html = ""
        for edu in education:
            education_html += f"""
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                    <div>
                        <span style="font-size: 15px; font-weight: 600; color: #1f2937;">
                            {edu.degree}
                        </span>
                        <span style="color: {config['secondary_color']}; font-size: 14px; margin-left: 8px;">
                            | {edu.institution}
                        </span>
                    </div>
                    <span style="font-size: 13px; color: {config['secondary_color']}; font-weight: 500;">
                        {edu.year}
                    </span>
                </div>
            </div>
            """

        return f"""
        <!-- Education Section -->
        <section style="margin-bottom: {config['section_spacing']};">
            <h2 style="font-size: 18px; font-weight: 600; color: {config['primary_color']}; margin: 0 0 12px 0; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #e5e7eb; padding-bottom: 8px;">
                Education
            </h2>
            {education_html}
        </section>
        """


# Convenience function for direct use
def generate_resume_html(
    personal_info: PersonalInfoModel,
    optimized_data: OptimizedResumeData,
    template: str = "modern",
) -> str:
    """
    Generate HTML resume from optimized data.

    Args:
        personal_info: Personal information.
        optimized_data: Optimized resume data.
        template: Template style name.

    Returns:
        Complete HTML string.
    """
    builder = ResumeBuilder()
    return builder.build_resume(personal_info, optimized_data, template)
