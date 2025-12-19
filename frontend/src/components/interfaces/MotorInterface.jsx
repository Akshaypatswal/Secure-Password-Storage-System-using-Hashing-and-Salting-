import React, { useState } from 'react'
import './Interface.css'

/**
 * MotorInterface - Motor-adapted interface with large buttons and switch mode
 * 
 * Features:
 * - Large buttons
 * - Switch mode support
 * - Simplified navigation
 * - High contrast
 */
const MotorInterface = () => {
  const [currentPage, setCurrentPage] = useState('home')
  const [switchMode, setSwitchMode] = useState(false)

  const navigationItems = [
    { id: 'home', name: 'Home', icon: '🏠' },
    { id: 'messages', name: 'Messages', icon: '💬' },
    { id: 'settings', name: 'Settings', icon: '⚙️' },
    { id: 'help', name: 'Help', icon: '❓' }
  ]

  return (
    <div className="interface-container motor-interface">
      <h2>Motor-Adapted Interface</h2>
      
      <div className="interface-content">
        <div className="switch-mode-toggle">
          <label>
            <input
              type="checkbox"
              checked={switchMode}
              onChange={(e) => setSwitchMode(e.target.checked)}
              aria-label="Toggle switch mode"
            />
            <span>Switch Mode</span>
          </label>
        </div>

        <div className="motor-navigation">
          <h3>Navigation:</h3>
          <div className="nav-grid">
            {navigationItems.map((item) => (
              <button
                key={item.id}
                className={`btn btn-primary btn-extra-large ${currentPage === item.id ? 'active' : ''}`}
                onClick={() => setCurrentPage(item.id)}
                aria-label={`Navigate to ${item.name}`}
              >
                <span className="nav-icon">{item.icon}</span>
                <span className="nav-text">{item.name}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="motor-actions">
          <h3>Quick Actions:</h3>
          <div className="action-grid">
            <button className="btn btn-secondary btn-extra-large">
              <span className="action-icon">✓</span>
              <span>Confirm</span>
            </button>
            <button className="btn btn-secondary btn-extra-large">
              <span className="action-icon">✗</span>
              <span>Cancel</span>
            </button>
            <button className="btn btn-secondary btn-extra-large">
              <span className="action-icon">←</span>
              <span>Back</span>
            </button>
            <button className="btn btn-secondary btn-extra-large">
              <span className="action-icon">→</span>
              <span>Next</span>
            </button>
          </div>
        </div>

        <div className="current-page-content">
          <h3>Current Page: {navigationItems.find(i => i.id === currentPage)?.name}</h3>
          <p>This is the content for the {currentPage} page.</p>
        </div>

        <div className="interface-info">
          <p>This interface features large buttons, simplified navigation, and switch mode support.</p>
        </div>
      </div>
    </div>
  )
}

export default MotorInterface

