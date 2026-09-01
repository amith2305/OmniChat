import { useState } from 'react'
import { X } from 'lucide-react'
import { getApiKey, setApiKey } from '../../services/storage.js'
import './SettingsModal.css'

export default function SettingsModal({ open, onClose, onSave }) {
  const [geminiKey, setGeminiKey] = useState(getApiKey('gemini'))
  const [openaiKey, setOpenaiKey] = useState(getApiKey('gpt4'))

  function handleSave() {
    setApiKey('gemini', geminiKey.trim())
    setApiKey('gpt4', openaiKey.trim())
    onSave?.()
    onClose()
  }

  if (!open) return null

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="settings-modal glass" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3 className="modal-title">System & API Settings</h3>
          <button className="close-btn" onClick={onClose}>
            <X size={18} />
          </button>
        </div>
        <div className="modal-body">
          <div className="settings-group">
            <label className="settings-label">Gemini API Key</label>
            <input
              type="password"
              className="settings-input"
              placeholder="Enter Gemini API Key..."
              value={geminiKey}
              onChange={(e) => setGeminiKey(e.target.value)}
            />
          </div>
          <div className="settings-group">
            <label className="settings-label">OpenAI API Key</label>
            <input
              type="password"
              className="settings-input"
              placeholder="Enter OpenAI API Key..."
              value={openaiKey}
              onChange={(e) => setOpenaiKey(e.target.value)}
            />
          </div>
        </div>
        <div className="modal-footer">
          <button className="btn-secondary" onClick={onClose}>Cancel</button>
          <button className="btn-primary" onClick={handleSave}>Save Settings</button>
        </div>
      </div>
    </div>
  )
}
