import { useState, useCallback } from 'react'
import { getStoredModel, storeModel } from '../services/storage.js'

export function useModel() {
  const [modelProvider, setModelProvider] = useState(getStoredModel())

  const changeModel = useCallback((provider) => {
    setModelProvider(provider)
    storeModel(provider)
  }, [])

  const resetModel = useCallback(() => {
    changeModel('gemini')
  }, [changeModel])

  return { modelProvider, changeModel, resetModel }
}
