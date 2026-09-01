import { Sparkles } from 'lucide-react'

const STEPS = [
  {
    title: 'Upload Source',
    desc: 'Click "Add Media" to upload documents, images, audio, video, or structured data files.',
  },
  {
    title: 'Chat & Analyze',
    desc: 'Ask questions about your file in the chat feed and get AI-powered insights.',
  },
]

export default function WelcomeScreen() {
  return (
    <div className="welcome-screen">
      <div className="welcome-icon">
        <Sparkles size={26} />
      </div>
      <p className="welcome-text">
        Analyze documents, extract key insights, and converse with your files in real time.
        Upload a source file to start with the local OmniChat workflow.
      </p>
      <div className="steps-grid">
        {STEPS.map((step, i) => (
          <div className="step-card" key={step.title}>
            <div className="step-number">{i + 1}</div>
            <div>
              <h4 className="step-title">{step.title}</h4>
              <p className="step-desc">{step.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
