import { useState, useCallback, useRef } from 'react'

export function useVoiceInput(onTranscript, showToast) {
  const [isListening, setIsListening] = useState(false)
  const recognitionRef = useRef(null)

  const ensureRecognition = useCallback(() => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SR) return null
    if (recognitionRef.current) return recognitionRef.current

    const recognition = new SR()
    recognition.continuous = false
    recognition.interimResults = false
    recognition.lang = 'en-US'

    recognition.onstart = () => setIsListening(true)
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript
      onTranscript?.(transcript)
    }
    recognition.onerror = (event) => {
      showToast?.('Voice input error: ' + event.error, 'error')
    }
    recognition.onend = () => setIsListening(false)

    recognitionRef.current = recognition
    return recognition
  }, [onTranscript, showToast])

  const toggleListening = useCallback(() => {
    const recognition = ensureRecognition()
    if (!recognition) {
      showToast?.('Speech recognition is not supported in this browser.', 'error')
      return
    }
    if (isListening) {
      recognition.stop()
    } else {
      recognition.start()
    }
  }, [ensureRecognition, isListening, showToast])

  return { isListening, toggleListening }
}
