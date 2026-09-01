import { formatNumber } from '../../utils/formatting.js'

export default function DocumentStats({ doc }) {
  return (
    <div className="sheet-grid-highlights">
      <div className="highlight-card">
        <div className="highlight-lbl">Word Count</div>
        <div className="highlight-val">{formatNumber(doc.wordCount)}</div>
      </div>
      <div className="highlight-card">
        <div className="highlight-lbl">Character Count</div>
        <div className="highlight-val">{formatNumber(doc.charCount)}</div>
      </div>
    </div>
  )
}
