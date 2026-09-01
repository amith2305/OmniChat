import { useDocumentZoom } from '../../hooks/useDocumentZoom.js'
import DocumentHeader from './DocumentHeader.jsx'
import DocumentSheet from './DocumentSheet.jsx'
import SummaryPanel from './SummaryPanel.jsx'
import WelcomeScreen from './WelcomeScreen.jsx'
import LoadingOverlay from './LoadingOverlay.jsx'
import './DocumentPane.css'

export default function DocumentPane({ activeDocument, loading, loaderText, showToast }) {
  const { zoomLevel, zoomIn, zoomOut } = useDocumentZoom()

  function handleShare() {
    navigator.clipboard
      .writeText(window.location.href)
      .then(() => showToast('Workspace sharing link copied to clipboard!'))
      .catch(() => showToast('Copied Insights URL!'))
  }

  return (
    <main className="document-pane">
      <DocumentHeader
        docName={activeDocument ? activeDocument.name : 'No document selected'}
        onZoomIn={zoomIn}
        onZoomOut={zoomOut}
        onShare={handleShare}
      />
      <div className="doc-viewer-body">
        {activeDocument ? (
          <DocumentSheet doc={activeDocument} zoomLevel={zoomLevel} />
        ) : (
          <WelcomeScreen />
        )}
      </div>
      {activeDocument && <SummaryPanel doc={activeDocument} showToast={showToast} />}
      <LoadingOverlay active={loading} text={loaderText} />
    </main>
  )
}
