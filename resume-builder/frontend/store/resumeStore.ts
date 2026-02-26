import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { ResumeStore, ResumeRequest, ResumeResponse } from '@/types/resume';

const initialState = {
  resumeData: null,
  optimizedData: null,
  loading: false,
  error: null,
};

export const useResumeStore = create<ResumeStore>()(
  persist(
    (set) => ({
      ...initialState,

      setResumeData: (data: ResumeRequest) =>
        set((state) => ({
          ...state,
          resumeData: data,
          error: null,
        })),

      setOptimizedData: (data: ResumeResponse) =>
        set((state) => ({
          ...state,
          optimizedData: data,
          loading: false,
          error: null,
        })),

      setLoading: (loading: boolean) =>
        set((state) => ({
          ...state,
          loading,
        })),

      setError: (error: string | null) =>
        set((state) => ({
          ...state,
          loading: false,
          error,
        })),

      reset: () => set(initialState),
    }),
    {
      name: 'resume-storage',
      partialize: (state) => ({ resumeData: state.resumeData }),
    }
  )
);
