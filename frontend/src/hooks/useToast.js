import { useState, useCallback, useRef } from 'react'

export function useToast() {
  const [toast, setToast] = useState({ message: '', type: 'success', visible: false })
  const timerRef = useRef(null)

  const showToast = useCallback((message, type = 'success') => {
    if (timerRef.current) clearTimeout(timerRef.current)
    setToast({ message, type, visible: true })
    timerRef.current = setTimeout(() => {
      setToast((prev) => ({ ...prev, visible: false }))
    }, 4000)
  }, [])

  return { toast, showToast }
}
