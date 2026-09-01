import { FileText, ZoomIn, ZoomOut, Share2 } from 'lucide-react'

export default function DocumentHeader({ docName, onZoomIn, onZoomOut, onShare }) {
  return (
    <header className="doc-header">
      <div className="doc-header-left">
        <div className="doc-identity">
          <FileText size={16} className="doc-icon-color" />
          <span className="doc-filename" title={docName}>{docName}</span>
        </div>
        <div className="zoom-controls">
          <button className="zoom-btn" onClick={onZoomOut} title="Zoom Out">
            <ZoomOut size={16} />
          </button>
          <button className="zoom-btn" onClick={onZoomIn} title="Zoom In">
            <ZoomIn size={16} />
          </button>
        </div>
      </div>
      <button className="share-btn" onClick={onShare}>
        <Share2 size={14} />
        Share Insights
      </button>
    </header>
  )
}
