import React from 'react'
import { motion } from 'framer-motion'
import { ArrowRight, ExternalLink, Eye, Sparkles } from 'lucide-react'
import { Link } from 'react-router-dom'
import { ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts'
import dashboardData from '../data/dashboardData.json'
import { RecommendationCard, ScoreCard } from '../components'

const pieColors = ['#38bdf8', '#8b5cf6', '#fb923c', '#34d399', '#f43f5e']

export const DashboardPage = () => {
  const { site, overallScore, scores, chartData, recommendations, strengths, weaknesses } = dashboardData

  const pieData = scores.map((item) => ({ name: item.label, value: item.score }))

  return (
    <div className="container px-4 py-12 lg:py-16">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35 }} className="mb-8 flex flex-col gap-4 rounded-3xl border border-slate-800 bg-slate-900/70 p-8 shadow-2xl shadow-slate-950/30 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Result dashboard</p>
          <h1 className="mt-2 text-3xl font-semibold text-white">{site.name}</h1>
          <p className="mt-3 max-w-2xl text-slate-400">{site.summary}</p>
          <a href={site.url} target="_blank" rel="noreferrer" className="mt-4 inline-flex items-center gap-2 text-sm font-medium text-sky-400">
            {site.url} <ExternalLink size={16} />
          </a>
        </div>
        <div className="rounded-2xl border border-sky-500/30 bg-sky-500/10 px-5 py-4 text-center">
          <p className="text-sm text-slate-400">Overall CRO Score</p>
          <p className="text-4xl font-semibold text-white">{overallScore}/100</p>
        </div>
      </motion.div>

      <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
        <div className="space-y-6">
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            {scores.map((item) => (
              <ScoreCard key={item.label} label={item.label} score={item.score} max={100} />
            ))}
          </div>

          <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6">
            <div className="mb-4 flex items-center justify-between">
              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Performance trend</p>
                <h2 className="text-xl font-semibold text-white">Score distribution</h2>
              </div>
              <div className="inline-flex items-center gap-2 rounded-full bg-emerald-500/10 px-3 py-1 text-sm font-medium text-emerald-300">
                <Sparkles size={16} /> Healthy baseline
              </div>
            </div>
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
                  <XAxis dataKey="name" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" domain={[0, 100]} />
                  <Tooltip contentStyle={{ backgroundColor: '#020617', border: '1px solid #334155' }} />
                  <Bar dataKey="score" radius={[8, 8, 0, 0]} fill="#38bdf8" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6">
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Composition</p>
            <h2 className="mt-2 text-xl font-semibold text-white">Area balance</h2>
            <div className="mt-4 h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={pieData} dataKey="value" nameKey="name" innerRadius={60} outerRadius={95} paddingAngle={3}>
                    {pieData.map((entry, index) => (
                      <Cell key={entry.name} fill={pieColors[index % pieColors.length]} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: '#020617', border: '1px solid #334155' }} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6">
            <div className="mb-4 flex items-center justify-between">
              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Recommendations</p>
                <h2 className="text-xl font-semibold text-white">Best next actions</h2>
              </div>
            </div>
            <div className="space-y-3">
              {recommendations.map((item) => (
                <RecommendationCard key={item.title} priority={item.priority} title={item.title} description={item.description} reasoning={item.reasoning} />
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="mt-8 grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
        <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6">
          <div className="mb-4 flex items-center gap-2 text-sky-300">
            <Eye size={18} />
            <p className="text-sm font-semibold uppercase tracking-[0.3em]">Preview</p>
          </div>
          <div className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-950">
            <div className="flex items-center gap-2 border-b border-slate-800 bg-slate-900 px-4 py-3">
              <span className="h-2.5 w-2.5 rounded-full bg-rose-500" />
              <span className="h-2.5 w-2.5 rounded-full bg-amber-500" />
              <span className="h-2.5 w-2.5 rounded-full bg-emerald-500" />
              <span className="ml-3 text-sm text-slate-400">{site.url}</span>
            </div>
            <div className="p-6">
              <div className="rounded-2xl border border-slate-800 bg-gradient-to-br from-slate-900 to-slate-800 p-6">
                <p className="text-sm font-medium text-sky-400">Mocked preview</p>
                <h3 className="mt-3 text-2xl font-semibold text-white">{site.name} landing experience</h3>
                <p className="mt-3 text-sm leading-7 text-slate-400">A polished interface with a clear headline, focused CTA, and space for product proof points.</p>
                <div className="mt-6 flex flex-wrap gap-3">
                  <span className="rounded-full bg-sky-500/10 px-3 py-1 text-sm font-medium text-sky-300">High clarity</span>
                  <span className="rounded-full bg-violet-500/10 px-3 py-1 text-sm font-medium text-violet-300">Strong structure</span>
                  <span className="rounded-full bg-amber-500/10 px-3 py-1 text-sm font-medium text-amber-300">CTA refinement</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6">
          <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Snapshot</p>
          <h2 className="mt-2 text-xl font-semibold text-white">Strengths and watch-outs</h2>
          <div className="mt-6 space-y-4">
            <div>
              <p className="mb-2 text-sm font-semibold text-emerald-300">Strengths</p>
              <ul className="space-y-2 text-sm text-slate-400">
                {strengths.map((item) => <li key={item} className="rounded-xl border border-emerald-500/20 bg-emerald-500/10 px-3 py-2">{item}</li>)}
              </ul>
            </div>
            <div>
              <p className="mb-2 text-sm font-semibold text-amber-300">Weaknesses</p>
              <ul className="space-y-2 text-sm text-slate-400">
                {weaknesses.map((item) => <li key={item} className="rounded-xl border border-amber-500/20 bg-amber-500/10 px-3 py-2">{item}</li>)}
              </ul>
            </div>
          </div>
          <Link to="/report" className="mt-6 inline-flex items-center gap-2 text-sm font-semibold text-sky-400">
            View full report <ArrowRight size={16} />
          </Link>
        </div>
      </div>
    </div>
  )
}