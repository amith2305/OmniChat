import DocumentStats from './DocumentStats.jsx'

export default function DocumentSheet({ doc, zoomLevel }) {
  const paragraphs = doc.text.split(/\n\s*\n/).filter((p) => p.trim())

  return (
    <article
      className="document-sheet"
      style={{ transform: `scale(${zoomLevel})`, transformOrigin: 'top center' }}
    >
      <h1 className="sheet-title">{doc.title}</h1>
      <div className="sheet-subtitle">
        <span>Sector:</span>
        <span className="sheet-sector">{doc.sector}</span>
      </div>
      <DocumentStats doc={doc} />
      {paragraphs.map((p, i) => (
        <p key={i} className="sheet-paragraph">{p.trim()}</p>
      ))}
    </article>
  )
}
