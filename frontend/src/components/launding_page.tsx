'use client'

import Aurora from './Aurora/Aurora'
import Navbar from './navbar'

interface MatchaCVLandingProps {
  onNavigateToGuide?: () => void
}

export default function MatchaCVLanding({ onNavigateToGuide }: MatchaCVLandingProps = {}) {
  return (
    <div className="relative min-h-screen overflow-hidden">
      <div className="absolute inset-0 z-0">
        <Aurora
          colorStops={['#E9D5FF', '#FECACA', '#C084FC']}
          blend={0.5}
          amplitude={1.0}
          speed={0.5}
        />
      </div>
      
      {/* HEADER */}
      <Navbar />

      {/* HERO SECTION */}
      <div className="relative isolate px-6 pt-14 lg:px-8">
        <div className="mx-auto max-w-2xl py-32 sm:py-48 lg:py-56 text-center">
          <h1 className="text-balance text-5xl font-semibold tracking-tight text-white sm:text-7xl">
            AI-Powered CV to Job Matching
          </h1>

          <p className="mt-8 text-pretty text-lg font-medium text-gray-300 sm:text-xl">
            MatchaCV analyzes resumes and job descriptions using advanced AI
            to deliver an instant match score, highlight strengths, and
            identify skill gaps — helping smarter hiring decisions happen faster.
          </p>

          <div className="mt-10 flex items-center justify-center gap-x-6">
            <a
              href="#matching"
              className="rounded-md bg-purple-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-purple-500 transition-colors"
            >
              Try CV Matching
            </a>
            <a
              href="#guide"
              onClick={onNavigateToGuide}
              className="text-sm font-semibold text-gray-200 hover:text-purple-400 transition-colors"
            >
              Learn how it works →
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
