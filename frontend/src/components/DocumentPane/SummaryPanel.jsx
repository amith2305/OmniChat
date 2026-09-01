import { useState } from 'react'
import { Sparkles, ChevronDown, Loader } from 'lucide-react'
import { summarizeDocument } from '../../services/api.js'

export default function SummaryPanel({ doc, showToast }) {
  const [expanded, setExpanded] = useState(true)
  const [generating, setGenerating] = useState(false)
  const [summary, setSummary] = useState(null)

  if (!doc) return null

  const handleGenerateSummary = async () => {
    setGenerating(true)
    try {
      const result = await summarizeDocument(doc.source || doc.name, doc.title || doc.name)
      setSummary(result.summary)
      showToast?.('Summary generated successfully!', 'success')
    } catch (err) {
      showToast?.(`Failed to generate summary: ${err.message}`, 'error')
    } finally {
      setGenerating(false)
    }
  }

  const displaySummary = summary || doc.bullets?.trend || 'Click "Generate Summary" to create an AI summary of this document.'

  return (
    <div className={`summary-panel ${expanded ? 'expanded' : ''}`}>
      <div className="summary-header" onClick={() => setExpanded((e) => !e)}>
        <div className="summary-title-wrapper">
          <Sparkles size={18} className="summary-stars-icon" />
          <span className="summary-title">AI Summary</span>
        </div>
        <ChevronDown size={16} className="summary-toggle-arrow" />
      </div>
      <div className="summary-content">
        <div className="summary-text-area">
          {generating ? (
            <div className="summary-generating">
              <Loader size={16} className="spinner" />
              <span>Generating summary...</span>
            </div>
          ) : (
            <p className="summary-text">{displaySummary}</p>
          )}
        </div>
        <button
          className="summary-generate-btn"
          onClick={handleGenerateSummary}
          disabled={generating}
        >
          {generating ? 'Generating...' : 'Generate Summary'}
        </button>
      </div>
    </div>
  )
}
