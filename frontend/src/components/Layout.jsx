import React, { useEffect, useState } from 'react'
import { MoonStar, SunMedium, TrendingUp } from 'lucide-react'
import { Link, useLocation, useNavigate } from 'react-router-dom'

const navItems = [
  { to: '/', label: 'Home' },
  { to: '/analyze', label: 'Analyze' },
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/report', label: 'Report' },
  { to: '/api-docs', label: 'API Docs' },
]

export const Header = () => {
  const location = useLocation()
  const navigate = useNavigate()
  const [theme, setTheme] = useState('dark')

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark')
  }, [theme])

  return (
    <header className="sticky top-0 z-50 border-b border-slate-800/80 bg-slate-950/80 backdrop-blur">
      <div className="container flex flex-wrap items-center justify-between gap-4 py-4">
        <div className="flex cursor-pointer items-center gap-3" onClick={() => navigate('/')}>
          <div className="rounded-2xl bg-sky-500/10 p-2 text-sky-400">
            <TrendingUp size={22} />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-white">Landing Page Intelligence</h1>
            <p className="text-xs text-slate-400">CRO Analyzer</p>
          </div>
        </div>

        <nav className="flex flex-wrap items-center gap-2">
          {navItems.map((item) => (
            <Link key={item.to} to={item.to} className={`rounded-full px-3 py-2 text-sm transition ${location.pathname === item.to ? 'bg-slate-800 text-white' : 'text-slate-300 hover:bg-slate-900 hover:text-white'}`}>
              {item.label}
            </Link>
          ))}
          <button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')} className="ml-2 rounded-full border border-slate-700 bg-slate-900 p-2 text-slate-200 transition hover:border-slate-500">
            {theme === 'dark' ? <SunMedium size={16} /> : <MoonStar size={16} />}
          </button>
        </nav>
      </div>
    </header>
  )
}

export const Footer = () => {
  return (
    <footer className="border-t border-slate-800 bg-slate-950/80">
      <div className="container flex flex-col gap-2 py-8 text-center text-sm text-slate-400 md:flex-row md:items-center md:justify-between">
        <p>&copy; 2026 Landing Page Intelligence. Designed for mock product storytelling.</p>
        <p>React, Tailwind, Framer Motion, and Lucide React.</p>
      </div>
    </footer>
  )
}
