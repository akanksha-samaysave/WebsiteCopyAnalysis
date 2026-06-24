import React, { useEffect, useState, useRef } from 'react'
import { useSearchParams } from 'react-router-dom'
import { ComparisonBarChart, ScoreDistributionChart, LoadingSpinner, ErrorAlert } from '../components'
import { analysisService } from '../services/api'

// Statuses that mean the job is still in flight
const PENDING_STATUSES = new Set(['pending', 'processing'])

export const ComparisonPage = () => {
  const [searchParams] = useSearchParams()
  const jobId = searchParams.get('jobId')
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Keep a ref to the interval so we can clear it from inside the async callback
  const intervalRef = useRef(null)

  useEffect(() => {
    if (!jobId) {
      setError('No analysis selected. Please start an analysis from the home page.')
      return
    }

    const fetchComparison = async () => {
      try {
        setLoading(true)
        const response = await analysisService.getComparison(jobId)
        setData(response)

        // FIX: stop polling once the job reaches a terminal state
        if (!PENDING_STATUSES.has(response.status)) {
          clearInterval(intervalRef.current)
          intervalRef.current = null
        }
      } catch (err) {
        // Surface the real error message; stop polling on hard errors
        const message =
          err?.response?.data?.detail ||
          err?.response?.data?.message ||
          err.message ||
          'Unknown error'
        setError(message)
        clearInterval(intervalRef.current)
        intervalRef.current = null
      } finally {
        setLoading(false)
      }
    }

    // Initial fetch
    fetchComparison()

    // Refresh every 3 seconds while job is still processing
    intervalRef.current = setInterval(fetchComparison, 3000)
    return () => clearInterval(intervalRef.current)
  }, [jobId])

  if (loading && !data) {
    return (
      <div className="min-h-screen py-12">
        <div className="container text-center">
          <LoadingSpinner />
          <p className="mt-4 text-gray-300">Loading comparison data...</p>
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

  if (!data) {
    return (
      <div className="min-h-screen py-12">
        <div className="container text-center">
          <p className="text-gray-300">No comparison data available</p>
        </div>
      </div>
    )
  }

  // Show a banner while the job is still running
  const isProcessing = PENDING_STATUSES.has(data.status)

  const { ranking, websites, best_category, worst_category } = data

  return (
    <div className="min-h-screen py-12">
      <div className="container">
        <h1 className="text-4xl font-bold mb-4">Comparison Dashboard</h1>

        {/* Processing banner */}
        {isProcessing && (
          <div className="mb-8 flex items-center gap-3 rounded-lg bg-yellow-900/40 border border-yellow-500 px-5 py-3 text-yellow-300">
            <LoadingSpinner small />
            <span>Analysis in progress — results update automatically…</span>
          </div>
        )}

        {/* Ranking */}
        <div className="mb-12 card p-6">
          <h2 className="text-2xl font-bold mb-6">Overall Ranking</h2>
          {ranking && ranking.length > 0 ? (
            <>
              <div className="mb-8">
                <ComparisonBarChart data={ranking} label="Overall Score" />
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead>
                    <tr className="border-b border-slate-700">
                      <th className="px-4 py-3 font-semibold text-gray-300">Rank</th>
                      <th className="px-4 py-3 font-semibold text-gray-300">Website</th>
                      <th className="px-4 py-3 font-semibold text-gray-300">Overall Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    {ranking.map((site, idx) => (
                      <tr key={idx} className="border-b border-slate-700 hover:bg-slate-700/50">
                        <td className="px-4 py-3">
                          <span className="text-lg font-bold">#{idx + 1}</span>
                        </td>
                        <td className="px-4 py-3">
                          <a href={site.url} target="_blank" rel="noopener noreferrer" className="text-primary-400 hover:underline">
                            {site.domain}
                          </a>
                        </td>
                        <td className="px-4 py-3">
                          <span className={`text-lg font-bold ${
                            site.overall_score >= 80 ? 'text-green-500' :
                            site.overall_score >= 60 ? 'text-yellow-500' :
                            'text-red-500'
                          }`}>
                            {site.overall_score.toFixed(0)}/100
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </>
          ) : (
            <p className="text-gray-400">Waiting for completed results…</p>
          )}
        </div>

        {/* Category Comparison */}
        {websites && websites.length > 0 && (
          <div className="mb-12 card p-6">
            <h2 className="text-2xl font-bold mb-6">Category-wise Comparison</h2>
            <ScoreDistributionChart websites={websites} />
          </div>
        )}

        {/* Best & Worst Categories */}
        <div className="grid md:grid-cols-2 gap-6 mb-12">
          {best_category && (
            <div className="card p-6 border-green-500">
              <h3 className="text-lg font-bold mb-2 text-green-500">✨ Best Performing Category</h3>
              <p className="text-2xl font-bold mb-1">{best_category.category.replace(/_/g, ' ').toUpperCase()}</p>
              <p className="text-sm text-gray-400">Average Score: {best_category.average_score.toFixed(1)}/10</p>
            </div>
          )}
          {worst_category && (
            <div className="card p-6 border-red-500">
              <h3 className="text-lg font-bold mb-2 text-red-500">⚠️ Needs Improvement</h3>
              <p className="text-2xl font-bold mb-1">{worst_category.category.replace(/_/g, ' ').toUpperCase()}</p>
              <p className="text-sm text-gray-400">Average Score: {worst_category.average_score.toFixed(1)}/10</p>
            </div>
          )}
        </div>

        {/* Detailed Comparison Table */}
        {websites && websites.length > 0 && (
          <div className="card p-6 overflow-x-auto">
            <h2 className="text-2xl font-bold mb-6">Detailed Scores</h2>
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-slate-700">
                  <th className="px-4 py-3 font-semibold text-gray-300">Website</th>
                  <th className="px-4 py-3 font-semibold text-gray-300">Design</th>
                  <th className="px-4 py-3 font-semibold text-gray-300">Messaging</th>
                  <th className="px-4 py-3 font-semibold text-gray-300">Trust</th>
                  <th className="px-4 py-3 font-semibold text-gray-300">Clarity</th>
                  <th className="px-4 py-3 font-semibold text-gray-300">Conversion</th>
                  <th className="px-4 py-3 font-semibold text-gray-300">UX</th>
                  <th className="px-4 py-3 font-semibold text-gray-300">Overall</th>
                </tr>
              </thead>
              <tbody>
                {websites.map((site, idx) => (
                  <tr key={idx} className="border-b border-slate-700 hover:bg-slate-700/50">
                    <td className="px-4 py-3 font-semibold">{site.domain}</td>
                    <td className="px-4 py-3">{site.scores?.design?.toFixed(1) ?? '-'}</td>
                    <td className="px-4 py-3">{site.scores?.messaging?.toFixed(1) ?? '-'}</td>
                    <td className="px-4 py-3">{site.scores?.trust?.toFixed(1) ?? '-'}</td>
                    <td className="px-4 py-3">{site.scores?.clarity?.toFixed(1) ?? '-'}</td>
                    <td className="px-4 py-3">{site.scores?.conversion?.toFixed(1) ?? '-'}</td>
                    <td className="px-4 py-3">{site.scores?.ux?.toFixed(1) ?? '-'}</td>
                    <td className="px-4 py-3 font-bold">{site.overall_score?.toFixed(0) ?? '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
