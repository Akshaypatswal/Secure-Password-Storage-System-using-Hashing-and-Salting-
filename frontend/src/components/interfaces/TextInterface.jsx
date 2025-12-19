import React, { useState } from 'react'
import './Interface.css'

/**
 * TextInterface - Text-based interface for hearing-impaired users
 * 
 * Features:
 * - Large text
 * - Visual indicators
 * - Text-to-speech (optional)
 * - Clear visual feedback
 */
const TextInterface = () => {
  const [input, setInput] = useState('')
  const [output, setOutput] = useState('')

  const handleProcess = () => {
    if (input.trim()) {
      setOutput(`Processed: ${input}`)
    }
  }

  return (
    <div className="interface-container text-interface">
      <h2>Text-Based Interface</h2>
      
      <div className="interface-content">
        <div className="text-input-section">
          <label htmlFor="text-input" className="large-label">
            Enter Text:
          </label>
          <textarea
            id="text-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your text here..."
            className="large-textarea"
            aria-label="Text input"
          />
          <button
            className="btn btn-primary btn-large"
            onClick={handleProcess}
            aria-label="Process text"
          >
            Process
          </button>
        </div>

        {output && (
          <div className="text-output-section">
            <label className="large-label">Output:</label>
            <div className="output-box large-text">
              {output}
            </div>
          </div>
        )}

        <div className="text-actions">
          <h3>Quick Actions:</h3>
          <div className="action-buttons">
            <button
              className="btn btn-secondary btn-large"
              onClick={() => setInput('Hello, how can I help you?')}
            >
              Sample Text 1
            </button>
            <button
              className="btn btn-secondary btn-large"
              onClick={() => setInput('I need assistance with this feature.')}
            >
              Sample Text 2
            </button>
            <button
              className="btn btn-secondary btn-large"
              onClick={() => setInput('')}
            >
              Clear
            </button>
          </div>
        </div>

        <div className="interface-info">
          <p>This interface uses large text and clear visual indicators for better readability.</p>
        </div>
      </div>
    </div>
  )
}

export default TextInterface

