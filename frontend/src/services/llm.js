export async function callGemini(prompt, apiKey, isJson = false) {
  const model = 'gemini-3.6-flash'
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`

  const requestBody = {
    contents: [{ parts: [{ text: prompt }] }],
  }
  if (isJson) {
    requestBody.generationConfig = { responseMimeType: 'application/json' }
  }

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-goog-api-key': apiKey,
    },
    body: JSON.stringify(requestBody),
  })

  if (!response.ok) {
    const errData = await response.json().catch(() => ({}))
    throw new Error(errData.error?.message || `Gemini API error (HTTP ${response.status})`)
  }

  const data = await response.json()
  const candidate = data.candidates && data.candidates[0]
  if (!candidate || !candidate.content || !candidate.content.parts || !candidate.content.parts[0]) {
    const blockReason = data.promptFeedback?.blockReason
    throw new Error(blockReason ? `Gemini blocked the request (${blockReason})` : 'Gemini returned an empty response.')
  }
  return candidate.content.parts[0].text
}

export async function callOpenAI(prompt, apiKey, isJson = false) {
  const url = 'https://api.openai.com/v1/chat/completions'
  const requestBody = {
    model: 'gpt-4o',
    messages: [{ role: 'user', content: prompt }],
  }
  if (isJson) {
    requestBody.response_format = { type: 'json_object' }
  }

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify(requestBody),
  })

  if (!response.ok) {
    const errData = await response.json().catch(() => ({}))
    throw new Error(errData.error?.message || `OpenAI API error (HTTP ${response.status})`)
  }

  const data = await response.json()
  return data.choices[0].message.content
}

function parseJSON(text) {
  const cleanText = text.replace(/```json\s*|```/g, '').trim()
  return JSON.parse(cleanText)
}

export async function fetchSummaryFromLLM(text, provider, apiKey) {
  const truncatedText = text.substring(0, 15000)
  const prompt = `You are a document analyzer. Summarize the following document.
You MUST return your output STRICTLY in JSON format. Do not write any normal text before or after the JSON.
The format MUST be precisely:
{
  "summary": "a brief executive summary of 2-3 sentences",
  "bullet1_text": "core trend or main finding extracted from document",
  "bullet2_text": "market cap estimation or key statistic from document",
  "bullet3_text": "investment rate or notable data point from document"
}

Document Content:
${truncatedText}`

  let responseText
  if (provider === 'gemini') {
    responseText = await callGemini(prompt, apiKey, true)
  } else {
    responseText = await callOpenAI(prompt, apiKey, true)
  }
  return parseJSON(responseText)
}

export async function fetchChatResponseFromLLM(question, docText, provider, apiKey) {
  const contextLimitText = docText ? docText.substring(0, 25000) : ''

  let prompt
  if (contextLimitText) {
    prompt = `You are a helpful AI assistant analyzing the following document:

--- START DOCUMENT ---
${contextLimitText}
--- END DOCUMENT ---

Using the document content above, answer the user's question.
- If the user asks for a summary or to explain the story/document, summarize it beautifully.
- If the question is a general greeting (like "hi" or "hello"), respond friendly and offer to help with the document.
- If the question is unrelated to the document, answer it naturally but remind them you can help analyze the document.
- If they ask a specific question about the document but the information is not present, explain that politely.

User Question: ${question}`
  } else {
    prompt = `You are a helpful AI assistant. The user has not loaded any document yet.
Politely greet them and ask them to upload a document to get started.

User Question: ${question}`
  }

  if (provider === 'gemini') {
    return await callGemini(prompt, apiKey, false)
  }
  return await callOpenAI(prompt, apiKey, false)
}
