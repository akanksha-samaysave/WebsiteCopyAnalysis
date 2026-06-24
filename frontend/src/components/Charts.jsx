import React from 'react'
import {
  BarChart,
  Bar,
  RadarChart,
  Radar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell
} from 'recharts'

export const RadarChartComponent = ({ data, categories }) => {
  const chartData = categories.map(cat => ({
    category: cat.replace(/_/g, ' ').toUpperCase(),
    value: data[cat] || 0,
    fullMark: 10
  }))

  return (
    <div className="w-full h-64">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={chartData}>
          <CartesianGrid stroke="#475569" />
          <PolarAngleAxis dataKey="category" stroke="#9ca3af" />
          <PolarRadiusAxis angle={90} domain={[0, 10]} stroke="#9ca3af" />
          <Radar name="Score" dataKey="value" stroke="#0ea5e9" fill="#0ea5e9" fillOpacity={0.6} />
          <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  )
}

export const ComparisonBarChart = ({ data, label }) => {
  const colors = ['#0ea5e9', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']

  return (
    <div className="w-full h-80">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 60 }}>
          <CartesianGrid stroke="#475569" strokeDasharray="3 3" />
          <XAxis 
            dataKey="domain" 
            stroke="#9ca3af" 
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis stroke="#9ca3af" domain={[0, 100]} />
          <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }} />
          <Bar dataKey="overall_score" name={label} radius={[8, 8, 0, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export const ScoreDistributionChart = ({ websites }) => {
  const data = websites.map(w => ({
    domain: w.domain.split('.')[0],
    design: w.scores?.design || 0,
    messaging: w.scores?.messaging || 0,
    trust: w.scores?.trust || 0,
    clarity: w.scores?.clarity || 0,
    conversion: w.scores?.conversion || 0,
    ux: w.scores?.ux || 0
  }))

  return (
    <div className="w-full h-80">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 60 }}>
          <CartesianGrid stroke="#475569" strokeDasharray="3 3" />
          <XAxis 
            dataKey="domain"
            stroke="#9ca3af"
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis stroke="#9ca3af" domain={[0, 10]} />
          <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }} />
          <Legend />
          <Bar dataKey="design" fill="#0ea5e9" />
          <Bar dataKey="messaging" fill="#10b981" />
          <Bar dataKey="trust" fill="#f59e0b" />
          <Bar dataKey="clarity" fill="#8b5cf6" />
          <Bar dataKey="conversion" fill="#ec4899" />
          <Bar dataKey="ux" fill="#14b8a6" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
