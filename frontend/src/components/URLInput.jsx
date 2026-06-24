import React, { useState } from 'react'
import { Trash2, Plus } from 'lucide-react'

export const URLInput = ({ onAnalyze, loading }) => {
  const [urls, setUrls] = useState([''])

  const handleAddUrl = () => {
    if (urls.length < 5) {
      setUrls([...urls, ''])
    }
  }

  const handleRemoveUrl = (index) => {
    if (urls.length > 1) {
      setUrls(urls.filter((_, i) => i !== index))
    }
  }

  const handleUrlChange = (index, value) => {
    const newUrls = [...urls]
    newUrls[index] = value
    setUrls(newUrls)
  }

  const handleSubmit = () => {
    const validUrls = urls.filter(url => url.trim())
    if (validUrls.length > 0) {
      onAnalyze(validUrls)
    }
  }

  return (
    <div className="card p-8 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Analyze Landing Pages</h2>
      <p className="text-gray-300 mb-6">Enter up to 5 landing page URLs to analyze:</p>
      
      <div className="space-y-3 mb-6">
        {urls.map((url, index) => (
          <div key={index} className="flex gap-2">
            <input
              type="url"
              value={url}
              onChange={(e) => handleUrlChange(index, e.target.value)}
              placeholder="https://example.com"
              className="input flex-1"
              disabled={loading}
            />
            {urls.length > 1 && (
              <button
                onClick={() => handleRemoveUrl(index)}
                className="btn btn-secondary p-2"
                disabled={loading}
              >
                <Trash2 size={20} />
              </button>
            )}
          </div>
        ))}
      </div>

      {urls.length < 5 && (
        <button
          onClick={handleAddUrl}
          className="btn btn-secondary mb-6 flex items-center gap-2"
          disabled={loading}
        >
          <Plus size={20} />
          Add URL
        </button>
      )}

      <button
        onClick={handleSubmit}
        className="btn btn-primary w-full text-lg py-3 font-bold"
        disabled={loading || urls.every(u => !u.trim())}
      >
        {loading ? 'Analyzing...' : 'Start Analysis'}
      </button>
    </div>
  )
}
