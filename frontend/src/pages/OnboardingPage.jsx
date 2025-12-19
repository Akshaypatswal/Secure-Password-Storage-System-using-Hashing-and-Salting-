import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import ConsentModal from '../components/ConsentModal'
import CameraScanner from '../components/CameraScanner'
import RecommendationCard from '../components/RecommendationCard'
import ManualSelectionForm from '../components/ManualSelectionForm'
import { saveConsent, savePreferences, clearCameraData } from '../utils/storage'
import { submitAssistScan, saveUserPreferences } from '../utils/api'
import './OnboardingPage.css'

/**
 * OnboardingPage - Main onboarding flow with camera scan
 * 
 * Flow:
 * 1. Show consent modal
 * 2. If accepted, show camera scanner
 * 3. Show recommendation
 * 4. Allow accept/override/manual
 */
const OnboardingPage = ({ onComplete }) => {
  const navigate = useNavigate()
  const [step, setStep] = useState('welcome') // welcome, consent, scan, recommendation, manual, complete
  const [showConsent, setShowConsent] = useState(false)
  const [recommendation, setRecommendation] = useState(null)
  const [showManual, setShowManual] = useState(false)
  const [error, setError] = useState(null)

  const handleStartOnboarding = () => {
    setShowConsent(true)
    setStep('consent')
  }

  const handleConsentAccept = () => {
    saveConsent({
      cameraUsage: true,
      timestamp: new Date().toISOString(),
      version: '1.0'
    })
    setShowConsent(false)
    setStep('scan')
  }

  const handleConsentDecline = () => {
    saveConsent({
      cameraUsage: false,
      timestamp: new Date().toISOString(),
      version: '1.0'
    })
    setShowConsent(false)
    setStep('manual')
    setShowManual(true)
  }

  const handleScanComplete = async (scanData) => {
    try {
      setStep('processing')
      // Submit scan data to backend for analysis
      const result = await submitAssistScan(scanData)
      setRecommendation(result)
      setStep('recommendation')
    } catch (error) {
      console.error('Error processing scan:', error)
      setError('Failed to process scan. Please try manual selection.')
      setStep('manual')
      setShowManual(true)
    }
  }

  const handleScanError = (error) => {
    console.error('Camera error:', error)
    setError('Camera access denied or unavailable. Please use manual selection.')
    setStep('manual')
    setShowManual(true)
  }

  const handleAcceptRecommendation = async (mode) => {
    try {
      const preferences = {
        assistMode: mode,
        source: 'camera_recommendation',
        confidence: recommendation.confidence,
        completedOnboarding: true,
        timestamp: new Date().toISOString()
      }

      // Save locally
      savePreferences(preferences)

      // Save to backend (optional)
      try {
        await saveUserPreferences(preferences)
      } catch (err) {
        console.warn('Backend save failed, using local storage only:', err)
      }

      setStep('complete')
      setTimeout(() => {
        onComplete?.()
        navigate('/hub')
      }, 2000)
    } catch (error) {
      console.error('Error saving preferences:', error)
      setError('Failed to save preferences. Please try again.')
    }
  }

  const handleOverride = () => {
    setStep('manual')
    setShowManual(true)
  }

  const handleManualSelection = async (selectedMode) => {
    try {
      const preferences = {
        assistMode: selectedMode,
        source: 'manual_selection',
        completedOnboarding: true,
        timestamp: new Date().toISOString()
      }

      // Save locally
      const saved = savePreferences(preferences)
      if (!saved) {
        throw new Error('Failed to save preferences locally')
      }

      // Save to backend (optional)
      try {
        await saveUserPreferences(preferences)
      } catch (err) {
        console.warn('Backend save failed, using local storage only:', err)
      }

      setStep('complete')
      setTimeout(() => {
        onComplete?.()
        navigate('/hub')
      }, 2000)
    } catch (error) {
      console.error('Error saving manual preferences:', error)
      setError('Failed to save preferences. Please try again.')
    }
  }

  const handleSkipCamera = () => {
    setShowConsent(false)
    setStep('manual')
    setShowManual(true)
  }

  const handleDeleteCameraData = () => {
    clearCameraData()
    alert('Camera data deleted successfully.')
  }

  return (
    <div className="onboarding-page">
      <div className="onboarding-container">
        {step === 'welcome' && (
          <div className="welcome-section">
            <h1>Welcome to InclusiveAI</h1>
            <p className="welcome-description">
              We'll help you find the best assistive interface for your needs.
              You can use our camera-based scan (with your consent) or manually select your preferences.
            </p>
            <div className="welcome-actions">
              <button 
                className="btn btn-primary btn-large"
                onClick={handleStartOnboarding}
                aria-label="Start onboarding with camera scan"
              >
                Start with Camera Scan
              </button>
              <button 
                className="btn btn-secondary btn-large"
                onClick={handleSkipCamera}
                aria-label="Skip camera and use manual selection"
              >
                Skip Camera - Manual Selection
              </button>
            </div>
          </div>
        )}

        {step === 'consent' && (
          <ConsentModal
            isOpen={showConsent}
            onAccept={handleConsentAccept}
            onDecline={handleConsentDecline}
            onClose={() => setShowConsent(false)}
          />
        )}

        {step === 'scan' && (
          <div className="scan-section">
            <h2>Camera Scan</h2>
            <p className="section-description">
              Please follow the on-screen instructions. The scan will take about 20 seconds.
            </p>
            <CameraScanner
              onScanComplete={handleScanComplete}
              onError={handleScanError}
            />
            <button 
              className="btn btn-text"
              onClick={handleSkipCamera}
              style={{ marginTop: '20px' }}
            >
              Skip Camera Scan
            </button>
          </div>
        )}

        {step === 'processing' && (
          <div className="processing-section">
            <div className="spinner"></div>
            <p>Processing your scan...</p>
          </div>
        )}

        {step === 'recommendation' && recommendation && (
          <div className="recommendation-section">
            <h2>Recommended Interface</h2>
            <RecommendationCard
              recommendation={recommendation}
              onAccept={handleAcceptRecommendation}
              onOverride={handleOverride}
              onManual={handleOverride}
            />
            <div className="privacy-actions" style={{ marginTop: '20px' }}>
              <button 
                className="btn btn-text"
                onClick={handleDeleteCameraData}
                aria-label="Delete camera data"
              >
                Delete Camera Data
              </button>
            </div>
          </div>
        )}

        {showManual && (
          <div className="manual-section">
            <h2>Manual Selection</h2>
            <p className="section-description">
              Please select the assistive interface that works best for you.
            </p>
            <ManualSelectionForm onSelect={handleManualSelection} />
          </div>
        )}

        {step === 'complete' && (
          <div className="complete-section">
            <div className="success-icon">✓</div>
            <h2>Setup Complete!</h2>
            <p>Redirecting to your assistive hub...</p>
          </div>
        )}

        {error && (
          <div className="error-message" role="alert">
            <p>{error}</p>
            <button 
              className="btn btn-secondary"
              onClick={() => setError(null)}
            >
              Dismiss
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default OnboardingPage

