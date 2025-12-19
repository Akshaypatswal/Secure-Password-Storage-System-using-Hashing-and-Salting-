import React, { useState } from 'react'
import './ManualSelectionForm.css'

/**
 * ManualSelectionForm - Manual assist mode selection
 * 
 * Allows users to manually choose their preferred assist mode
 * without using camera analysis
 */
const ManualSelectionForm = ({ onSelect }) => {
  const [selectedMode, setSelectedMode] = useState(null)

  const modes = [
    {
      id: 'voice',
      name: 'Voice-First Interface',
      icon: '🎤',
      description: 'Optimized for low-vision and blind users. Voice commands and screen reader support.',
      features: ['Voice commands', 'Screen reader', 'Audio feedback']
    },
    {
      id: 'sign',
      name: 'Sign Language Interface',
      icon: '👋',
      description: 'Optimized for deaf and hard-of-hearing users. Sign language avatar and text chat.',
      features: ['Sign language avatar', 'Text chat', 'Visual alerts']
    },
    {
      id: 'text',
      name: 'Text-Based Interface',
      icon: '📝',
      description: 'Optimized for hearing-impaired users. Large text and clear visual indicators.',
      features: ['Large text', 'Visual indicators', 'Text-to-speech']
    },
    {
      id: 'gesture',
      name: 'Gesture Interface',
      icon: '✋',
      description: 'Optimized for motor-impaired users. Hand gesture recognition and touch controls.',
      features: ['Hand gestures', 'Touch controls', 'Adaptive UI']
    },
    {
      id: 'motor',
      name: 'Motor-Adapted Interface',
      icon: '🖱️',
      description: 'Large buttons, switch mode, and simplified navigation for motor impairments.',
      features: ['Large buttons', 'Switch mode', 'Simplified navigation']
    }
  ]

  const handleSelect = (modeId) => {
    setSelectedMode(modeId)
  }

  const handleSubmit = () => {
    if (selectedMode) {
      onSelect(selectedMode)
    }
  }

  return (
    <div className="manual-selection-form">
      <div className="modes-grid">
        {modes.map((mode) => (
          <div
            key={mode.id}
            className={`mode-card ${selectedMode === mode.id ? 'selected' : ''}`}
            onClick={() => handleSelect(mode.id)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault()
                handleSelect(mode.id)
              }
            }}
            tabIndex={0}
            role="button"
            aria-pressed={selectedMode === mode.id}
            aria-label={`Select ${mode.name}`}
          >
            <div className="mode-icon">{mode.icon}</div>
            <h3>{mode.name}</h3>
            <p className="mode-description">{mode.description}</p>
            <ul className="mode-features">
              {mode.features.map((feature, index) => (
                <li key={index}>{feature}</li>
              ))}
            </ul>
            {selectedMode === mode.id && (
              <div className="selected-indicator">✓ Selected</div>
            )}
          </div>
        ))}
      </div>

      <div className="form-footer">
        <button
          className="btn btn-primary btn-large"
          onClick={handleSubmit}
          disabled={!selectedMode}
          aria-label="Confirm selection"
        >
          Confirm Selection
        </button>
      </div>
    </div>
  )
}

export default ManualSelectionForm

