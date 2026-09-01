import { useState, useCallback } from 'react'

const MIN_ZOOM = 0.85
const MAX_ZOOM = 1.3
const ZOOM_STEP = 0.1

export function useDocumentZoom() {
  const [zoomLevel, setZoomLevel] = useState(1)

  const zoomIn = useCallback(() => {
    setZoomLevel((zoom) => Math.min(zoom + ZOOM_STEP, MAX_ZOOM))
  }, [])

  const zoomOut = useCallback(() => {
    setZoomLevel((zoom) => Math.max(zoom - ZOOM_STEP, MIN_ZOOM))
  }, [])

  const resetZoom = useCallback(() => {
    setZoomLevel(1)
  }, [])

  return { zoomLevel, zoomIn, zoomOut, resetZoom }
}
