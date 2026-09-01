import { useState, useCallback } from 'react'
import { chatWithDocument } from '../services/api.js'

export function useChat(activeDocument) {
  const [messages, setMessages] = useState([])
  const [isTyping, setIsTyping] = useState(false)

  const sendMessage = useCallback(async (text, modelProvider) => {
    if (!text.trim()) return

    const userMsg = { role: 'user', text: text.trim(), time: new Date() }
    setMessages((prev) => [...prev, userMsg])
    setIsTyping(true)

    try {
      const source = activeDocument?.source || activeDocument?.name || null
      const sessionId = activeDocument?.sessionId || null
      const result = await chatWithDocument(text, source, sessionId)
      const responseText = result?.answer || 'No answer returned by the backend.'
      const aiMsg = { role: 'ai', text: responseText, time: new Date() }
      setMessages((prev) => [...prev, aiMsg])
    } catch (err) {
      const errMsg = {
        role: 'ai',
        text: `Backend error: ${err.message}`,
        time: new Date(),
      }
      setMessages((prev) => [...prev, errMsg])
    } finally {
      setIsTyping(false)
    }
  }, [activeDocument])

  const clearMessages = useCallback(() => {
    setMessages([])
  }, [])

  return { messages, isTyping, sendMessage, clearMessages }
}
