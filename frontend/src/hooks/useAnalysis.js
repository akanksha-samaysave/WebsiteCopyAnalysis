import { useState, useCallback, useEffect, useRef } from 'react'
import { analysisService } from '../services/api'

export const useAnalysis = () => {
  const [jobId, setJobId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const startAnalysis = useCallback(async (urls) => {
    try {
      setLoading(true)
      setError(null)
      const response = await analysisService.analyzePages(urls)
      setJobId(response.job_id)
      return response.job_id
    } catch (err) {
      setError(err.message)
      return null
    } finally {
      setLoading(false)
    }
  }, [])

  const fetchResults = useCallback(async (id) => {
    if (!id) return null
    try {
      setLoading(true)
      const response = await analysisService.getAnalysisResults(id)
      setResults(response)
      return response
    } catch (err) {
      setError(err.message)
      return null
    } finally {
      setLoading(false)
    }
  }, [])

  const intervalRef = useRef(null)
  useEffect(() => {
    if (!jobId) return
    intervalRef.current = setInterval(() => fetchResults(jobId), 3000)
    return () => clearInterval(intervalRef.current)
  }, [jobId, fetchResults])

  return { jobId, loading, results, error, startAnalysis, fetchResults }
}

export const useComparison = (jobId) => {
  const [comparison, setComparison] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const intervalRef = useRef(null)

  useEffect(() => {
    if (!jobId) return

    const fetchComparison = async () => {
      try {
        setLoading(true)
        const response = await analysisService.getComparison(jobId)
        setComparison(response)
        if (!new Set(['pending', 'processing']).has(response.status)) {
          clearInterval(intervalRef.current)
        }
      } catch (err) {
        setError(err.message)
        clearInterval(intervalRef.current)
      } finally {
        setLoading(false)
      }
    }

    fetchComparison()
    intervalRef.current = setInterval(fetchComparison, 3000)
    return () => clearInterval(intervalRef.current)
  }, [jobId])

  return { comparison, loading, error }
}