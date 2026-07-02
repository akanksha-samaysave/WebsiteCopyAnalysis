import React from 'react'
import { motion } from 'framer-motion'
import { Code2, Search } from 'lucide-react'
import apiDocs from '../data/apiDocs.json'

export const ApiDocsPage = () => {
  return (
    <div className="container px-4 py-12 lg:py-16">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35 }} className="rounded-3xl border border-slate-800 bg-slate-900/70 p-8 shadow-2xl shadow-slate-950/30">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">API documentation</p>
            <h1 className="mt-2 text-3xl font-semibold text-white">Swagger-style reference for the demo product</h1>
          </div>
          <div className="rounded-full border border-slate-700 bg-slate-950/70 px-4 py-2 text-sm text-slate-300">Mock endpoints only</div>
        </div>

        <div className="mt-8 space-y-6">
          {apiDocs.endpoints.map((endpoint) => (
            <div key={endpoint.path} className="rounded-2xl border border-slate-800 bg-slate-950/70 p-6">
              <div className="flex flex-wrap items-center gap-3">
                <span className="rounded-full bg-sky-500/10 px-3 py-1 text-sm font-semibold text-sky-300">{endpoint.method}</span>
                <span className="text-lg font-semibold text-white">{endpoint.path}</span>
                <span className="text-sm text-slate-400">{endpoint.status}</span>
              </div>
              <p className="mt-3 text-sm leading-7 text-slate-400">{endpoint.description}</p>

              <div className="mt-6 grid gap-6 lg:grid-cols-2">
                <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-4">
                  <div className="mb-3 flex items-center gap-2 text-sky-300">
                    <Code2 size={16} />
                    <p className="text-sm font-semibold uppercase tracking-[0.3em]">Request</p>
                  </div>
                  <pre className="overflow-x-auto text-sm text-slate-300">{JSON.stringify(endpoint.request, null, 2)}</pre>
                </div>
                <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-4">
                  <div className="mb-3 flex items-center gap-2 text-emerald-300">
                    <Search size={16} />
                    <p className="text-sm font-semibold uppercase tracking-[0.3em]">Response</p>
                  </div>
                  <pre className="overflow-x-auto text-sm text-slate-300">{JSON.stringify(endpoint.response, null, 2)}</pre>
                </div>
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  )
}
