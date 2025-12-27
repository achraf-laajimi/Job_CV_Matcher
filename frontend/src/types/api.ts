// TypeScript interfaces matching backend Pydantic models

export interface JobDescription {
  text: string
}

export interface MatchResult {
  score: number
  recommendation: string
  strengths: Array<Record<string, any> | string>
  gaps: Array<Record<string, any> | string>
  processing_time?: number
}

export interface RankingResult {
  filename: string
  score: number
  recommendation: string
  strengths: Array<Record<string, any> | string>
  gaps: Array<Record<string, any> | string>
  processing_time?: number
}

export interface BulkRankingResponse {
  total_cvs: number
  total_time: number
  average_time: number
  results: RankingResult[]
}

export interface HealthResponse {
  status: string
  version: string
  optimizations: {
    caching: boolean
    text_trimming: boolean
    parallelization: boolean
    token_limits: boolean
  }
  timestamp: string
}

export interface CacheStats {
  cached_cvs: number
  cache_size_mb: number
  status: string
}

export interface ApiWelcome {
  message: string
  version: string
  endpoints: Record<string, string>
}

export interface ClearCacheResponse {
  message: string
  status: string
}
