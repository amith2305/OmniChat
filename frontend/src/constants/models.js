export const MODEL_OPTIONS = [
  { id: 'gemini', label: 'Gemini 3.6 Flash', shortLabel: 'Gemini 3.6' },
  { id: 'gpt4', label: 'GPT-4o', shortLabel: 'GPT-4o' },
  { id: 'sonnet', label: 'Claude 3.5 Sonnet', shortLabel: 'Claude 3.5' },
]

export const API_KEY_LABELS = {
  gemini: 'Gemini API Key',
  gpt4: 'OpenAI API Key',
  sonnet: 'Claude API Key',
}

export function getModelOption(provider) {
  return MODEL_OPTIONS.find((m) => m.id === provider) || MODEL_OPTIONS[0]
}
