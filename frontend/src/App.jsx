import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { HomePage, AnalysisPage, DashboardPage, ReportPage, ApiDocsPage } from './pages'
import { Header, Footer } from './components'

function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen flex-col bg-slate-950 text-slate-100">
        <Header />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/analyze" element={<AnalysisPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/report" element={<ReportPage />} />
            <Route path="/api-docs" element={<ApiDocsPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  )
}

export default App