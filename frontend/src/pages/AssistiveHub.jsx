import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getStoredPreferences, savePreferences, deleteAllUserData } from '../utils/storage'
import VoiceInterface from '../components/interfaces/VoiceInterface'
import SignInterface from '../components/interfaces/SignInterface'
import TextInterface from '../components/interfaces/TextInterface'
import GestureInterface from '../components/interfaces/GestureInterface'
import MotorInterface from '../components/interfaces/MotorInterface'
import './AssistiveHub.css'

/**
 * AssistiveHub - Main interface that adapts based on user's selected assist mode
 */
const AssistiveHub = () => {
  const navigate = useNavigate()
  const [preferences, setPreferences] = useState(null)
  const [showSettings, setShowSettings] = useState(false)

  useEffect(() => {
    const prefs = getStoredPreferences()
    if (!prefs || !prefs.completedOnboarding) {
      navigate('/')
      return
    }
    setPreferences(prefs)
  }, [navigate])

  const handleChangeMode = (newMode) => {
    const updated = {
      ...preferences,
      assistMode: newMode,
      updatedAt: new Date().toISOString()
    }
    savePreferences(updated)
    setPreferences(updated)
  }

  const handleDeleteData = () => {
    if (window.confirm('Are you sure you want to delete all your data? This cannot be undone.')) {
      deleteAllUserData()
      navigate('/')
    }
  }

  if (!preferences) {
    return (
      <div className="loading-hub">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    )
  }

  const renderInterface = () => {
    switch (preferences.assistMode) {
      case 'voice':
        return <VoiceInterface />
      case 'sign':
        return <SignInterface />
      case 'text':
        return <TextInterface />
      case 'gesture':
        return <GestureInterface />
      case 'motor':
        return <MotorInterface />
      default:
        return <TextInterface />
    }
  }

  return (
    <div className="assistive-hub">
      <header className="hub-header">
        <div className="hub-title">
          <h1>InclusiveAI Hub</h1>
        </div>
        <div className="hub-actions">
          <button
            className="btn btn-secondary"
            onClick={() => setShowSettings(!showSettings)}
            aria-label="Toggle settings"
          >
            Settings
          </button>
        </div>
      </header>

      {showSettings && (
        <div className="settings-panel">
          <h3>Settings</h3>
          <div className="settings-content">
            <div className="setting-item">
              <label>Current Mode:</label>
              <select
                value={preferences.assistMode}
                onChange={(e) => handleChangeMode(e.target.value)}
                aria-label="Change assist mode"
              >
                <option value="voice">Voice-First</option>
                <option value="sign">Sign Language</option>
                <option value="text">Text-Based</option>
                <option value="gesture">Gesture</option>
                <option value="motor">Motor-Adapted</option>
              </select>
            </div>
            <div className="setting-item">
              <button
                className="btn btn-danger"
                onClick={handleDeleteData}
                aria-label="Delete all user data"
              >
                Delete All Data
              </button>
            </div>
          </div>
        </div>
      )}

      <main className="hub-main">
        {renderInterface()}
      </main>

      <footer className="hub-footer">
        <p>InclusiveAI - Built for accessibility. Built with privacy.</p>
      </footer>
    </div>
  )
}

export default AssistiveHub

