import React, { useEffect, useState, useCallback, useRef } from 'react'
import { useSearchParams } from 'react-router-dom'
import {
  ScoreCard,
  RadarChartComponent,
  RecommendationCard,
  LoadingSpinner,
  ErrorAlert
} from '../components'
import { analysisService } from '../services/api'
import { Download } from 'lucide-react'

const PENDING_STATUSES = new Set(['pending', 'processing'])

export const DashboardPage = () => {
  const [searchParams] = useSearchParams()
  const jobId = searchParams.get('jobId')

  const [allAnalyses, setAllAnalyses] = useState([])
  const [selectedIndex, setSelectedIndex] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [jobStatus, setJobStatus] = useState(null)
  const [generating, setGenerating] = useState(false)

  const intervalRef = useRef(null)

  const fetchData = useCallback(async () => {
    if (!jobId) return

    try {
      const res = await analysisService.getAnalysisResults(jobId)

      const list = res?.analyses ?? []

      setJobStatus(res?.status)
      setAllAnalyses(list)

      // stop polling when completed/failed
      if (res?.status && !PENDING_STATUSES.has(res.status)) {
        if (intervalRef.current) {
          clearInterval(intervalRef.current)
          intervalRef.current = null
        }
      }
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
        err.message ||
        'Failed to load analysis'
      )

      if (intervalRef.current) {
        clearInterval(intervalRef.current)
        intervalRef.current = null
      }
    }
  }, [jobId])

  useEffect(() => {
    if (!jobId) return

    fetchData()

    intervalRef.current = setInterval(fetchData, 2000)

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
  }, [jobId, fetchData])

  useEffect(() => {
    if (selectedIndex >= allAnalyses.length && allAnalyses.length > 0) {
      setSelectedIndex(0)
    }
  }, [allAnalyses.length, selectedIndex])

  const currentAnalysis = allAnalyses[selectedIndex] ?? null

  const handleDownloadReport = async () => {
    try {
      setGenerating(true)

      await analysisService.generateReport(jobId)

      const blob = await analysisService.downloadReport(jobId)

      const url = window.URL.createObjectURL(blob)

      const a = document.createElement('a')
      a.href = url
      a.download = `analysis_${jobId}.pdf`
      a.click()

      window.URL.revokeObjectURL(url)
    } catch (err) {
      console.error(err)
    } finally {
      setGenerating(false)
    }
  }

  if (loading && allAnalyses.length === 0) {
    return (
      <div className="min-h-screen py-12">
        <div className="container text-center">
          <LoadingSpinner />
          <p className="mt-4 text-gray-300">
            Analyzing your landing pages...
          </p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen py-12">
        <div className="container">
          <ErrorAlert message={error} />
        </div>
      </div>
    )
  }

  if (!currentAnalysis) {
    return (
      <div className="min-h-screen py-12">
        <div className="container text-center">
          {PENDING_STATUSES.has(jobStatus) ? (
            <>
              <LoadingSpinner />
              <p className="mt-4 text-gray-300">
                Analysis queued — results will appear shortly...
              </p>
            </>
          ) : (
            <p className="text-gray-300">
              No analysis data available
            </p>
          )}
        </div>
      </div>
    )
  }

  const scores = currentAnalysis.metadata?.category_scores ?? {}
  const overall = currentAnalysis.metadata?.overall_score ?? 0
  const recommendations = currentAnalysis.recommendations ?? []

  return (
    <div className="min-h-screen py-12">
      <div className="container">

        <div className="flex items-center justify-between mb-12">
          <div>
            <h1 className="text-4xl font-bold mb-2">
              {currentAnalysis.website_url}
            </h1>

            <p className="text-gray-400">
              Status:
              <span className="capitalize ml-2">
                {currentAnalysis.status}
              </span>

              {PENDING_STATUSES.has(jobStatus) && (
                <span className="ml-2 text-yellow-400 text-sm">
                  (updating...)
                </span>
              )}
            </p>
          </div>

          {currentAnalysis.status === 'completed' && (
            <button
              onClick={handleDownloadReport}
              className="btn btn-primary flex items-center gap-2"
              disabled={generating}
            >
              <Download size={20} />
              {generating ? 'Generating...' : 'Download Report'}
            </button>
          )}
        </div>

        {allAnalyses.length > 1 && (
          <div className="mb-8 flex gap-2 flex-wrap">
            {allAnalyses.map((analysis, index) => (
              <button
                key={index}
                onClick={() => setSelectedIndex(index)}
                className={`px-4 py-2 rounded-lg transition ${
                  selectedIndex === index
                    ? 'bg-primary-600 text-white'
                    : 'bg-slate-700 text-gray-300 hover:bg-slate-600'
                }`}
              >
                {(analysis.website_url || '').split('/')[2] ||
                  `Site ${index + 1}`}
              </button>
            ))}
          </div>
        )}

        {currentAnalysis.status === 'completed' ? (
          <>
            <div className="mb-12 card p-8 text-center">
              <p className="text-gray-400 mb-2">Overall Score</p>

              <div className="text-6xl font-bold mb-4">
                <span
                  className={
                    overall >= 80
                      ? 'text-green-500'
                      : overall >= 60
                      ? 'text-yellow-500'
                      : 'text-red-500'
                  }
                >
                  {Number(overall).toFixed(0)}
                </span>
                <span className="text-2xl text-gray-400">/100</span>
              </div>
            </div>

            <div className="mb-12">
              <h2 className="text-2xl font-bold mb-6">
                Category Breakdown
              </h2>

              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                <ScoreCard label="Design" score={scores.design ?? 0} />
                <ScoreCard label="Messaging" score={scores.messaging ?? 0} />
                <ScoreCard label="Trust" score={scores.trust ?? 0} />
                <ScoreCard label="Clarity" score={scores.clarity ?? 0} />
                <ScoreCard label="Conversion" score={scores.conversion ?? 0} />
                <ScoreCard label="UX" score={scores.ux ?? 0} />
              </div>
            </div>

            {Object.keys(scores).length > 0 && (
              <div className="mb-12 card p-6">
                <h2 className="text-xl font-bold mb-6">
                  Performance Profile
                </h2>

                <RadarChartComponent
                  data={scores}
                  categories={Object.keys(scores)}
                />
              </div>
            )}

            <div>
              <h2 className="text-2xl font-bold mb-6">
                Recommendations
              </h2>

              <div className="space-y-4">
                {recommendations.length > 0 ? (
                  recommendations.map((rec, idx) => (
                    <RecommendationCard
                      key={idx}
                      priority={rec.priority}
                      title={rec.title}
                      description={rec.description}
                      reasoning={rec.reasoning}
                    />
                  ))
                ) : (
                  <p className="text-gray-400">
                    No recommendations available yet
                  </p>
                )}
              </div>
            </div>
          </>
        ) : (
          <div className="text-center">
            <LoadingSpinner />
            <p className="mt-4 text-gray-300">
              {currentAnalysis.status === 'failed'
                ? `Analysis failed${
                    currentAnalysis.metadata?.error
                      ? ': ' + currentAnalysis.metadata.error
                      : ''
                  }`
                : 'Still analyzing...'}
            </p>
          </div>
        )}
      </div>
    </div>
  )
}