import React from 'react'
import './RecommendationCard.css'

/**
 * RecommendationCard - Shows assist mode recommendation with explainability
 * 
 * Displays:
 * - Recommended mode with confidence score
 * - Top-3 cues that triggered the recommendation
 * - Accept/Override/Manual options
 */
const RecommendationCard = ({ recommendation, onAccept, onOverride, onManual }) => {
  if (!recommendation) return null

  const { mode, confidence, cues, scores } = recommendation

  const modeInfo = {
    voice: {
      name: 'Voice-First Interface',
      description: 'Optimized for low-vision and blind users',
      icon: '🎤',
    },
    sign: {
      name: 'Sign Language Interface',
      description: 'Optimized for deaf and hard-of-hearing users',
      icon: '👋',
    },
    text: {
      name: 'Text-Based Interface',
      description: 'Optimized for hearing-impaired users',
      icon: '📝',
    },
    gesture: {
      name: 'Gesture Interface',
      description: 'Optimized for motor-impaired users',
      icon: '✋',
    },
    motor: {
      name: 'Motor-Adapted Interface',
      description: 'Large buttons and switch mode support',
      icon: '🖱️',
    }
  }

  const currentMode = modeInfo[mode] || modeInfo.voice
  const confidencePercent = Math.round(confidence * 100)
  const isHighConfidence = confidence > 0.7

  return (
    <div className="recommendation-card">
      <div className="recommendation-header">
        <div className="mode-icon">{currentMode.icon}</div>
        <div>
          <h3>{currentMode.name}</h3>
        </div>
      </div>

      <div className="recommendation-body">
        <p className="mode-description">{currentMode.description}</p>

        <div className="confidence-section">
          <div className="confidence-label">
            <span>Confidence Score:</span>
            <span className="confidence-value">{confidencePercent}%</span>
          </div>
          <div className="confidence-bar">
            <div 
              className="confidence-fill" 
              style={{ width: `${confidencePercent}%` }}
            ></div>
          </div>
          {!isHighConfidence && (
            <p className="confidence-warning">
              Low confidence - We recommend manual selection
            </p>
          )}
        </div>

        {cues && cues.length > 0 && (
          <div className="cues-section">
            <h4>Why this recommendation?</h4>
            <ul className="cues-list">
              {cues.slice(0, 3).map((cue, index) => (
                <li key={index} className="cue-item">
                  <span className="cue-icon">✓</span>
                  <span>{cue}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {scores && (
          <div className="scores-section">
            <h4>All Mode Scores:</h4>
            <div className="scores-grid">
              {Object.entries(scores).map(([modeName, score]) => (
                <div 
                  key={modeName} 
                  className={`score-item ${modeName === mode ? 'selected' : ''}`}
                >
                  <span className="score-label">{modeInfo[modeName]?.name || modeName}</span>
                  <span className="score-value">{Math.round(score * 100)}%</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="recommendation-footer">
        <button 
          className="btn btn-primary"
          onClick={() => onAccept(mode)}
          disabled={!isHighConfidence}
          aria-label={`Accept ${currentMode.name} recommendation`}
        >
          Accept Recommendation
        </button>
        <button 
          className="btn btn-secondary"
          onClick={onOverride}
          aria-label="Choose different mode"
        >
          Choose Different Mode
        </button>
        <button 
          className="btn btn-text"
          onClick={onManual}
          aria-label="Manual selection"
        >
          Manual Selection
        </button>
      </div>

      <div className="recommendation-disclaimer">
        <p>
          <strong>Note:</strong> This is a UI suggestion, not a medical diagnosis. 
          You can always change your preference later.
        </p>
      </div>
    </div>
  )
}

export default RecommendationCard

