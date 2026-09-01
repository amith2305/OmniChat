const loadedScripts = {}

export const PDFJS_SRC = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.min.js'
export const PDFJS_WORKER_SRC = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.worker.min.js'
export const MAMMOTH_SRC = 'https://cdnjs.cloudflare.com/ajax/libs/mammoth/1.6.0/mammoth.browser.min.js'

function loadScript(src) {
  return new Promise((resolve, reject) => {
    if (loadedScripts[src]) {
      resolve()
      return
    }
    const existing = document.querySelector(`script[src="${src}"]`)
    if (existing) {
      existing.addEventListener('load', () => {
        loadedScripts[src] = true
        resolve()
      })
      existing.addEventListener('error', () => reject(new Error(`Failed to load library: ${src}`)))
      return
    }

    const script = document.createElement('script')
    script.src = src
    script.async = true
    script.onload = () => {
      loadedScripts[src] = true
      resolve()
    }
    script.onerror = () => reject(new Error(`Failed to load library: ${src}`))
    document.head.appendChild(script)
  })
}

export async function loadDocumentLibraries() {
  await Promise.all([loadScript(PDFJS_SRC), loadScript(MAMMOTH_SRC)])
  if (window.pdfjsLib) {
    window.pdfjsLib.GlobalWorkerOptions.workerSrc = PDFJS_WORKER_SRC
  }
}
