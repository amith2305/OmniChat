import { Sparkles } from 'lucide-react'
import { formatTime } from '../../utils/formatting.js'

export default function ChatBubble({ message, modelLabel }) {
  const isUser = message.role === 'user'

  if (isUser) {
    return (
      <div className="chat-bubble-row user">
        <div className="bubble-user">{message.text}</div>
        <span className="bubble-time">{formatTime(message.time)}</span>
      </div>
    )
  }

  return (
    <div className="chat-bubble-row ai">
      <div className="ai-header">
        <div className="ai-avatar">
          <Sparkles size={14} />
        </div>
        <span className="ai-name">{modelLabel}</span>
      </div>
      <div className="bubble-ai">
        {message.text.split('\n').map((line, i) => (
          <p key={i}>{line || '\u00A0'}</p>
        ))}
      </div>
      <span className="bubble-time">{formatTime(message.time)}</span>
    </div>
  )
}
