import React, { useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { HomePage, DashboardPage, ComparisonPage } from './pages'
import { Header, Footer } from './components'
import { analysisService } from './services/api'

function App() {
  useEffect(() => {
    // Check API health on startup
    analysisService.healthCheck().catch(err => console.error('API not available:', err))
  }, [])

  return (
    <BrowserRouter>
      <div className="flex flex-col min-h-screen bg-dark-900">
        <Header />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/comparison" element={<ComparisonPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  )
}

export default App