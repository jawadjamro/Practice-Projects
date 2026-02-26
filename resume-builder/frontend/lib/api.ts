import axios from 'axios';
import { ResumeRequest, ResumeResponse } from '@/types/resume';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const generateResume = async (
  data: ResumeRequest
): Promise<ResumeResponse> => {
  const response = await api.post<ResumeResponse>(
    '/api/resume/generate-resume',
    data
  );
  return response.data;
};

export const downloadPdf = async (filename: string): Promise<Blob> => {
  const response = await api.get(`/api/resume/download/${filename}`, {
    responseType: 'blob',
  });
  return response.data;
};
