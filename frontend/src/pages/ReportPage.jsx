import React from 'react'
import { motion } from 'framer-motion'
import { Download, FileText, Sparkles } from 'lucide-react'
import reportData from '../data/reportData.json'

export const ReportPage = () => {
  return (
    <div className="container px-4 py-12 lg:py-16">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35 }} className="rounded-3xl border border-slate-800 bg-slate-900/70 p-8 shadow-2xl shadow-slate-950/30">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Report page</p>
            <h1 className="mt-2 text-3xl font-semibold text-white">Executive-ready landing page report</h1>
          </div>
          <div className="flex flex-wrap gap-3">
            <button className="btn btn-secondary inline-flex items-center gap-2"><Download size={16} /> Download PDF</button>
            <button className="btn btn-primary inline-flex items-center gap-2"><FileText size={16} /> Export Report</button>
          </div>
        </div>

        <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-950/70 p-6">
          <div className="flex items-center gap-2 text-sky-300">
            <Sparkles size={18} />
            <p className="text-sm font-semibold uppercase tracking-[0.3em]">Executive summary</p>
          </div>
          <p className="mt-4 text-lg leading-8 text-slate-300">{reportData.executiveSummary}</p>
        </div>

        <div className="mt-8 grid gap-6 lg:grid-cols-2">
          <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-6">
            <h2 className="text-xl font-semibold text-white">Strengths</h2>
            <ul className="mt-4 space-y-3 text-sm text-slate-400">
              {reportData.strengths.map((item) => (
                <li key={item} className="rounded-xl border border-emerald-500/20 bg-emerald-500/10 px-3 py-2">{item}</li>
              ))}
            </ul>
          </div>
          <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-6">
            <h2 className="text-xl font-semibold text-white">Weaknesses</h2>
            <ul className="mt-4 space-y-3 text-sm text-slate-400">
              {reportData.weaknesses.map((item) => (
                <li key={item} className="rounded-xl border border-amber-500/20 bg-amber-500/10 px-3 py-2">{item}</li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-8 grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
          <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-6">
            <h2 className="text-xl font-semibold text-white">Recommendations</h2>
            <ul className="mt-4 space-y-3 text-sm text-slate-400">
              {reportData.recommendations.map((item) => (
                <li key={item} className="rounded-xl border border-slate-800 bg-slate-900/80 px-3 py-3">{item}</li>
              ))}
            </ul>
          </div>
          <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-6">
            <h2 className="text-xl font-semibold text-white">Priority improvements</h2>
            <div className="mt-4 flex flex-wrap gap-2">
              {reportData.priorityImprovements.map((item) => (
                <span key={item} className="rounded-full bg-sky-500/10 px-3 py-2 text-sm font-medium text-sky-300">{item}</span>
              ))}
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
