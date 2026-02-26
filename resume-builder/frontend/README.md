# AI Resume Builder - Frontend

Modern SaaS frontend for an AI-powered resume generator built with Next.js 14.

## Tech Stack

- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS v4
- **HTTP Client**: Axios
- **Forms**: React Hook Form
- **State Management**: Zustand with localStorage persistence

## Getting Started

### Prerequisites

- Node.js 18+
- Backend server running at `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Create .env.local file
cp .env.local.example .env.local
```

### Development

```bash
# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the application.

### Build

```bash
# Production build
npm run build

# Start production server
npm start
```

### Lint

```bash
npm run lint
```

## Project Structure

```
frontend/
├── app/
│   ├── page.tsx              # Landing page
│   ├── dashboard/page.tsx    # Resume builder form
│   ├── preview/page.tsx      # Resume preview & download
│   ├── layout.tsx            # Root layout
│   └── globals.css           # Global styles
├── components/
│   ├── ResumeForm.tsx        # Main form component
│   ├── ResumePreview.tsx     # Preview component
│   ├── TemplateSelector.tsx  # Template selection
│   ├── SkillsInput.tsx       # Tag-based skills input
│   ├── ExperienceSection.tsx # Dynamic experience entries
│   ├── EducationSection.tsx  # Dynamic education entries
│   └── Loader.tsx            # Loading spinner
├── store/
│   └── resumeStore.ts        # Zustand state management
├── lib/
│   └── api.ts                # API client
├── types/
│   └── resume.ts             # TypeScript interfaces
└── .env.local                # Environment variables
```

## Features

### Landing Page (`/`)
- Hero section with gradient CTA
- Feature highlights
- Modern SaaS design
- Fully responsive

### Dashboard (`/dashboard`)
- Personal information form
- Professional summary textarea
- Tag-based skills input
- Dynamic experience section (add/remove)
- Dynamic education section (add/remove)
- Job description input for AI optimization
- Template selector (Modern, Classic, Minimal)
- Form validation with React Hook Form

### Preview Page (`/preview`)
- Render optimized resume HTML
- Download PDF button
- Regenerate option
- Clean professional layout

## State Management

Zustand store with localStorage persistence:

```typescript
{
  resumeData: ResumeRequest | null,
  optimizedData: ResumeResponse | null,
  loading: boolean,
  error: string | null
}
```

## API Integration

The frontend communicates with the backend at:
- `POST /api/resume/generate-resume` - Generate optimized resume
- `GET /api/resume/download/{filename}` - Download PDF

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |

## Design System

- **Primary Color**: Blue (#2563eb)
- **Background**: White with gray accents
- **Typography**: Geist Sans + Geist Mono
- **Components**: Rounded corners, soft shadows, clean spacing

## License

MIT
