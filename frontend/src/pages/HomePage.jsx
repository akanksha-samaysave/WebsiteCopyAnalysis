import React, { useState, useEffect } from 'react'
import { URLInput, ErrorAlert, LoadingSpinner } from '../components'
import { useAnalysis } from '../hooks/useAnalysis'
import { useNavigate } from 'react-router-dom'

export const HomePage = () => {
  const navigate = useNavigate()
  const { jobId, loading, error, startAnalysis, results } = useAnalysis()

  const handleAnalyze = async (urls) => {
    const id = await startAnalysis(urls)
    if (id) {
      // Redirect to dashboard after starting analysis
      setTimeout(() => {
        navigate(`/dashboard?jobId=${id}`)
      }, 500)
    }
  }

  return (
    <div className="min-h-screen py-12">
      <div className="container">
        <div className="max-w-4xl mx-auto mb-12 text-center">
          <h1 className="text-5xl font-bold mb-4">Optimize Your Landing Pages</h1>
          <p className="text-xl text-gray-300 mb-6">
            Get instant insights on UX, copywriting, conversion optimization, and trust signals
          </p>
        </div>

        {error && <ErrorAlert message={error} />}
        
        <URLInput onAnalyze={handleAnalyze} loading={loading} />

        {loading && (
          <div className="mt-12">
            <LoadingSpinner />
            <p className="text-center text-gray-300 mt-4">Setting up analysis...</p>
          </div>
        )}

        <div className="mt-12 grid md:grid-cols-3 gap-6">
          <div className="card p-6 text-center">
            <div className="text-4xl mb-2">📊</div>
            <h3 className="font-bold mb-2">Detailed Analysis</h3>
            <p className="text-sm text-gray-400">Get scores on design, messaging, UX, trust, and conversion</p>
          </div>
          <div className="card p-6 text-center">
            <div className="text-4xl mb-2">🎯</div>
            <h3 className="font-bold mb-2">CRO Recommendations</h3>
            <p className="text-sm text-gray-400">Actionable insights to improve conversion rates</p>
          </div>
          <div className="card p-6 text-center">
            <div className="text-4xl mb-2">📈</div>
            <h3 className="font-bold mb-2">Competitor Comparison</h3>
            <p className="text-sm text-gray-400">Compare multiple sites side-by-side</p>
          </div>
        </div>
      </div>
    </div>
  )
}
