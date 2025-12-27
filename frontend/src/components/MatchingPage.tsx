import { useState } from 'react'
import Aurora from './Aurora/Aurora'
import Navbar from './navbar'
import PyramidLoader from './PyramidLoader/PyramidLoader'
import { rankMultipleCVs } from '../services/api'
import type { BulkRankingResponse } from '../types/api'

export default function MatchingPage() {
  const [jobDescription, setJobDescription] = useState('')
  const [cvFiles, setCvFiles] = useState<File[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [results, setResults] = useState<BulkRankingResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const files = Array.from(e.target.files)
      const pdfFiles = files.filter(file => file.name.endsWith('.pdf'))
      
      if (pdfFiles.length !== files.length) {
        setError('Only PDF files are supported')
        setTimeout(() => setError(null), 3000)
      }
      
      setCvFiles(prev => [...prev, ...pdfFiles])
    }
  }

  const handleRemoveFile = (index: number) => {
    setCvFiles(prev => prev.filter((_, i) => i !== index))
  }

  const handleFindBestCandidate = async () => {
    if (!jobDescription.trim()) {
      setError('Please enter a job description')
      setTimeout(() => setError(null), 3000)
      return
    }

    if (cvFiles.length === 0) {
      setError('Please upload at least one CV')
      setTimeout(() => setError(null), 3000)
      return
    }

    setIsLoading(true)
    setError(null)
    setResults(null)

    try {
      console.log('Starting CV analysis...', { cvCount: cvFiles.length })
      const response = await rankMultipleCVs(cvFiles, jobDescription)
      console.log('Response received:', response)
      console.log('Response type:', typeof response)
      console.log('Response keys:', Object.keys(response))
      setResults(response)
      console.log('Results set successfully')
    } catch (err) {
      console.error('Error processing CVs:', err)
      setError(err instanceof Error ? err.message : 'Failed to process CVs')
    } finally {
      console.log('Setting isLoading to false')
      setIsLoading(false)
      console.log('isLoading set to false')
    }
  }

  const getRecommendationColor = (recommendation: string) => {
    switch (recommendation.toLowerCase()) {
      case 'strong match':
        return 'text-green-400 bg-green-900/30 border-green-700'
      case 'good match':
        return 'text-blue-400 bg-blue-900/30 border-blue-700'
      case 'potential match':
        return 'text-yellow-400 bg-yellow-900/30 border-yellow-700'
      case 'weak match':
        return 'text-orange-400 bg-orange-900/30 border-orange-700'
      default:
        return 'text-gray-400 bg-gray-900/30 border-gray-700'
    }
  }

  return (
    <div className="relative min-h-screen overflow-hidden">
      {/* Animated Aurora Background */}
      <div className="absolute inset-0 z-0">
        <Aurora
          colorStops={['#C8ACD6', '#433D8B']}
          blend={0.5}
          amplitude={1.0}
          speed={0.5}
        />
      </div>

      {/* Navbar */}
      <Navbar />

      {/* Main Content */}
      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 pt-28">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-4">
            Find Your Best Candidate
          </h1>
          <p className="text-xl text-gray-300">
            Upload CVs and match them against your job description
          </p>
        </div>

        {/* Job Description Input */}
        <div className="mb-8 bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700">
          <label className="block text-white font-semibold mb-3 text-lg">
            Step 1: Enter Job Description
          </label>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste your job description here... Include required skills, experience, education, and responsibilities."
            className="w-full h-48 px-4 py-3 bg-gray-900/50 border border-gray-600 rounded-lg text-gray-200 placeholder-gray-500 focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/50 resize-none"
          />
        </div>

        {/* CV Upload Section - Hidden when loading or showing results */}
        {!isLoading && !results && (
          <div className="mb-8 bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700">
            <label className="block text-white font-semibold mb-3 text-lg">
              Step 2: Upload CVs (PDF format)
            </label>
            
            <div className="mb-4">
              <input
                type="file"
                id="cv-upload"
                multiple
                accept=".pdf"
                onChange={handleFileUpload}
                className="hidden"
              />
              <label
                htmlFor="cv-upload"
                className="inline-flex items-center px-6 py-3 bg-purple-600 text-white font-semibold rounded-lg cursor-pointer hover:bg-purple-500 transition-colors"
              >
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                Upload CVs
              </label>
            </div>

            {/* Uploaded Files List */}
            {cvFiles.length > 0 && (
              <div className="space-y-2">
                <p className="text-gray-300 font-medium mb-2">
                  Uploaded CVs ({cvFiles.length})
                </p>
                {cvFiles.map((file, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between bg-gray-900/50 border border-gray-600 rounded-lg px-4 py-3"
                  >
                    <div className="flex items-center">
                      <svg className="w-5 h-5 text-purple-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                      </svg>
                      <span className="text-gray-200">{file.name}</span>
                      <span className="text-gray-500 ml-3 text-sm">
                        ({(file.size / 1024).toFixed(1)} KB)
                      </span>
                    </div>
                    <button
                      onClick={() => handleRemoveFile(index)}
                      className="text-red-400 hover:text-red-300 transition-colors"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-8 bg-red-900/30 border border-red-700 rounded-lg px-4 py-3">
            <p className="text-red-400">{error}</p>
          </div>
        )}

        {/* Debug Info - Remove this after testing */}
       

        {/* Find Best Candidate Button */}
        {!isLoading && !results && (
          <div className="text-center mb-8">
            <button
              onClick={handleFindBestCandidate}
              disabled={!jobDescription.trim() || cvFiles.length === 0}
              className="px-8 py-4 bg-purple-600 text-white font-bold text-lg rounded-lg hover:bg-purple-500 disabled:bg-gray-600 disabled:cursor-not-allowed transition-colors shadow-lg"
            >
              🔍 Find Best Candidate
            </button>
          </div>
        )}

        {/* Loading State */}
        {isLoading && (
          <div className="flex flex-col items-center justify-center py-8">
            <PyramidLoader />
            <p className="text-white text-xl mt-8">Analyzing CVs...</p>
            <p className="text-gray-400 mt-2">This may take a few moments</p>
          </div>
        )}

        {/* Simple Results Check */}
        {results && (
          <div className="mb-4 bg-green-900/30 border border-green-700 rounded-lg px-4 py-3">
            <p className="text-green-400">
              ✅ Results received! Total CVs: {results.total_cvs}, Results array length: {results.results?.length}
            </p>
          </div>
        )}

        {/* Results */}
        {results && !isLoading && (
          <div className="space-y-6">
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700">
              <h2 className="text-2xl font-bold text-white mb-4">
                📊 Ranking Results
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="bg-purple-900/30 border border-purple-700 rounded-lg p-4">
                  <p className="text-purple-300 text-sm">Total CVs</p>
                  <p className="text-white text-3xl font-bold">{results.total_cvs}</p>
                </div>
                <div className="bg-purple-900/30 border border-purple-700 rounded-lg p-4">
                  <p className="text-purple-300 text-sm">Total Time</p>
                  <p className="text-white text-3xl font-bold">{results.total_time}s</p>
                </div>
                <div className="bg-purple-900/30 border border-purple-700 rounded-lg p-4">
                  <p className="text-purple-300 text-sm">Avg Time/CV</p>
                  <p className="text-white text-3xl font-bold">{results.average_time}s</p>
                </div>
              </div>
            </div>

            {/* Ranked Candidates */}
            <div className="space-y-4">
              {results.results.map((result, index) => (
                <div
                  key={index}
                  className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700 hover:border-purple-500 transition-all"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center">
                      <div className="w-12 h-12 bg-purple-600 rounded-full flex items-center justify-center text-white font-bold text-xl mr-4">
                        #{index + 1}
                      </div>
                      <div>
                        <h3 className="text-xl font-bold text-white">{result.filename}</h3>
                        <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium border mt-1 ${getRecommendationColor(result.recommendation)}`}>
                          {result.recommendation}
                        </span>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-4xl font-bold text-purple-400">{result.score}%</p>
                      <p className="text-gray-400 text-sm">{result.processing_time}s</p>
                    </div>
                  </div>

                  {/* Strengths */}
                  {result.strengths.length > 0 && (
                    <div className="mb-4">
                      <h4 className="text-green-400 font-semibold mb-2 flex items-center">
                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Strengths
                      </h4>
                      <ul className="space-y-1 ml-7">
                        {result.strengths.map((strength, i) => (
                          <li key={i} className="text-gray-300 text-sm">
                            • {typeof strength === 'string' ? strength : (strength.point || strength.skill || JSON.stringify(strength))}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Gaps */}
                  {result.gaps.length > 0 && (
                    <div>
                      <h4 className="text-orange-400 font-semibold mb-2 flex items-center">
                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                        Gaps
                      </h4>
                      <ul className="space-y-1 ml-7">
                        {result.gaps.map((gap, i) => (
                          <li key={i} className="text-gray-300 text-sm">
                            • {typeof gap === 'string' ? gap : (gap.point || gap.skill || gap.error || JSON.stringify(gap))}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* Reset Button */}
            <div className="text-center pt-8">
              <button
                onClick={() => {
                  setResults(null)
                  setJobDescription('')
                  setCvFiles([])
                }}
                className="px-6 py-3 bg-gray-700 text-white font-semibold rounded-lg hover:bg-gray-600 transition-colors"
              >
                Start New Analysis
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
