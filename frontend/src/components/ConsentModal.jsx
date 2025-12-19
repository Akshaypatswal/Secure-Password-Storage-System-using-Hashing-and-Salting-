import React, { useState, useEffect, useRef } from 'react'
import './ConsentModal.css'

/**
 * ConsentModal - Privacy-first consent flow for camera usage
 * 
 * Shows clear explanation of:
 * - What camera will analyze
 * - What data is stored (prefer none)
 * - How results are used
 * - Option to opt-out
 */
const ConsentModal = ({ isOpen, onAccept, onDecline, onClose }) => {
  const [readSections, setReadSections] = useState({
    purpose: false,
    data: false,
    usage: false,
    rights: false
  })
  const [manualCheckbox, setManualCheckbox] = useState(false)
  const sectionRefs = {
    purpose: useRef(null),
    data: useRef(null),
    usage: useRef(null),
    rights: useRef(null)
  }

  // Auto-detect when sections are scrolled into view
  useEffect(() => {
    if (!isOpen) return

    const observerOptions = {
      root: null,
      rootMargin: '0px',
      threshold: 0.5 // Section is considered read when 50% is visible
    }

    const observerCallback = (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const sectionId = entry.target.dataset.section
          if (sectionId) {
            setReadSections(prev => ({ ...prev, [sectionId]: true }))
          }
        }
      })
    }

    const observer = new IntersectionObserver(observerCallback, observerOptions)

    // Observe all sections with a small delay to ensure refs are set
    const timeoutId = setTimeout(() => {
      Object.values(sectionRefs).forEach(ref => {
        if (ref.current) {
          observer.observe(ref.current)
        }
      })
    }, 100)

    return () => {
      clearTimeout(timeoutId)
      observer.disconnect()
    }
  }, [isOpen])

  // Reset when modal opens
  useEffect(() => {
    if (isOpen) {
      setReadSections({
        purpose: false,
        data: false,
        usage: false,
        rights: false
      })
      setManualCheckbox(false)
    }
  }, [isOpen])

  if (!isOpen) return null

  const handleSectionRead = (section) => {
    setReadSections(prev => ({ ...prev, [section]: true }))
  }

  const handleCheckboxChange = (e) => {
    setManualCheckbox(e.target.checked)
  }

  const allRead = Object.values(readSections).every(Boolean) || manualCheckbox

  return (
    <div className="consent-modal-overlay" role="dialog" aria-labelledby="consent-title" aria-modal="true">
      <div className="consent-modal">
        <div className="consent-modal-header">
          <h2 id="consent-title">Camera Usage Consent</h2>
        </div>

        <div className="consent-modal-content">
          <div className="consent-warning">
            <strong>⚠️ Important Disclaimer:</strong>
            <p>This is NOT a medical diagnosis tool. Camera analysis only suggests UI preferences based on interaction patterns.</p>
          </div>

          <div className="consent-sections">
            <section 
              ref={sectionRefs.purpose}
              data-section="purpose"
              className={`consent-section ${readSections.purpose ? 'read' : ''}`}
              onFocus={() => handleSectionRead('purpose')}
              onClick={() => handleSectionRead('purpose')}
            >
              <div className="section-header">
                <h3>1. What We Analyze</h3>
                {readSections.purpose && <span className="read-indicator">✓</span>}
              </div>
              <ul>
                <li>Gaze & eye contact patterns (brief) - to infer low-vision interaction needs</li>
                <li>Hand movement & signing gestures - to detect sign-language preference</li>
                <li>Face & mouth movement - cues for hearing preferences</li>
                <li>Posture & mobility cues - to suggest motor-adapted UI</li>
                <li>Interaction behavior - voice vs typed input preferences</li>
              </ul>
            </section>

            <section 
              ref={sectionRefs.data}
              data-section="data"
              className={`consent-section ${readSections.data ? 'read' : ''}`}
              onFocus={() => handleSectionRead('data')}
              onClick={() => handleSectionRead('data')}
            >
              <div className="section-header">
                <h3>2. Data Storage & Privacy</h3>
                {readSections.data && <span className="read-indicator">✓</span>}
              </div>
              <ul>
                <li><strong>Default:</strong> All processing happens on-device (no images uploaded)</li>
                <li><strong>Storage:</strong> Only lightweight keypoint summaries may be stored locally</li>
                <li><strong>No images stored:</strong> Raw camera images are never saved</li>
                <li><strong>Encryption:</strong> Any stored data is encrypted locally</li>
                <li><strong>You can delete:</strong> All camera-derived data can be deleted immediately</li>
              </ul>
            </section>

            <section 
              ref={sectionRefs.usage}
              data-section="usage"
              className={`consent-section ${readSections.usage ? 'read' : ''}`}
              onFocus={() => handleSectionRead('usage')}
              onClick={() => handleSectionRead('usage')}
            >
              <div className="section-header">
                <h3>3. How Results Are Used</h3>
                {readSections.usage && <span className="read-indicator">✓</span>}
              </div>
              <ul>
                <li>Results suggest an optimal assistive interface mode (Voice, Sign, Text, Gesture, Motor)</li>
                <li>You can accept, modify, or completely override the suggestion</li>
                <li>Results are only used to improve your app experience</li>
                <li>No data is shared with third parties without explicit consent</li>
              </ul>
            </section>

            <section 
              ref={sectionRefs.rights}
              data-section="rights"
              className={`consent-section ${readSections.rights ? 'read' : ''}`}
              onFocus={() => handleSectionRead('rights')}
              onClick={() => handleSectionRead('rights')}
            >
              <div className="section-header">
                <h3>4. Your Rights</h3>
                {readSections.rights && <span className="read-indicator">✓</span>}
              </div>
              <ul>
                <li>You can skip camera analysis entirely</li>
                <li>You can delete all camera data at any time</li>
                <li>You can manually choose your assist mode without camera</li>
                <li>You can revoke consent at any time</li>
              </ul>
            </section>
          </div>

          <div className="consent-checkbox">
            <label>
              <input 
                type="checkbox" 
                checked={allRead || manualCheckbox}
                onChange={handleCheckboxChange}
                aria-label="I have read and understood all sections"
              />
              <span>I have read and understood all sections above</span>
            </label>
            {!allRead && !manualCheckbox && (
              <p className="checkbox-hint">
                Please read all sections above or check this box to proceed
              </p>
            )}
          </div>
        </div>

        <div className="consent-modal-footer">
          <button 
            className="btn btn-secondary" 
            onClick={onDecline}
            aria-label="Skip camera analysis"
          >
            Skip Camera
          </button>
          <button 
            className="btn btn-primary" 
            onClick={onAccept}
            disabled={!allRead}
            aria-label="Accept and proceed with camera analysis"
          >
            I Understand, Proceed
          </button>
          <button 
            className="btn btn-text" 
            onClick={onClose}
            aria-label="Close consent modal"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}

export default ConsentModal

