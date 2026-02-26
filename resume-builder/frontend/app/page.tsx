import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50">
      {/* Navigation */}
      <nav className="border-b border-gray-100 bg-white/80 backdrop-blur-sm">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-2">
            <svg
              className="h-8 w-8 text-blue-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <span className="text-xl font-bold text-gray-900">
              ResumeBuilder
            </span>
          </div>
          <Link
            href="/dashboard"
            className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700"
          >
            Get Started
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl md:text-6xl">
            <span className="block">Create Your Perfect Resume</span>
            <span className="block bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
              Powered by AI
            </span>
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">
            Transform your experience into a professional, ATS-optimized resume
            in minutes. Our AI analyzes job descriptions and tailors your resume
            to stand out.
          </p>
          <div className="mt-10 flex justify-center gap-4">
            <Link
              href="/dashboard"
              className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 to-blue-700 px-8 py-4 font-semibold text-white shadow-lg transition-all hover:from-blue-700 hover:to-blue-800 hover:shadow-xl"
            >
              Build My Resume
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
                  d="M13 7l5 5m0 0l-5 5m5-5H6"
                />
              </svg>
            </Link>
            <Link
              href="#features"
              className="rounded-xl border border-gray-300 bg-white px-8 py-4 font-semibold text-gray-700 transition-all hover:bg-gray-50"
            >
              Learn More
            </Link>
          </div>
        </div>

        {/* Features Section */}
        <div id="features" className="mt-24">
          <h2 className="text-center text-3xl font-bold text-gray-900">
            Why Choose ResumeBuilder?
          </h2>
          <div className="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {/* Feature 1 */}
            <div className="rounded-2xl bg-white p-8 shadow-sm ring-1 ring-gray-200">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-blue-100">
                <svg
                  className="h-6 w-6 text-blue-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 10V3L4 14h7v7l9-11h-7z"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900">
                AI-Powered Optimization
              </h3>
              <p className="mt-2 text-gray-600">
                Our AI rewrites your experience with measurable achievements and
                ATS-friendly keywords.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="rounded-2xl bg-white p-8 shadow-sm ring-1 ring-gray-200">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-blue-100">
                <svg
                  className="h-6 w-6 text-blue-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900">
                ATS Compatible
              </h3>
              <p className="mt-2 text-gray-600">
                Get past applicant tracking systems with optimized formatting
                and keywords.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="rounded-2xl bg-white p-8 shadow-sm ring-1 ring-gray-200">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-blue-100">
                <svg
                  className="h-6 w-6 text-blue-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900">
                Professional Templates
              </h3>
              <p className="mt-2 text-gray-600">
                Choose from modern, classic, or minimal templates designed by
                professionals.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="rounded-2xl bg-white p-8 shadow-sm ring-1 ring-gray-200">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-blue-100">
                <svg
                  className="h-6 w-6 text-blue-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900">
                Save Time
              </h3>
              <p className="mt-2 text-gray-600">
                Create a polished resume in minutes instead of hours. Focus on
                what matters.
              </p>
            </div>

            {/* Feature 5 */}
            <div className="rounded-2xl bg-white p-8 shadow-sm ring-1 ring-gray-200">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-blue-100">
                <svg
                  className="h-6 w-6 text-blue-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900">
                PDF Export
              </h3>
              <p className="mt-2 text-gray-600">
                Download your resume as a high-quality PDF ready to send to
                employers.
              </p>
            </div>

            {/* Feature 6 */}
            <div className="rounded-2xl bg-white p-8 shadow-sm ring-1 ring-gray-200">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-blue-100">
                <svg
                  className="h-6 w-6 text-blue-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900">
                Secure & Private
              </h3>
              <p className="mt-2 text-gray-600">
                Your data is processed securely and never stored permanently.
              </p>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="mt-24 rounded-3xl bg-gradient-to-r from-blue-600 to-blue-800 px-6 py-16 text-center shadow-xl">
          <h2 className="text-3xl font-bold text-white">
            Ready to Land Your Dream Job?
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-blue-100">
            Join thousands of professionals who have created standout resumes
            with our AI-powered platform.
          </p>
          <Link
            href="/dashboard"
            className="mt-8 inline-block rounded-xl bg-white px-8 py-4 font-semibold text-blue-600 shadow-lg transition-all hover:bg-blue-50"
          >
            Get Started for Free
          </Link>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-24 border-t border-gray-200 bg-white">
        <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
            <div className="flex items-center gap-2">
              <svg
                className="h-6 w-6 text-blue-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              <span className="font-semibold text-gray-900">
                ResumeBuilder
              </span>
            </div>
            <p className="text-sm text-gray-500">
              © 2024 ResumeBuilder. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
