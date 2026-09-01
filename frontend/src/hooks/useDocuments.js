import { useState, useCallback, useEffect } from 'react'
import { parseFile } from '../services/documentParser.js'
import { deleteDocumentBySource, listDocuments, uploadDocument } from '../services/api.js'

function buildDocFromUpload(parsed, source, file) {
  const preview = parsed.text || ''
  const summaryText = preview.trim().slice(0, 260) || 'Document uploaded and indexed successfully.'
  return {
    name: file.name,
    title: parsed.title,
    sector: parsed.sector,
    text: preview,
    wordCount: parsed.wordCount,
    charCount: parsed.charCount,
    source,
    sessionId: null,
    summary: summaryText,
    bullets: {
      trend: 'Document uploaded and indexed successfully.',
      cap: 'AI summary will appear once the backend finishes processing.',
      invest: 'Use the chat panel to ask questions about this document.',
    },
  }
}

export function useDocuments(showToast) {
  const [documents, setDocuments] = useState([])
  const [activeDoc, setActiveDoc] = useState(null)
  const [loading, setLoading] = useState(false)
  const [loaderText, setLoaderText] = useState('')

  const refreshDocuments = useCallback(async () => {
    try {
      const sources = await listDocuments()
      const mapped = sources.map((sourceInfo) => {
        const rawSource = sourceInfo.source || ''
        const displayName = rawSource.includes('_') ? rawSource.split('_').slice(1).join('_') : rawSource
        const title = displayName ? displayName.replace(/\.[^/.]+$/, '') : 'Uploaded Document'
        return {
          name: displayName || rawSource,
          title,
          sector: 'Uploaded Document',
          text: '',
          source: rawSource,
          wordCount: 0,
          charCount: 0,
          summary: 'Document is available in the backend. Ask a question to analyze it.',
          bullets: {
            trend: 'Backend indexing complete.',
            cap: 'The document is ready for RAG chat.',
            invest: 'Open the document in the chat panel to use it.',
          },
        }
      })
      setDocuments((prev) => {
        if (!mapped.length) return prev
        const next = [...prev]
        mapped.forEach((doc) => {
          const exists = next.findIndex((item) => item.source === doc.source || item.name === doc.name)
          if (exists >= 0) next[exists] = { ...next[exists], ...doc }
          else next.push(doc)
        })
        return next
      })
    } catch {
      // backend is optional at page load; the UI can still function with local uploads.
    }
  }, [])

  useEffect(() => {
    refreshDocuments()
  }, [refreshDocuments])

  const activeDocument = documents.find((d) => d.name === activeDoc) || null

  const uploadFile = useCallback(async (file, modelProvider) => {
    setLoading(true)
    setLoaderText(`Reading ${file.name}...`)
    try {
      const parsed = await parseFile(file)
      setLoaderText('Uploading document to backend...')
      const result = await uploadDocument(file)
      const doc = buildDocFromUpload(parsed, result?.source || file.name, file)
      const uploadedName = doc.name

      setDocuments((prev) => {
        const idx = prev.findIndex((d) => d.name === uploadedName)
        if (idx !== -1) {
          const updated = [...prev]
          updated[idx] = { ...updated[idx], ...doc }
          return updated
        }
        return [...prev, doc]
      })
      setActiveDoc(uploadedName)

      showToast('Document uploaded and queued for analysis.', 'success')
      await refreshDocuments()
    } catch (err) {
      showToast(err.message, 'error')
    } finally {
      setLoading(false)
    }
  }, [refreshDocuments, showToast])

  const deleteDocument = useCallback(async (name) => {
    const target = documents.find((doc) => doc.name === name)
    if (target?.source) {
      try {
        await deleteDocumentBySource(target.source)
      } catch (err) {
        showToast(err.message, 'error')
      }
    }
    setDocuments((prev) => prev.filter((d) => d.name !== name))
    setActiveDoc((prev) => (prev === name ? null : prev))
  }, [documents, showToast])

  const clearDocuments = useCallback(() => {
    setDocuments([])
    setActiveDoc(null)
  }, [])

  return {
    documents,
    activeDoc,
    activeDocument,
    loading,
    loaderText,
    uploadFile,
    deleteDocument,
    clearDocuments,
    setActiveDoc,
  }
}
