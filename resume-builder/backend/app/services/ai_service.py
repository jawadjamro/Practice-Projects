"""
AI Service for resume optimization.
Handles communication with OpenAI/Claude APIs for intelligent resume enhancement.
"""

import json
import re
from typing import Optional

import httpx

from app.config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    OPENAI_MODEL,
    ANTHROPIC_API_KEY,
    ANTHROPIC_MODEL,
    GEMINI_API_KEY,
    GEMINI_MODEL,
)
from app.models import ExperienceModel, EducationModel, OptimizedResumeData
from app.schemas import ResumeRequest


class AIServiceError(Exception):
    """Custom exception for AI service errors."""

    pass


class AIService:
    """
    AI service for optimizing resume content.
    Supports OpenAI, Anthropic (Claude), and Google Gemini APIs.
    """

    def __init__(self, use_claude: bool = False, use_gemini: bool = False):
        """
        Initialize AI service.

        Args:
            use_claude: If True, use Claude API. Otherwise use OpenAI.
            use_gemini: If True, use Google Gemini API.
        """
        self.use_claude = use_claude
        self.use_gemini = use_gemini
        self.openai_api_key = OPENAI_API_KEY
        self.anthropic_api_key = ANTHROPIC_API_KEY
        self.gemini_api_key = GEMINI_API_KEY

        # Auto-detect: if no preference set, use first available key (priority: Gemini > Claude > OpenAI)
        if not self.use_claude and not self.use_gemini:
            if self.gemini_api_key:
                self.use_gemini = True
            elif self.anthropic_api_key:
                self.use_claude = True

        if not any([self.openai_api_key, self.anthropic_api_key, self.gemini_api_key]):
            raise AIServiceError(
                "No API key configured. Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or GEMINI_API_KEY in .env"
            )

    async def optimize_resume(
        self, request: ResumeRequest
    ) -> OptimizedResumeData:
        """
        Optimize resume content using AI.

        Args:
            request: Resume request with user-provided data.

        Returns:
            OptimizedResumeData with AI-enhanced content.

        Raises:
            AIServiceError: If API call fails or returns invalid response.
        """
        # Build the prompt for AI optimization
        prompt = self._build_optimization_prompt(request)

        # Select API based on configuration and available keys
        # Priority: explicitly set flag > auto-detect by available key
        if self.use_gemini and self.gemini_api_key:
            response_data = await self._call_gemini_api(prompt)
        elif self.use_claude and self.anthropic_api_key:
            response_data = await self._call_claude_api(prompt)
        elif self.openai_api_key:
            response_data = await self._call_openai_api(prompt)
        else:
            raise AIServiceError("No valid API key available for the selected service")

        # Parse and validate the response
        return self._parse_ai_response(response_data, request)

    def _build_optimization_prompt(self, request: ResumeRequest) -> str:
        """
        Build a detailed prompt for resume optimization.

        Args:
            request: Resume request data.

        Returns:
            Formatted prompt string.
        """
        job_context = ""
        if request.job_description:
            job_context = f"""
TARGET JOB DESCRIPTION:
{request.job_description}
"""

        experience_context = ""
        for i, exp in enumerate(request.experience, 1):
            experience_context += f"""
EXPERIENCE {i}:
Company: {exp.company}
Role: {exp.role}
Period: {exp.start_date} - {exp.end_date}
Responsibilities: {exp.responsibilities}
"""

        education_context = ""
        for edu in request.education:
            education_context += f"""
- {edu.degree}, {edu.institution}, {edu.year}
"""

        skills_context = ", ".join(request.skills) if request.skills else "Not provided"

        prompt = f"""
You are an expert resume writer and career coach with 15+ years of experience.
Your task is to optimize a resume to make it highly effective, ATS-friendly, and compelling to hiring managers.

{job_context}

CANDIDATE INFORMATION:

PERSONAL DETAILS:
- Name: {request.personal_info.full_name}
- Email: {request.personal_info.email}
- Phone: {request.personal_info.phone}
- Location: {request.personal_info.location}
{f"- LinkedIn: {request.personal_info.linkedin}" if request.personal_info.linkedin else ""}
{f"- Portfolio: {request.personal_info.portfolio}" if request.personal_info.portfolio else ""}

CURRENT SUMMARY:
{request.summary}

SKILLS:
{skills_context}

EXPERIENCE:{experience_context}

EDUCATION:{education_context}

---

OPTIMIZATION REQUIREMENTS:

1. PROFESSIONAL SUMMARY:
   - Rewrite to be impactful, concise, and tailored to the target role
   - Include relevant keywords from the job description
   - Highlight unique value proposition
   - Keep it 3-5 lines maximum

2. WORK EXPERIENCE:
   - Rewrite each role using action verbs and the STAR method
   - Quantify achievements with specific metrics (%, $, numbers)
   - Focus on impact and results, not just responsibilities
   - Include 3-5 bullet points per role with measurable outcomes
   - Optimize for ATS keywords relevant to the target job

3. SKILLS OPTIMIZATION:
   - Reorganize skills into logical categories
   - Add relevant keywords from job description that match candidate's background
   - Remove redundant or outdated skills
   - Prioritize in-demand technical and soft skills

4. ATS OPTIMIZATION:
   - Extract and incorporate relevant keywords from the job description
   - Use standard job titles and industry terminology
   - Ensure proper keyword density without keyword stuffing

5. GENERAL IMPROVEMENTS:
   - Fix any grammar, spelling, or clarity issues
   - Maintain professional tone throughout
   - Ensure consistency in formatting and style
   - Remove clichés and generic phrases

---

RESPONSE FORMAT:
Return ONLY valid JSON in this exact structure (no markdown, no explanations):

{{
    "optimized_summary": "The rewritten professional summary",
    "optimized_experience": [
        {{
            "company": "Company Name",
            "role": "Job Title",
            "start_date": "Start Date",
            "end_date": "End Date",
            "responsibilities": "Rewritten responsibilities and achievements as bullet points with metrics",
            "achievements": ["Achievement 1 with metric", "Achievement 2 with metric", "Achievement 3 with metric"]
        }}
    ],
    "optimized_education": [
        {{
            "degree": "Degree Name",
            "institution": "Institution Name",
            "year": "Year"
        }}
    ],
    "optimized_skills": ["Skill 1", "Skill 2", "Skill 3", ...],
    "ats_keywords": ["keyword1", "keyword2", "keyword3", ...]
}}
"""
        return prompt

    async def _call_openai_api(self, prompt: str) -> dict:
        """
        Call OpenAI API for resume optimization.

        Args:
            prompt: The optimization prompt.

        Returns:
            Parsed JSON response from API.

        Raises:
            AIServiceError: If API call fails.
        """
        url = f"{OPENAI_BASE_URL}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": OPENAI_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert resume writer. Return ONLY valid JSON, no markdown formatting.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 4000,
            "response_format": {"type": "json_object"},
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()

                content = data["choices"][0]["message"]["content"]
                return self._extract_json_from_response(content)

            except httpx.HTTPError as e:
                raise AIServiceError(f"OpenAI API error: {str(e)}")
            except (KeyError, IndexError) as e:
                raise AIServiceError(f"Invalid OpenAI API response: {str(e)}")

    async def _call_claude_api(self, prompt: str) -> dict:
        """
        Call Anthropic Claude API for resume optimization.

        Args:
            prompt: The optimization prompt.

        Returns:
            Parsed JSON response from API.

        Raises:
            AIServiceError: If API call fails.
        """
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.anthropic_api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }

        # Remove the JSON format instruction from system prompt for Claude
        system_prompt = "You are an expert resume writer. Return ONLY valid JSON."

        payload = {
            "model": ANTHROPIC_MODEL,
            "max_tokens": 4000,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": prompt},
            ],
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()

                content = data["content"][0]["text"]
                return self._extract_json_from_response(content)

            except httpx.HTTPError as e:
                raise AIServiceError(f"Claude API error: {str(e)}")
            except (KeyError, IndexError) as e:
                raise AIServiceError(f"Invalid Claude API response: {str(e)}")

    async def _call_gemini_api(self, prompt: str) -> dict:
        """
        Call Google Gemini API for resume optimization.

        Args:
            prompt: The optimization prompt.

        Returns:
            Parsed JSON response from API.

        Raises:
            AIServiceError: If API call fails.
        """
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
        headers = {
            "Content-Type": "application/json",
        }

        # Add API key to query params
        params = {"key": self.gemini_api_key}

        # Gemini system instruction via prompt
        system_instruction = "You are an expert resume writer. Return ONLY valid JSON, no markdown formatting, no explanations."
        full_prompt = f"{system_instruction}\n\n{prompt}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": full_prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 4000,
                "responseMimeType": "application/json",
            },
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, headers=headers, params=params, json=payload)
                response.raise_for_status()
                data = response.json()

                # Extract text from Gemini response
                if "candidates" in data and len(data["candidates"]) > 0:
                    content = data["candidates"][0]["content"]["parts"][0]["text"]
                    return self._extract_json_from_response(content)
                else:
                    raise AIServiceError("Empty response from Gemini API")

            except httpx.HTTPError as e:
                raise AIServiceError(f"Gemini API error: {str(e)}")
            except (KeyError, IndexError) as e:
                raise AIServiceError(f"Invalid Gemini API response: {str(e)}")

    def _extract_json_from_response(self, content: str) -> dict:
        """
        Extract JSON from AI response, handling potential markdown wrapping.

        Args:
            content: Raw response content.

        Returns:
            Parsed JSON as dictionary.

        Raises:
            AIServiceError: If JSON parsing fails.
        """
        # Remove markdown code blocks if present
        content = re.sub(r"^```json\s*", "", content, flags=re.MULTILINE)
        content = re.sub(r"^```\s*", "", content, flags=re.MULTILINE)
        content = re.sub(r"```$", "", content, flags=re.MULTILINE)
        content = content.strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise AIServiceError(f"Failed to parse AI response as JSON: {str(e)}")

    def _parse_ai_response(
        self, response_data: dict, original_request: ResumeRequest
    ) -> OptimizedResumeData:
        """
        Parse and validate AI response into OptimizedResumeData.

        Args:
            response_data: Parsed JSON from AI.
            original_request: Original resume request for fallback values.

        Returns:
            OptimizedResumeData model.

        Raises:
            AIServiceError: If required fields are missing.
        """
        try:
            # Parse optimized summary
            optimized_summary = response_data.get(
                "optimized_summary", original_request.summary
            )

            # Parse optimized experience
            optimized_experience = []
            ai_experience = response_data.get("optimized_experience", [])

            # If AI didn't return experience, use original with empty achievements
            if not ai_experience:
                for exp in original_request.experience:
                    optimized_experience.append(
                        ExperienceModel(
                            company=exp.company,
                            role=exp.role,
                            start_date=exp.start_date,
                            end_date=exp.end_date,
                            responsibilities=exp.responsibilities,
                            achievements=[],
                        )
                    )
            else:
                for exp_data in ai_experience:
                    optimized_experience.append(
                        ExperienceModel(
                            company=exp_data.get("company", ""),
                            role=exp_data.get("role", ""),
                            start_date=exp_data.get("start_date", ""),
                            end_date=exp_data.get("end_date", ""),
                            responsibilities=exp_data.get("responsibilities", ""),
                            achievements=exp_data.get("achievements", []),
                        )
                    )

            # Parse optimized education
            optimized_education = []
            ai_education = response_data.get("optimized_education", [])

            if not ai_education:
                for edu in original_request.education:
                    optimized_education.append(
                        EducationModel(
                            degree=edu.degree,
                            institution=edu.institution,
                            year=edu.year,
                        )
                    )
            else:
                for edu_data in ai_education:
                    optimized_education.append(
                        EducationModel(
                            degree=edu_data.get("degree", ""),
                            institution=edu_data.get("institution", ""),
                            year=edu_data.get("year", ""),
                        )
                    )

            # Parse optimized skills
            optimized_skills = response_data.get(
                "optimized_skills", original_request.skills
            )

            return OptimizedResumeData(
                summary=optimized_summary,
                experience=optimized_experience,
                education=optimized_education,
                skills=optimized_skills,
                ats_keywords=response_data.get("ats_keywords", []),
            )

        except KeyError as e:
            raise AIServiceError(f"Missing required field in AI response: {str(e)}")


# Convenience function for direct use
async def optimize_resume_data(request: ResumeRequest) -> OptimizedResumeData:
    """
    Optimize resume data using AI.

    Args:
        request: Resume request with user data.

    Returns:
        Optimized resume data.
    """
    service = AIService()
    return await service.optimize_resume(request)
