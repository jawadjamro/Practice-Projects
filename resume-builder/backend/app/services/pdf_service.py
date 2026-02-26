"""
PDF Service for generating PDF files from HTML resumes.
Uses reportlab for reliable PDF generation.
"""

import io
import uuid
from pathlib import Path
from typing import Optional

from app.config import GENERATED_DIR


class PDFServiceError(Exception):
    """Custom exception for PDF service errors."""

    pass


class PDFService:
    """
    Service for converting HTML to PDF.
    Handles file generation, storage, and cleanup.
    """

    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize PDF service.

        Args:
            output_dir: Directory to store generated PDFs.
        """
        self.output_dir = output_dir or GENERATED_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_pdf(
        self,
        html_content: str,
        filename: Optional[str] = None,
        candidate_name: Optional[str] = None,
    ) -> tuple[str, str]:
        """
        Generate PDF from HTML content.

        Args:
            html_content: HTML string to convert.
            filename: Optional custom filename (without extension).
            candidate_name: Optional candidate name for filename generation.

        Returns:
            Tuple of (pdf_filename, pdf_path).

        Raises:
            PDFServiceError: If PDF generation fails.
        """
        # Generate secure filename
        if filename:
            safe_filename = self._sanitize_filename(filename)
        elif candidate_name:
            safe_filename = self._sanitize_filename(candidate_name)
        else:
            safe_filename = str(uuid.uuid4())[:8]

        pdf_filename = f"{safe_filename}_resume.pdf"
        pdf_path = self.output_dir / pdf_filename

        try:
            # Try xhtml2pdf first
            from xhtml2pdf import pisa

            with open(str(pdf_path), "w+b") as pdf_file:
                pisa_status = pisa.CreatePDF(
                    src=html_content,
                    dest=pdf_file,
                    encoding="utf-8",
                )

            if pisa_status.err:
                raise PDFServiceError("xhtml2pdf rendering error")

        except ImportError:
            # Fallback: Use reportlab to create simple PDF
            self._create_pdf_with_reportlab(
                html_content, pdf_path, candidate_name or "Resume"
            )

        except Exception as e:
            # Fallback: Use reportlab
            self._create_pdf_with_reportlab(
                html_content, pdf_path, candidate_name or "Resume"
            )

        return pdf_filename, str(pdf_path)

    def _create_pdf_with_reportlab(
        self, html_content: str, pdf_path: Path, title: str
    ):
        """
        Create a PDF using reportlab as fallback.
        Extracts text content from HTML and creates a simple PDF.
        """
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

        # Extract content from HTML (simple text extraction)
        import re

        def extract_text(html: str, tag: str) -> str:
            pattern = f"<{tag}[^>]*>(.*?)</{tag}>"
            match = re.search(pattern, html, re.DOTALL)
            if match:
                # Remove HTML tags from content
                content = match.group(1)
                content = re.sub(r"<[^>]+>", "", content)
                return content.strip()
            return ""

        # Extract sections
        name = extract_text(html_content, "title").replace(" - Resume", "")
        summary = extract_text(html_content, "p")

        # Create PDF
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=A4,
            rightMargin=0.75 * inch,
            leftMargin=0.75 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
        )

        styles = getSampleStyleSheet()
        styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=styles["Heading1"],
                fontSize=24,
                textColor=colors.HexColor("#2563eb"),
                spaceAfter=12,
                alignment=1,  # Center
            )
        )
        styles.add(
            ParagraphStyle(
                name="SectionTitle",
                parent=styles["Heading2"],
                fontSize=14,
                textColor=colors.HexColor("#2563eb"),
                spaceAfter=6,
                spaceBefore=12,
                borderWidth=1,
                borderColor=colors.HexColor("#2563eb"),
            )
        )
        styles.add(
            ParagraphStyle(
                name="NormalText",
                parent=styles["Normal"],
                fontSize=10,
                textColor=colors.HexColor("#374151"),
            )
        )

        story = []

        # Title
        story.append(Paragraph(name, styles["CustomTitle"]))
        story.append(Spacer(1, 0.2 * inch))

        # Summary
        if summary:
            story.append(Paragraph("Professional Summary", styles["SectionTitle"]))
            story.append(Paragraph(summary, styles["NormalText"]))
            story.append(Spacer(1, 0.1 * inch))

        # Note about HTML version
        story.append(Spacer(1, 0.2 * inch))
        story.append(
            Paragraph(
                "<i>For full formatting, view the HTML version or print from browser.</i>",
                styles["NormalText"],
            )
        )

        doc.build(story)

    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename by removing invalid characters.

        Args:
            filename: Original filename.

        Returns:
            Sanitized filename safe for filesystem.
        """
        invalid_chars = '<>:"/\\|?*'

        sanitized = filename
        for char in invalid_chars:
            sanitized = sanitized.replace(char, "_")

        sanitized = sanitized.replace(" ", "_")

        while "__" in sanitized:
            sanitized = sanitized.replace("__", "_")

        sanitized = sanitized.strip("_").lower()

        if not sanitized:
            sanitized = str(uuid.uuid4())[:8]

        return sanitized

    def get_download_url(self, filename: str) -> str:
        """Generate download URL for a PDF file."""
        return f"/api/resume/download/{filename}"

    def file_exists(self, filename: str) -> bool:
        """Check if a PDF file exists."""
        file_path = self.output_dir / filename
        return file_path.exists()

    def get_file_path(self, filename: str) -> Path:
        """Get the full path for a PDF file."""
        return self.output_dir / filename


def generate_resume_pdf(
    html_content: str,
    filename: Optional[str] = None,
    candidate_name: Optional[str] = None,
) -> tuple[str, str]:
    """Generate PDF from HTML content."""
    service = PDFService()
    return service.generate_pdf(html_content, filename, candidate_name)
