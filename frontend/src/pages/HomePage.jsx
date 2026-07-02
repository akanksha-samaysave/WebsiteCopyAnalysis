import React from 'react'
import { motion } from 'framer-motion'
import { ArrowRight, BarChart3, MessageSquareText, Sparkles, ShieldCheck } from 'lucide-react'
import { useNavigate, Link } from 'react-router-dom'
import data from '../data/landingPage.json'

const iconMap = {
  Sparkles,
  MessageSquareText,
  BarChart3,
}

export const HomePage = () => {
  const navigate = useNavigate()

  return (
    <div className="relative overflow-hidden">
      <div className="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top_left,_rgba(14,165,233,0.2),_transparent_35%),radial-gradient(circle_at_bottom_right,_rgba(129,140,248,0.2),_transparent_30%)]" />
      <section className="container grid gap-10 px-4 py-16 lg:grid-cols-[1.1fr_0.9fr] lg:items-center lg:py-24">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
          <p className="mb-4 inline-flex rounded-full border border-sky-500/30 bg-sky-500/10 px-3 py-1 text-sm font-medium text-sky-300">
            {data.hero.eyebrow}
          </p>
          <h1 className="max-w-3xl text-4xl font-semibold tracking-tight text-white sm:text-5xl lg:text-6xl">
            {data.hero.title}
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-300">
            {data.hero.description}
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <button onClick={() => navigate('/analyze')} className="inline-flex items-center gap-2 rounded-full bg-sky-500 px-5 py-3 font-semibold text-white transition hover:bg-sky-400">
              {data.hero.primaryCta} <ArrowRight size={18} />
            </button>
            <Link to="/api-docs" className="inline-flex items-center gap-2 rounded-full border border-slate-700 bg-slate-900/70 px-5 py-3 font-semibold text-slate-100 transition hover:border-slate-500">
              {data.hero.secondaryCta}
            </Link>
          </div>
          <div className="mt-8 flex flex-wrap gap-4 text-sm text-slate-400">
            <span className="inline-flex items-center gap-2"><ShieldCheck size={16} className="text-emerald-400" /> No backend required</span>
            <span className="inline-flex items-center gap-2"><Sparkles size={16} className="text-violet-400" /> Mock-first demo experience</span>
          </div>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.1 }} className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl shadow-slate-950/50 backdrop-blur">
          <div className="rounded-2xl border border-slate-800 bg-slate-950/80 p-5">
            <div className="mb-4 flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-400">Demo workflow</p>
                <p className="text-xl font-semibold text-white">CRO Snapshot</p>
              </div>
              <div className="rounded-full bg-emerald-500/15 px-3 py-1 text-sm font-medium text-emerald-300">Live preview</div>
            </div>
            <div className="space-y-4">
              {['UX audit', 'Copywriting health', 'Priority recommendations'].map((item, index) => (
                <div key={item} className="flex items-center justify-between rounded-2xl border border-slate-800 bg-slate-900/80 px-4 py-3">
                  <div>
                    <p className="font-medium text-white">{item}</p>
                    <p className="text-sm text-slate-400">Mocked workflow step {index + 1}</p>
                  </div>
                  <div className="text-2xl font-semibold text-sky-400">{index + 1}/3</div>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      </section>

      <section className="container px-4 py-8 lg:py-16">
        <div className="mb-8 flex items-end justify-between gap-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Features</p>
            <h2 className="text-3xl font-semibold text-white">Everything needed to shape a stronger funnel</h2>
          </div>
        </div>
        <div className="grid gap-6 md:grid-cols-3">
          {data.features.map((feature, index) => {
            const Icon = iconMap[feature.icon]
            return (
              <motion.div key={feature.title} initial={{ opacity: 0, y: 16 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.2 }} transition={{ duration: 0.3, delay: index * 0.05 }} className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-lg shadow-slate-950/20">
                <div className="mb-4 inline-flex rounded-2xl bg-sky-500/10 p-3 text-sky-400">
                  <Icon size={22} />
                </div>
                <h3 className="mb-2 text-xl font-semibold text-white">{feature.title}</h3>
                <p className="text-sm leading-7 text-slate-400">{feature.description}</p>
              </motion.div>
            )
          })}
        </div>
      </section>

      <section className="container px-4 py-8 lg:py-16">
        <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
          <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-8">
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">How it works</p>
            <h2 className="mt-3 text-3xl font-semibold text-white">A guided product flow for fast experimentation</h2>
            <p className="mt-4 text-slate-400">This experience demonstrates the product journey without touching a real backend, so the visual flow stays realistic and polished.</p>
          </div>
          <div className="space-y-4">
            {data.steps.map((step, index) => (
              <div key={step.title} className="flex gap-4 rounded-2xl border border-slate-800 bg-slate-900/70 p-5">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-sky-500/15 text-sm font-semibold text-sky-300">0{index + 1}</div>
                <div>
                  <h3 className="font-semibold text-white">{step.title}</h3>
                  <p className="mt-1 text-sm text-slate-400">{step.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
