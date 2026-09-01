import { useEffect, useRef, useState } from 'react'
import { Sparkles } from 'lucide-react'
import ChatBubble from './ChatBubble.jsx'
import ChatInput from './ChatInput.jsx'
import TypingIndicator from './TypingIndicator.jsx'
import { getModelOption } from '../../constants/models.js'
import { useVoiceInput } from '../../hooks/useVoiceInput.js'
import './ChatPane.css'

export default function ChatPane({ messages, isTyping, onSend, modelProvider, showToast }) {
  const [inputValue, setInputValue] = useState('')
  const scrollRef = useRef(null)

  const modelLabel = `${getModelOption(modelProvider).shortLabel} Assistant`

  const { isListening, toggleListening } = useVoiceInput(
    (transcript) => setInputValue(transcript),
    showToast,
  )

  useEffect(() => {
    const el = scrollRef.current
    if (el) el.scrollTop = el.scrollHeight
  }, [messages, isTyping])

  const hasMessages = messages.length > 0

  return (
    <section className="chat-pane">
      <header className="chat-header-pane">
        <div className="chat-title-wrapper">
          <span className="chat-status-dot" />
          <h2 className="chat-title-text">Chat Analysis</h2>
        </div>
      </header>

      <div className="chat-messages-container" ref={scrollRef}>
        {!hasMessages && (
          <div className="chat-bubble-row ai">
            <div className="ai-header">
              <div className="ai-avatar">
                <Sparkles size={14} />
              </div>
              <span className="ai-name">{modelLabel}</span>
            </div>
            <div className="bubble-ai">
              <p>Hello! Welcome to OmniChat.</p>
              <p>
                Configure your API Key in the left sidebar and upload a source document (PDF, TXT,
                or DOCX) in the Sources area to get started. Once uploaded, you can ask questions
                about your file here!
              </p>
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <ChatBubble key={i} message={msg} modelLabel={modelLabel} />
        ))}

        {isTyping && (
          <div className="chat-bubble-row ai">
            <div className="ai-header">
              <div className="ai-avatar">
                <Sparkles size={14} />
              </div>
              <span className="ai-name">{modelLabel}</span>
            </div>
            <div className="bubble-ai typing-bubble">
              <TypingIndicator />
            </div>
          </div>
        )}
      </div>

      <ChatInput
        value={inputValue}
        onChange={setInputValue}
        onSend={onSend}
        isListening={isListening}
        onToggleVoice={toggleListening}
      />
    </section>
  )
}
