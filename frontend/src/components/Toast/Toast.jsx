import { CheckCircle, AlertCircle } from 'lucide-react'
import './Toast.css'

export default function Toast({ message, type, visible }) {
  return (
    <div className={`toast ${visible ? 'show' : ''} ${type === 'error' ? 'error' : ''}`}>
      {type === 'error' ? <AlertCircle size={16} /> : <CheckCircle size={16} />}
      <span>{message}</span>
    </div>
  )
}
