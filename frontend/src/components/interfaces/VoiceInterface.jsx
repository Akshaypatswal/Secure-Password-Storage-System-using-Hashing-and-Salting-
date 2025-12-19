import React, { useState } from 'react'
import './Interface.css'

/**
 * VoiceInterface - Voice-first interface for low-vision/blind users
 * 
 * Features:
 * - Voice commands
 * - Screen reader support
 * - Audio feedback
 * - Text-to-speech
 */
const VoiceInterface = () => {
  const [isListening, setIsListening] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [response, setResponse] = useState('')

  const handleStartListening = () => {
    setIsListening(true)
    // In production, use Web Speech API
    setTimeout(() => {
      setTranscript('Hello, how can I help you today?')
      setIsListening(false)
    }, 2000)
  }

  const handleStopListening = () => {
    setIsListening(false)
  }

  const handleSpeak = (text) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = 'en-US'
      speechSynthesis.speak(utterance)
    }
  }

  return (
    <div className="interface-container voice-interface">
      <h2>Voice-First Interface</h2>
      
      <div className="interface-content">
        <div className="voice-controls">
          <button
            className={`btn ${isListening ? 'btn-danger' : 'btn-primary'}`}
            onClick={isListening ? handleStopListening : handleStartListening}
            aria-label={isListening ? 'Stop listening' : 'Start listening'}
          >
            {isListening ? 'Stop Listening' : 'Start Listening'}
          </button>
          
          {transcript && (
            <div className="transcript-box">
              <h3>Transcript:</h3>
              <p>{transcript}</p>
            </div>
          )}
        </div>

        <div className="voice-actions">
          <h3>Quick Actions:</h3>
          <div className="action-buttons">
            <button
              className="btn btn-secondary"
              onClick={() => handleSpeak('Reading the news')}
              aria-label="Read news"
            >
              Read News
            </button>
            <button
              className="btn btn-secondary"
              onClick={() => handleSpeak('Checking weather')}
              aria-label="Check weather"
            >
              Check Weather
            </button>
            <button
              className="btn btn-secondary"
              onClick={() => handleSpeak('Opening messages')}
              aria-label="Open messages"
            >
              Open Messages
            </button>
          </div>
        </div>

        <div className="interface-info">
          <p>This interface is optimized for voice commands and screen reader support.</p>
        </div>
      </div>
    </div>
  )
}

export default VoiceInterface

