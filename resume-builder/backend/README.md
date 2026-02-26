# AI Resume Builder Backend

Production-ready FastAPI backend for a resume generator SaaS.

## Features

- **Resume Generation**: Creates professional HTML resumes from user input
- **PDF Export**: Downloads resumes as PDF files
- **Multiple Templates**: Modern, Classic, and Minimal resume templates
- **Secure**: Input validation with Pydantic, CORS protection, secure file handling
- **Production-Ready**: Modular architecture, proper error handling, async support

## Quick Start

### 1. Install Dependencies

```bash
cd backend
uv sync
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` if needed (optional - works without API keys for basic resume generation).

### 3. Run the Server

```bash
uv run python -m app.main
```

Server will start at `http://localhost:8000`

### 4. API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### POST /api/resume/generate-resume

Generate a resume.

**Request Body:**

```json
{
  "personal_info": {
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-234-567-8900",
    "location": "San Francisco, CA",
    "linkedin": "linkedin.com/in/johndoe",
    "portfolio": "johndoe.com"
  },
  "summary": "Experienced software engineer...",
  "skills": ["Python", "FastAPI", "React"],
  "experience": [
    {
      "company": "Tech Corp",
      "role": "Senior Engineer",
      "start_date": "Jan 2020",
      "end_date": "Present",
      "responsibilities": "Led development of..."
    }
  ],
  "education": [
    {
      "degree": "BS Computer Science",
      "institution": "University",
      "year": "2019"
    }
  ],
  "job_description": "Optional job description for tailoring",
  "template": "modern"
}
```

**Response:**

```json
{
  "optimized_summary": "Experienced software engineer...",
  "optimized_experience": [...],
  "optimized_education": [...],
  "optimized_skills": [...],
  "resume_html": "<!DOCTYPE html>...",
  "pdf_download_url": "/api/resume/download/abc123_resume.pdf"
}
```

### GET /api/resume/download/{filename}

Download a generated PDF resume.

### GET /api/resume/health

Health check endpoint.

## Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI application entry
│   ├── config.py         # Configuration and env vars
│   ├── models.py         # Data models
│   ├── schemas.py        # Pydantic schemas
│   ├── services/
│   │   ├── ai_service.py       # AI optimization (optional)
│   │   ├── resume_builder.py   # HTML resume generation
│   │   └── pdf_service.py      # PDF generation
│   └── routers/
│       └── resume.py     # API endpoints
├── generated/            # Generated PDF files
├── requirements.txt
├── pyproject.toml
└── .env.example
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key (optional) | - |
| `GEMINI_MODEL` | Gemini model to use | `gemini-2.0-flash` |
| `OPENAI_API_KEY` | OpenAI API key (optional) | - |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o` |
| `ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:3000` |
| `DEBUG` | Debug mode | `False` |

## Development

### Run Tests

```bash
pytest
```

## License

MIT
