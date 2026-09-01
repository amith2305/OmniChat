import './TypingIndicator.css'

export default function TypingIndicator() {
  return (
    <div className="typing-indicator" aria-label="AI is typing">
      <span className="typing-dot" />
      <span className="typing-dot" />
      <span className="typing-dot" />
    </div>
  )
}
