export function parseTxtFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => resolve(e.target.result)
    reader.onerror = () => reject(new Error('Error reading text file.'))
    reader.readAsText(file)
  })
}

export function parsePdfFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = async (e) => {
      try {
        const typedarray = new Uint8Array(e.target.result)
        const pdfjsLib = window.pdfjsLib
        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.worker.min.js'
        const pdf = await pdfjsLib.getDocument(typedarray).promise
        let text = ''
        for (let i = 1; i <= pdf.numPages; i++) {
          const page = await pdf.getPage(i)
          const content = await page.getTextContent()
          text += content.items.map(item => item.str).join(' ') + '\n'
        }
        resolve(text)
      } catch (err) {
        reject(new Error('Error parsing PDF document: ' + err.message))
      }
    }
    reader.onerror = () => reject(new Error('Error loading file bytes.'))
    reader.readAsArrayBuffer(file)
  })
}

export function parseDocxFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      const arrayBuffer = e.target.result
      window.mammoth.extractRawText({ arrayBuffer })
        .then((result) => resolve(result.value))
        .catch((err) => reject(new Error('Mammoth DOCX extract failed: ' + err.message)))
    }
    reader.onerror = () => reject(new Error('Error loading file bytes.'))
    reader.readAsArrayBuffer(file)
  })
}

export async function parseFile(file) {
  const extension = file.name.split('.').pop().toLowerCase()

  const textLikeExtensions = new Set(['txt', 'md', 'rtf', 'csv', 'tsv', 'json'])
  const searchableTextExtensions = new Set(['pdf', 'docx'])

  let extractedText = ''

  if (textLikeExtensions.has(extension)) {
    extractedText = await parseTxtFile(file)
  } else if (searchableTextExtensions.has(extension)) {
    if (extension === 'pdf') extractedText = await parsePdfFile(file)
    if (extension === 'docx') extractedText = await parseDocxFile(file)
  } else {
    return {
      name: file.name,
      title: file.name.replace(/\.[^/.]+$/, ''),
      sector: `Queued for backend processing`,
      text: `File received: ${file.name}. The backend will process this media type and index it for chat analysis.`,
      wordCount: 0,
      charCount: file.name.length,
    }
  }

  if (extractedText && !extractedText.trim()) {
    throw new Error('Failed to extract readable text content from the file.')
  }

  const textContent = extractedText || `File received: ${file.name}. The backend will process this media type and index it for chat analysis.`
  const wordCount = textContent.trim() ? textContent.trim().split(/\s+/).length : 0

  return {
    name: file.name,
    title: file.name.replace(/\.[^/.]+$/, ''),
    sector: `Uploaded ${extension.toUpperCase()} File`,
    text: textContent,
    wordCount,
    charCount: textContent.length,
  }
}
