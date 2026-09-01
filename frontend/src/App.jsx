import { useEffect } from 'react'
import Sidebar from './components/Sidebar/Sidebar.jsx'
import DocumentPane from './components/DocumentPane/DocumentPane.jsx'
import ChatPane from './components/ChatPane/ChatPane.jsx'
import Toast from './components/Toast/Toast.jsx'
import { useToast } from './hooks/useToast.js'
import { useDocuments } from './hooks/useDocuments.js'
import { useChat } from './hooks/useChat.js'
import { useModel } from './hooks/useModel.js'
import { loadDocumentLibraries } from './services/libraryLoader.js'
import { clearAll } from './services/storage.js'

export default function App() {
  const { toast, showToast } = useToast()
  const { modelProvider, changeModel, resetModel } = useModel()

  const {
    documents,
    activeDoc,
    activeDocument,
    loading,
    loaderText,
    uploadFile,
    deleteDocument,
    clearDocuments,
    setActiveDoc,
  } = useDocuments(showToast)

  const { messages, isTyping, sendMessage, clearMessages } = useChat(activeDocument)

  useEffect(() => {
    loadDocumentLibraries().catch(() => {
      showToast('Failed to load document parsing libraries.', 'error')
    })
  }, [showToast])

  function handleUpload(file) {
    uploadFile(file, modelProvider)
  }

  function handleClearAll() {
    if (!window.confirm('Are you sure you want to reset all document workspaces and settings?')) {
      return
    }
    clearAll()
    resetModel()
    clearDocuments()
    clearMessages()
    showToast('Workspace fully reset!')
  }

  return (
    <div className="app-container">
      <div className="bg-orb orb-1" />
      <div className="bg-orb orb-2" />
      <div className="bg-orb orb-3" />

      <Sidebar
        documents={documents}
        activeDoc={activeDoc}
        onSelectDoc={setActiveDoc}
        onUpload={handleUpload}
        onDeleteDoc={deleteDocument}
        onClearAll={handleClearAll}
        showToast={showToast}
      />

      <DocumentPane
        activeDocument={activeDocument}
        loading={loading}
        loaderText={loaderText}
        showToast={showToast}
      />

      <ChatPane
        messages={messages}
        isTyping={isTyping}
        onSend={(text) => sendMessage(text, modelProvider)}
        modelProvider={modelProvider}
        showToast={showToast}
      />

      <Toast message={toast.message} type={toast.type} visible={toast.visible} />
    </div>
  )
}
