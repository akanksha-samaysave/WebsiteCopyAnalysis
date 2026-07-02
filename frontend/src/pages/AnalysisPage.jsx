import React, { useEffect, useMemo, useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowRight, CheckCircle2, ChevronDown, Loader2, Sparkles } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import landingPageData from '../data/landingPage.json'

const steps = [
  'Fetching website...',
  'Extracting content...',
  'Running AI analysis...',
  'Generating recommendations...',
]

export const AnalysisPage = () => {
  const navigate = useNavigate()
  const [url, setUrl] = useState(landingPageData.exampleUrls[0])
  const [loading, setLoading] = useState(false)
  const [activeStep, setActiveStep] = useState(0)

  useEffect(() => {
    if (!loading) return

    const timer = setInterval(() => {
      setActiveStep((prev) => (prev + 1) % steps.length)
    }, 800)

    return () => clearInterval(timer)
  }, [loading])

  const handleAnalyze = () => {
    if (!url.trim()) return
    setLoading(true)
    setActiveStep(0)

    window.setTimeout(() => {
      setLoading(false)
      navigate('/dashboard')
    }, 3600)
  }

  const progressLabel = useMemo(() => steps[activeStep], [activeStep])

  return (
    <div className="container px-4 py-12 lg:py-16">
      <div className="grid gap-8 lg:grid-cols-[0.95fr_1.05fr] lg:items-start">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35 }} className="rounded-3xl border border-slate-800 bg-slate-900/70 p-8 shadow-2xl shadow-slate-950/30">
          <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Analysis workspace</p>
          <h1 className="mt-3 text-3xl font-semibold text-white">Inspect a landing page in seconds</h1>
          <p className="mt-4 text-slate-400">Use a real-world example URL or paste your own. This flow is intentionally mock-driven to demonstrate the experience.</p>

          <div className="mt-8 space-y-4">
            <label className="block text-sm font-medium text-slate-300" htmlFor="url-input">Website URL</label>
            <div className="relative">
              <input id="url-input" value={url} onChange={(event) => setUrl(event.target.value)} className="input pr-12" placeholder="https://example.com" />
              <div className="pointer-events-none absolute inset-y-0 right-4 flex items-center text-slate-500">
                <ChevronDown size={18} />
              </div>
            </div>

            <div className="flex flex-wrap gap-3">
              {landingPageData.exampleUrls.map((exampleUrl) => (
                <button key={exampleUrl} onClick={() => setUrl(exampleUrl)} className="rounded-full border border-slate-700 bg-slate-900/80 px-3 py-2 text-sm text-slate-300 transition hover:border-sky-500 hover:text-white">
                  {exampleUrl}
                </button>
              ))}
            </div>

            <button onClick={handleAnalyze} disabled={loading} className="btn btn-primary mt-2 inline-flex items-center gap-2 px-5 py-3">
              {loading ? 'Analyzing...' : 'Analyze'}
              {loading ? <Loader2 size={18} className="animate-spin" /> : <ArrowRight size={18} />}
            </button>
          </div>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.08 }} className="rounded-3xl border border-slate-800 bg-slate-900/70 p-8 shadow-2xl shadow-slate-950/30">
          <div className="flex items-center gap-2 text-sky-300">
            <Sparkles size={18} />
            <p className="text-sm font-semibold uppercase tracking-[0.3em]">Analysis progress</p>
          </div>
          <h2 className="mt-3 text-2xl font-semibold text-white">Your mock analysis is underway</h2>

          <div className="mt-8 space-y-4">
            {steps.map((step, index) => {
              const completed = !loading ? index < 4 : index < activeStep
              return (
                <div key={step} className={`flex items-center gap-3 rounded-2xl border px-4 py-3 ${completed ? 'border-emerald-500/30 bg-emerald-500/10' : 'border-slate-800 bg-slate-950/70'}`}>
                  {completed ? <CheckCircle2 size={18} className="text-emerald-400" /> : <Loader2 size={18} className={`animate-spin ${loading ? 'text-sky-400' : 'text-slate-500'}`} />}
                  <div className="flex-1">
                    <p className="font-medium text-white">{step}</p>
                    <p className="text-sm text-slate-400">{index === activeStep && loading ? 'In progress' : completed ? 'Complete' : 'Queued'}</p>
                  </div>
                </div>
              )
            })}
          </div>

          <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
            <p className="text-sm text-slate-400">Current status</p>
            <p className="mt-2 text-lg font-semibold text-white">{loading ? progressLabel : 'Ready to begin'}</p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
