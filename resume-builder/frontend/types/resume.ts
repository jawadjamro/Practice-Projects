export interface PersonalInfo {
  full_name: string;
  email: string;
  phone: string;
  location: string;
  linkedin?: string;
  portfolio?: string;
}

export interface ExperienceItem {
  company: string;
  role: string;
  start_date: string;
  end_date: string;
  responsibilities: string;
}

export interface EducationItem {
  degree: string;
  institution: string;
  year: string;
}

export interface ResumeRequest {
  personal_info: PersonalInfo;
  summary: string;
  skills: string[];
  experience: ExperienceItem[];
  education: EducationItem[];
  job_description: string;
  template: string;
}

export interface OptimizedExperienceItem {
  company: string;
  role: string;
  start_date: string;
  end_date: string;
  responsibilities: string;
  achievements: string[];
}

export interface OptimizedEducationItem {
  degree: string;
  institution: string;
  year: string;
}

export interface ResumeResponse {
  optimized_summary: string;
  optimized_experience: OptimizedExperienceItem[];
  optimized_education: OptimizedEducationItem[];
  optimized_skills: string[];
  resume_html: string;
  pdf_download_url: string;
}

export interface ResumeState {
  resumeData: ResumeRequest | null;
  optimizedData: ResumeResponse | null;
  loading: boolean;
  error: string | null;
}

export interface ResumeStore extends ResumeState {
  setResumeData: (data: ResumeRequest) => void;
  setOptimizedData: (data: ResumeResponse) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  reset: () => void;
}
