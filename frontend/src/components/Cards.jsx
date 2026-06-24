import React from 'react'
import { AlertCircle } from 'lucide-react'

export const ScoreCard = ({ label, score, max = 10 }) => {
  const percentage = (score / max) * 100
  const color = percentage >= 80 ? 'bg-green-500' : percentage >= 60 ? 'bg-yellow-500' : 'bg-red-500'

  return (
    <div className="card p-6">
      <h3 className="text-sm font-semibold text-gray-300 mb-4">{label}</h3>
      <div className="flex items-center justify-between mb-3">
        <span className="text-3xl font-bold">{score.toFixed(1)}</span>
        <span className="text-sm text-gray-400">/{max}</span>
      </div>
      <div className="w-full bg-slate-700 rounded-full h-2">
        <div className={`${color} h-2 rounded-full transition-all duration-300`} style={{ width: `${percentage}%` }}></div>
      </div>
    </div>
  )
}

export const StatCard = ({ title, value, subtitle }) => {
  return (
    <div className="card p-6">
      <h3 className="text-sm font-semibold text-gray-300 mb-2">{title}</h3>
      <p className="text-3xl font-bold mb-1">{value}</p>
      {subtitle && <p className="text-xs text-gray-400">{subtitle}</p>}
    </div>
  )
}

export const RecommendationCard = ({ priority, title, description, reasoning }) => {
  const priorityColors = {
    High: 'bg-red-500/20 border-red-500',
    Medium: 'bg-yellow-500/20 border-yellow-500',
    Low: 'bg-blue-500/20 border-blue-500'
  }

  return (
    <div className={`card p-4 border ${priorityColors[priority] || priorityColors.Medium}`}>
      <div className="flex items-start justify-between mb-2">
        <h4 className="font-semibold text-white">{title}</h4>
        <span className={`text-xs font-bold px-2 py-1 rounded ${
          priority === 'High' ? 'bg-red-500' : priority === 'Medium' ? 'bg-yellow-500' : 'bg-blue-500'
        }`}>
          {priority}
        </span>
      </div>
      <p className="text-sm text-gray-300 mb-2">{description}</p>
      {reasoning && <p className="text-xs text-gray-400">💡 {reasoning}</p>}
    </div>
  )
}

export const ErrorAlert = ({ message }) => {
  return (
    <div className="card border-red-500 bg-red-500/10 p-4 flex items-start gap-3">
      <AlertCircle className="text-red-500 flex-shrink-0 mt-0.5" size={20} />
      <div>
        <h3 className="font-semibold text-red-500">Error</h3>
        <p className="text-sm text-gray-300">{message}</p>
      </div>
    </div>
  )
}

export const LoadingSpinner = () => {
  return (
    <div className="flex items-center justify-center py-12">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
    </div>
  )
}
