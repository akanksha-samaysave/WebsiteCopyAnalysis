import React from 'react'
import { TrendingUp } from 'lucide-react'
import { useLocation, useNavigate } from 'react-router-dom'

export const Header = () => {
  const location = useLocation()
  const navigate = useNavigate()

  return (
    <header className="bg-slate-800 border-b border-slate-700 sticky top-0 z-50">
      <div className="container py-4 flex items-center justify-between">
        <div 
          className="flex items-center gap-2 cursor-pointer"
          onClick={() => navigate('/')}
        >
          <TrendingUp className="text-primary-500" size={28} />
          <div>
            <h1 className="text-2xl font-bold">Landing Page Intelligence</h1>
            <p className="text-xs text-gray-400">CRO Analyzer</p>
          </div>
        </div>
        <nav className="flex gap-6">
          <a href="/" className={`text-sm ${location.pathname === '/' ? 'text-primary-400' : 'text-gray-300'} hover:text-white transition`}>
            Analyze
          </a>
          <a href="/dashboard" className={`text-sm ${location.pathname === '/dashboard' ? 'text-primary-400' : 'text-gray-300'} hover:text-white transition`}>
            Dashboard
          </a>
          <a href="/comparison" className={`text-sm ${location.pathname === '/comparison' ? 'text-primary-400' : 'text-gray-300'} hover:text-white transition`}>
            Comparison
          </a>
        </nav>
      </div>
    </header>
  )
}

export const Footer = () => {
  return (
    <footer className="bg-slate-800 border-t border-slate-700 mt-12">
      <div className="container py-8 text-center text-sm text-gray-400">
        <p>&copy; 2024 Landing Page Intelligence. All rights reserved.</p>
      </div>
    </footer>
  )
}
