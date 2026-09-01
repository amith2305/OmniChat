const API_BASE = ''

async function apiFetch(path, options = {}) {
  const headers = new Headers(options.headers || {})
  const isFormData = options.body instanceof FormData

  if (!isFormData && !headers.has('Content-Type') && options.body) {
    headers.set('Content-Type', 'application/json')
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    const text = await response.text()
    let errMessage = 'Request failed'
    try {
      const payload = JSON.parse(text)
      errMessage = payload.detail || payload.error || payload.message || errMessage
    } catch {
      errMessage = text || errMessage
    }
    throw new Error(errMessage)
  }

  if (response.status === 204) return null
  const contentType = response.headers.get('content-type') || ''
  if (contentType.includes('application/json')) {
    return response.json()
  }
  return response.text()
}

export async function uploadDocument(file) {
  const formData = new FormData()
  formData.append('file', file)
  return apiFetch('/api/upload', {
    method: 'POST',
    body: formData,
  })
}

export async function listDocuments() {
  const data = await apiFetch('/api/files')
  return data?.sources || []
}

export async function deleteDocumentBySource(source) {
  return apiFetch(`/api/files/${encodeURIComponent(source)}`, {
    method: 'DELETE',
  })
}

export async function chatWithDocument(question, source, sessionId = null) {
  return apiFetch('/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      question,
      source: source || null,
      session_id: sessionId,
    }),
  })
}

export async function getChatHistory(sessionId) {
  return apiFetch(`/api/history?session_id=${encodeURIComponent(sessionId)}`)
}

export async function resetChatHistory(sessionId) {
  return apiFetch('/api/history/reset', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ session_id: sessionId }),
  })
}

export async function checkBackendHealth() {
  return apiFetch('/api/health')
}

export async function summarizeDocument(source, title = null) {
  return apiFetch('/api/summarize', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      source,
      title: title || source,
    }),
  })
}
