import { useRef } from 'react'
import {
  FileText, Trash2, LayoutGrid, RotateCcw,
} from 'lucide-react'
import './Sidebar.css'

export default function Sidebar({
  documents, activeDoc, onSelectDoc, onUpload,
  onDeleteDoc, onClearAll, showToast,
}) {
  const fileInputRef = useRef(null)

  return (
    <aside className="sidebar glass">
      <div className="sidebar-top">
        <div className="logo-section">
          <div className="logo-box">O</div>
          <span className="logo-text">OmniChat</span>
        </div>

        <div className="section-title">Upload Source</div>
        <div className="upload-box" onClick={() => fileInputRef.current?.click()}>
          <div className="upload-icon-wrap">
            <FileText size={16} />
          </div>
          <div className="upload-title">Add Media</div>
          <div className="upload-desc">Documents • Images • Audio • Video • Data</div>
        </div>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.doc,.docx,.txt,.md,.rtf,.csv,.tsv,.json,.xlsx,.xls,.png,.jpg,.jpeg,.webp,.bmp,.gif,.mp3,.wav,.m4a,.ogg,.aac,.flac,.mp4,.mkv,.avi,.mov,.webm,.wmv"
          style={{ display: 'none' }}
          multiple
          onChange={(e) => {
            const files = Array.from(e.target.files || [])
            if (!files.length) return
            files.forEach((file) => onUpload(file))
            e.target.value = ''
          }}
        />

        <div className="section-title">Indexed Sources</div>
        <ul className="file-list">
          {documents.length === 0 && (
            <li className="file-item empty">No sources yet</li>
          )}
          {documents.map((doc) => (
            <li
              key={doc.name}
              className={`file-item ${doc.name === activeDoc ? 'active' : ''}`}
              onClick={() => onSelectDoc(doc.name)}
            >
              <div className="file-info">
                <FileText size={14} />
                <span className="file-name" title={doc.name}>{doc.name}</span>
              </div>
              {!doc.isMock && (
                <button
                  className="file-del"
                  onClick={(e) => { e.stopPropagation(); onDeleteDoc(doc.name) }}
                >
                  <Trash2 size={13} />
                </button>
              )}
            </li>
          ))}
        </ul>

        <ul className="nav-list">
          <li className="nav-item active">
            <LayoutGrid size={16} />
            <span>Media Canvas</span>
          </li>
        </ul>
      </div>

      <div className="profile-card">
        <button className="logout-btn" onClick={onClearAll} title="Clear workspace and start fresh">
          <RotateCcw size={16} />
          <span>New Workspace</span>
        </button>
      </div>
    </aside>
  )
}
