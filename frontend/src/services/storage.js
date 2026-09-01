const KEYS = {
  GEMINI: 'gemini_api_key',
  OPENAI: 'openai_api_key',
  CLAUDE: 'claude_api_key',
}

const MODEL_KEY = 'omnichat_model_provider'

export function getStoredModel() {
  return localStorage.getItem(MODEL_KEY) || 'gemini'
}

export function storeModel(provider) {
  localStorage.setItem(MODEL_KEY, provider)
}

export function getApiKey(provider) {
  const keyMap = {
    gemini: KEYS.GEMINI,
    gpt4: KEYS.OPENAI,
    sonnet: KEYS.CLAUDE,
  }
  return localStorage.getItem(keyMap[provider]) || ''
}

export function setApiKey(provider, key) {
  const keyMap = {
    gemini: KEYS.GEMINI,
    gpt4: KEYS.OPENAI,
    sonnet: KEYS.CLAUDE,
  }
  localStorage.setItem(keyMap[provider], key)
}

export function clearAll() {
  localStorage.clear()
}
