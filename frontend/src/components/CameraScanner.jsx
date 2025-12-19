import React, { useRef, useEffect, useState, useCallback } from 'react'
import { Hands } from '@mediapipe/hands'
import { Pose } from '@mediapipe/pose'
import { Camera } from '@mediapipe/camera_utils'
import { drawConnectors, drawLandmarks } from '@mediapipe/drawing_utils'
import './CameraScanner.css'

/**
 * CameraScanner - Guided camera scan for assist mode detection
 * 
 * Uses MediaPipe to extract:
 * - Hand keypoints (for sign language detection)
 * - Pose keypoints (for posture/mobility cues)
 * - Face landmarks (for gaze/eye contact)
 */
const CameraScanner = ({ onScanComplete, onError }) => {
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const handsRef = useRef(null)
  const poseRef = useRef(null)
  const faceRef = useRef(null)
  const cameraRef = useRef(null)
  const recognitionRef = useRef(null)
  
  const [isScanning, setIsScanning] = useState(false)
  const [scanProgress, setScanProgress] = useState(0)
  const [currentStep, setCurrentStep] = useState('')
  const [cameraFacing, setCameraFacing] = useState('user') // 'user' or 'environment'
  const [liveStats, setLiveStats] = useState({
    handsDetected: 0,
    gesturesCount: 0,
    speechDetected: false,
    faceDetected: false,
    poseDetected: false
  })
  const [features, setFeatures] = useState({
    handSignFreq: 0,
    speechDetected: false,
    gazePattern: null,
    posture: null,
    interactionBehavior: null,
    handMovementHistory: [],
    speechHistory: []
  })

  const scanDuration = 20000 // 20 seconds
  const startTimeRef = useRef(null)
  const progressIntervalRef = useRef(null)

  // Initialize MediaPipe models
  useEffect(() => {
    // Initialize MediaPipe Hands
    const hands = new Hands({
      locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
      }
    })

    hands.setOptions({
      maxNumHands: 2,
      modelComplexity: 1,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5
    })

    hands.onResults((results) => {
      if (canvasRef.current && videoRef.current && isScanning) {
        const canvasCtx = canvasRef.current.getContext('2d')
        canvasCtx.save()
        canvasCtx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height)
        canvasCtx.drawImage(results.image, 0, 0, canvasRef.current.width, canvasRef.current.height)

        if (results.multiHandLandmarks) {
          // Draw hand landmarks
          results.multiHandLandmarks.forEach(landmarks => {
            drawLandmarks(canvasCtx, landmarks, { color: '#FF0000', lineWidth: 1, radius: 3 })
          })
          
          // Analyze hand gestures
          analyzeHandGestures(results.multiHandLandmarks)
          
          // Update live stats
          setLiveStats(prev => ({
            ...prev,
            handsDetected: results.multiHandLandmarks.length
          }))
        }
      }
    })

    handsRef.current = hands

    // Initialize MediaPipe Pose
    const pose = new Pose({
      locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`
      }
    })

    pose.setOptions({
      modelComplexity: 1,
      smoothLandmarks: true,
      enableSegmentation: false,
      smoothSegmentation: false,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5
    })

    pose.onResults((results) => {
      if (canvasRef.current && videoRef.current && isScanning) {
        const canvasCtx = canvasRef.current.getContext('2d')
        
        if (results.poseLandmarks) {
          // Draw pose landmarks
          drawLandmarks(canvasCtx, results.poseLandmarks, { color: '#FF00FF', lineWidth: 1, radius: 3 })
          
          analyzePose(results.poseLandmarks)
          
          // Simplified gaze detection using nose position
          if (results.poseLandmarks && results.poseLandmarks.length > 0) {
            const nose = results.poseLandmarks[0] // NOSE landmark
            if (nose) {
              let gazePattern = 'normal'
              if (nose.x < 0.3 || nose.x > 0.7) {
                gazePattern = 'inconsistent'
              }
              
              setFeatures(prev => ({
                ...prev,
                gazePattern: gazePattern
              }))
              
              setLiveStats(prev => ({
                ...prev,
                faceDetected: true,
                poseDetected: true
              }))
            }
          }
        }
      }
    })

    poseRef.current = pose

    // Face detection - simplified version using pose landmarks
    // In production, use Face Mesh for better accuracy
    // For now, we'll detect face presence through pose detection

    return () => {
      if (cameraRef.current) {
        cameraRef.current.stop()
      }
      if (recognitionRef.current) {
        recognitionRef.current.stop()
      }
    }
  }, [isScanning])

  const analyzeHandGestures = useCallback((landmarks) => {
    if (landmarks.length > 0) {
      // Calculate hand movement velocity
      const currentTime = Date.now()
      const handPositions = landmarks.map(hand => {
        const wrist = hand[0] // Wrist landmark
        return { x: wrist.x, y: wrist.y, z: wrist.z, time: currentTime }
      })

      setFeatures(prev => {
        const history = [...prev.handMovementHistory, ...handPositions]
        // Keep only last 10 positions
        const recentHistory = history.slice(-10)
        
        // Calculate movement frequency
        let movementFreq = prev.handSignFreq
        if (recentHistory.length >= 2) {
          const lastPos = recentHistory[recentHistory.length - 1]
          const prevPos = recentHistory[recentHistory.length - 2]
          const distance = Math.sqrt(
            Math.pow(lastPos.x - prevPos.x, 2) + 
            Math.pow(lastPos.y - prevPos.y, 2)
          )
          if (distance > 0.01) { // Threshold for movement
            movementFreq += 0.2
          }
        }

        return {
          ...prev,
          handSignFreq: Math.min(movementFreq, 10),
          handMovementHistory: recentHistory
        }
      })

      setLiveStats(prev => ({
        ...prev,
        gesturesCount: prev.gesturesCount + 1
      }))
    }
  }, [])

  const analyzePose = useCallback((landmarks) => {
    // Analyze posture - detect sitting vs standing
    const leftHip = landmarks[23] // LEFT_HIP
    const rightHip = landmarks[24] // RIGHT_HIP
    const leftAnkle = landmarks[27] // LEFT_ANKLE
    const rightAnkle = landmarks[28] // RIGHT_ANKLE

    if (leftHip && rightHip && leftAnkle && rightAnkle) {
      const hipY = (leftHip.y + rightHip.y) / 2
      const ankleY = (leftAnkle.y + rightAnkle.y) / 2
      const hipAnkleDiff = Math.abs(hipY - ankleY)

      let posture = 'standing'
      if (hipAnkleDiff < 0.2) {
        posture = 'seated'
      }

      setFeatures(prev => ({
        ...prev,
        posture: posture
      }))
    }
  }, [])


  // Initialize Speech Recognition
  const initSpeechRecognition = useCallback(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
      const recognition = new SpeechRecognition()
      
      recognition.continuous = true
      recognition.interimResults = true
      recognition.lang = 'en-US'

      recognition.onresult = (event) => {
        let speechDetected = false
        for (let i = event.resultIndex; i < event.results.length; i++) {
          if (event.results[i].isFinal) {
            speechDetected = true
            const transcript = event.results[i][0].transcript
            setFeatures(prev => ({
              ...prev,
              speechDetected: true,
              speechHistory: [...prev.speechHistory.slice(-5), transcript]
            }))
          }
        }
        
        if (speechDetected) {
          setLiveStats(prev => ({
            ...prev,
            speechDetected: true
          }))
        }
      }

      recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error)
      }

      recognitionRef.current = recognition
      return recognition
    }
    return null
  }, [])

  const startScan = async () => {
    try {
      // Request camera access
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { 
          width: 640, 
          height: 480,
          facingMode: cameraFacing
        },
        audio: true // For speech recognition
      })

      if (videoRef.current) {
        videoRef.current.srcObject = stream
        videoRef.current.play()

        // Setup canvas
        if (canvasRef.current) {
          canvasRef.current.width = 640
          canvasRef.current.height = 480
        }

        // Start MediaPipe processing
        if (handsRef.current && videoRef.current) {
          const camera = new Camera(videoRef.current, {
            onFrame: async () => {
              if (isScanning) {
                if (handsRef.current) {
                  await handsRef.current.send({ image: videoRef.current })
                }
                if (poseRef.current) {
                  await poseRef.current.send({ image: videoRef.current })
                }
              }
              // Face detection can be added here if Face Mesh is available
            },
            width: 640,
            height: 480
          })
          camera.start()
          cameraRef.current = camera
        }

        // Start speech recognition
        const recognition = initSpeechRecognition()
        if (recognition) {
          recognition.start()
        }

        setIsScanning(true)
        startTimeRef.current = Date.now()
        startGuidedSteps()
      }
    } catch (error) {
      console.error('Error accessing camera:', error)
      onError?.(error)
    }
  }

  const startGuidedSteps = () => {
    const steps = [
      { time: 0, text: 'Please wave your hands or make signing gestures', duration: 5000 },
      { time: 5000, text: 'Try speaking a short sentence', duration: 5000 },
      { time: 10000, text: 'Look at the camera and maintain eye contact', duration: 5000 },
      { time: 15000, text: 'Almost done...', duration: 5000 }
    ]

    steps.forEach(step => {
      setTimeout(() => {
        setCurrentStep(step.text)
        setTimeout(() => {
          if (step.time + step.duration >= scanDuration) {
            completeScan()
          }
        }, step.duration)
      }, step.time)
    })

    // Update progress
    progressIntervalRef.current = setInterval(() => {
      if (startTimeRef.current) {
        const elapsed = Date.now() - startTimeRef.current
        const progress = Math.min((elapsed / scanDuration) * 100, 100)
        setScanProgress(progress)

        if (progress >= 100) {
          clearInterval(progressIntervalRef.current)
          progressIntervalRef.current = null
          // Auto-complete scan when progress reaches 100%
          if (isScanning) {
            completeScan()
          }
        }
      }
    }, 100)
  }

  const completeScan = () => {
    // Clear progress interval first
    if (progressIntervalRef.current) {
      clearInterval(progressIntervalRef.current)
      progressIntervalRef.current = null
    }
    
    setIsScanning(false)
    
    // Stop camera
    if (cameraRef.current) {
      try {
        cameraRef.current.stop()
      } catch (e) {
        console.warn('Error stopping camera:', e)
      }
    }
    if (videoRef.current?.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(track => {
        track.stop()
        track.enabled = false
      })
      videoRef.current.srcObject = null
    }
    
    // Stop speech recognition
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop()
      } catch (e) {
        console.warn('Error stopping speech recognition:', e)
      }
    }

    // Prepare scan results with proper structure
    const scanResults = {
      features: {
        handSignFreq: Math.min(features.handSignFreq, 10), // Normalize to 0-10
        speechDetected: features.speechDetected || liveStats.speechDetected,
        gazePattern: features.gazePattern || 'normal',
        posture: features.posture || 'standing',
        interactionBehavior: features.interactionBehavior || null,
        timestamp: new Date().toISOString()
      },
      duration: scanDuration
    }

    // Call onScanComplete with a small delay to ensure UI updates
    setTimeout(() => {
      onScanComplete?.(scanResults)
    }, 300)
  }

  const stopScan = () => {
    setIsScanning(false)
    
    // Stop camera
    if (cameraRef.current) {
      cameraRef.current.stop()
    }
    if (videoRef.current?.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(track => track.stop())
    }
    
    // Stop speech recognition
    if (recognitionRef.current) {
      recognitionRef.current.stop()
    }
    
    // Clear progress interval
    if (progressIntervalRef.current) {
      clearInterval(progressIntervalRef.current)
    }
  }

  const flipCamera = async () => {
    if (isScanning) {
      stopScan()
      setCameraFacing(prev => prev === 'user' ? 'environment' : 'user')
      setTimeout(() => startScan(), 500)
    } else {
      setCameraFacing(prev => prev === 'user' ? 'environment' : 'user')
    }
  }

  return (
    <div className="camera-scanner">
      <div className="camera-container">
        <video
          ref={videoRef}
          className="camera-video"
          autoPlay
          playsInline
          muted
          style={{ display: isScanning ? 'block' : 'none' }}
        />
        <canvas
          ref={canvasRef}
          className="camera-canvas"
          style={{ display: isScanning ? 'block' : 'none' }}
        />
        {!isScanning && (
          <div className="camera-placeholder">
            <p>Camera will start when you click "Start Scan"</p>
          </div>
        )}
      </div>

      {isScanning && (
        <div className="scan-indicator" role="status" aria-live="polite">
          <div className="scan-light"></div>
          <span>Camera is active - Processing...</span>
        </div>
      )}

      {isScanning && (
        <div className="scan-progress">
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${scanProgress}%` }}
            ></div>
          </div>
          <p className="progress-text">{Math.round(scanProgress)}%</p>
        </div>
      )}

      {isScanning && currentStep && (
        <div className="scan-instruction">
          <p>{currentStep}</p>
        </div>
      )}

      {isScanning && (
        <div className="live-stats">
          <h4>Live Detection Stats:</h4>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-label">Hands:</span>
              <span className="stat-value">{liveStats.handsDetected}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Gestures:</span>
              <span className="stat-value">{liveStats.gesturesCount}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Speech:</span>
              <span className="stat-value">{liveStats.speechDetected ? '✓' : '✗'}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Face:</span>
              <span className="stat-value">{liveStats.faceDetected ? '✓' : '✗'}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Pose:</span>
              <span className="stat-value">{liveStats.poseDetected ? '✓' : '✗'}</span>
            </div>
          </div>
        </div>
      )}

      <div className="camera-controls">
        {!isScanning ? (
          <button 
            className="btn btn-primary"
            onClick={startScan}
            aria-label="Start camera scan"
          >
            Start Scan
          </button>
        ) : (
          <>
            <button 
              className="btn btn-danger"
              onClick={stopScan}
              aria-label="Stop camera scan"
            >
              Stop Scan
            </button>
            <button 
              className="btn btn-secondary"
              onClick={flipCamera}
              aria-label="Flip camera"
            >
              Flip Camera
            </button>
          </>
        )}
      </div>
    </div>
  )
}

export default CameraScanner

