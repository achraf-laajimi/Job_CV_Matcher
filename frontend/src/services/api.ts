// API service for CV-Job Matching backend
import type {
  MatchResult,
  BulkRankingResponse,
  HealthResponse,
  CacheStats,
  ApiWelcome,
  ClearCacheResponse
} from '../types/api'

// API base URL - update this based on your backend configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

/**
 * Root endpoint - Get API information
 */
export async function getApiInfo(): Promise<ApiWelcome> {
  const response = await fetch(`${API_BASE_URL}/`)
  if (!response.ok) {
    throw new Error(`API request failed: ${response.statusText}`)
  }
  return response.json()
}

/**
 * Health check endpoint
 */
export async function getHealthCheck(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/health`)
  if (!response.ok) {
    throw new Error(`Health check failed: ${response.statusText}`)
  }
  return response.json()
}

/**
 * Match a single CV against a job description
 * @param cvFile - PDF file of the CV
 * @param jobDescription - Job description text
 */
export async function matchSingleCV(
  cvFile: File,
  jobDescription: string
): Promise<MatchResult> {
  const formData = new FormData()
  formData.append('file', cvFile)
  formData.append('job_description', jobDescription)

  const response = await fetch(`${API_BASE_URL}/match`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }))
    throw new Error(error.detail || 'Failed to match CV')
  }

  return response.json()
}

/**
 * Rank multiple CVs against a job description
 * @param cvFiles - Array of PDF files
 * @param jobDescription - Job description text
 */
export async function rankMultipleCVs(
  cvFiles: File[],
  jobDescription: string
): Promise<BulkRankingResponse> {
  console.log('API: rankMultipleCVs called with', cvFiles.length, 'files')
  const formData = new FormData()
  
  // Append all files
  cvFiles.forEach((file) => {
    formData.append('files', file)
    console.log('API: Added file:', file.name, file.size, 'bytes')
  })
  
  formData.append('job_description', jobDescription)
  console.log('API: Added job description, length:', jobDescription.length)

  console.log('API: Sending POST to', `${API_BASE_URL}/rank`)
  const response = await fetch(`${API_BASE_URL}/rank`, {
    method: 'POST',
    body: formData,
  })

  console.log('API: Response status:', response.status, response.statusText)

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }))
    console.error('API: Error response:', error)
    throw new Error(error.detail || 'Failed to rank CVs')
  }

  console.log('API: Parsing JSON response...')
  const data = await response.json()
  console.log('API: Response data:', data)
  return data
}

/**
 * Get cache statistics
 */
export async function getCacheStats(): Promise<CacheStats> {
  const response = await fetch(`${API_BASE_URL}/cache/stats`)
  if (!response.ok) {
    throw new Error(`Failed to get cache stats: ${response.statusText}`)
  }
  return response.json()
}

/**
 * Clear all cached CV data
 */
export async function clearCache(): Promise<ClearCacheResponse> {
  const response = await fetch(`${API_BASE_URL}/cache`, {
    method: 'DELETE',
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }))
    throw new Error(error.detail || 'Failed to clear cache')
  }

  return response.json()
}
