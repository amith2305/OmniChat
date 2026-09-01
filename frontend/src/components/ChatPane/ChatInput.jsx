import { Mic, MicOff, ArrowUp } from 'lucide-react'

export default function ChatInput({ value, onChange, onSend, isListening, onToggleVoice }) {
  function handleSubmit() {
    if (!value.trim()) return
    onSend(value.trim())
    onChange('')
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter') handleSubmit()
  }

  return (
    <div className="chat-input-bar">
      <div className="chat-input-pill">
        <input
          type="text"
          className="chat-text-input"
          placeholder={isListening ? 'Listening...' : 'Ask about the document...'}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button
          className={`chat-input-pill-btn mic-btn ${isListening ? 'listening' : ''}`}
          onClick={onToggleVoice}
          title="Use voice input"
        >
          {isListening ? <MicOff size={16} /> : <Mic size={16} />}
        </button>
        <button className="chat-input-pill-btn send-btn" onClick={handleSubmit} title="Send question">
          <ArrowUp size={16} />
        </button>
      </div>
      <div className="chat-disclaimer">AI can make mistakes. Verify information.</div>
    </div>
  )
}
