export default function LoadingOverlay({ active, text }) {
  return (
    <div className={`viewer-loading-overlay ${active ? 'active' : ''}`}>
      <div className="spinner" />
      <div className="loader-text">{text}</div>
    </div>
  )
}
