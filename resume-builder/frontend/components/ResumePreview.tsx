'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useResumeStore } from '@/store/resumeStore';
import { downloadPdf } from '@/lib/api';
import Loader from './Loader';

export default function ResumePreview() {
  const router = useRouter();
  const { optimizedData, resumeData, reset } = useResumeStore();
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!optimizedData && !resumeData) {
      router.push('/dashboard');
    }
  }, [optimizedData, resumeData, router]);

  const handleDownload = async () => {
    if (!optimizedData) return;

    setDownloading(true);
    setError(null);

    try {
      const filename = optimizedData.pdf_download_url.split('/').pop() || '';
      const blob = await downloadPdf(filename);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError('Failed to download PDF');
    } finally {
      setDownloading(false);
    }
  };

  const handleRegenerate = () => {
    reset();
    router.push('/dashboard');
  };

  if (!optimizedData) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Loader />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="mx-auto max-w-4xl px-4">
        {/* Header Actions */}
        <div className="mb-6 flex flex-col items-center justify-between gap-4 sm:flex-row">
          <h1 className="text-2xl font-bold text-gray-900">
            Your Optimized Resume
          </h1>
          <div className="flex gap-3">
            <button
              onClick={handleRegenerate}
              className="rounded-lg border border-gray-300 bg-white px-4 py-2 font-medium text-gray-700 transition-colors hover:bg-gray-50"
            >
              Regenerate
            </button>
            <button
              onClick={handleDownload}
              disabled={downloading}
              className="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition-colors hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {downloading ? (
                <>
                  <Loader />
                  <span>Downloading...</span>
                </>
              ) : (
                <>
                  <svg
                    className="h-5 w-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                    />
                  </svg>
                  <span>Download PDF</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 rounded-lg bg-red-50 p-4 text-red-700">
            {error}
          </div>
        )}

        {/* Optimized Info Cards */}
        <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
          <div className="rounded-lg bg-white p-4 shadow-sm">
            <h3 className="text-sm font-medium text-gray-500">Summary</h3>
            <p className="mt-1 text-sm text-gray-900">
              AI-optimized for impact
            </p>
          </div>
          <div className="rounded-lg bg-white p-4 shadow-sm">
            <h3 className="text-sm font-medium text-gray-500">Experience</h3>
            <p className="mt-1 text-sm text-gray-900">
              {optimizedData.optimized_experience.length} role(s) enhanced
            </p>
          </div>
          <div className="rounded-lg bg-white p-4 shadow-sm">
            <h3 className="text-sm font-medium text-gray-500">Skills</h3>
            <p className="mt-1 text-sm text-gray-900">
              {optimizedData.optimized_skills.length} skills optimized
            </p>
          </div>
        </div>

        {/* Resume Preview */}
        <div className="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-lg">
          <div
            className="prose prose-sm max-w-none p-8"
            dangerouslySetInnerHTML={{ __html: optimizedData.resume_html }}
          />
        </div>

        {/* Footer Info */}
        <div className="mt-6 text-center text-sm text-gray-500">
          <p>
            Your resume has been optimized using AI for ATS compatibility and
            impact.
          </p>
          <p className="mt-1">
            Download the PDF or regenerate to make changes.
          </p>
        </div>
      </div>
    </div>
  );
}
