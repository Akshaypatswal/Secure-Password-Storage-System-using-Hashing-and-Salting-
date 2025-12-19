import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import OnboardingPage from './pages/OnboardingPage'
import AssistiveHub from './pages/AssistiveHub'
import { getStoredPreferences } from './utils/storage'
import './App.css'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [hasCompletedOnboarding, setHasCompletedOnboarding] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem('auth_token')
    const guestMode = localStorage.getItem('guest_mode')
    setIsAuthenticated(!!token || !!guestMode)

    // Check if user has completed onboarding
    const preferences = getStoredPreferences()
    setHasCompletedOnboarding(preferences?.completedOnboarding || false)
    setLoading(false)
  }, [])

  const handleLogin = (response) => {
    setIsAuthenticated(true)
  }

  if (loading) {
    return (
      <div className="app-loading">
        <div className="loading-spinner">
          <div className="spinner-ring"></div>
          <div className="spinner-ring"></div>
          <div className="spinner-ring"></div>
        </div>
        <p>Loading InclusiveAI...</p>
      </div>
    )
  }

  return (
    <Router>
      <Routes>
        <Route 
          path="/login" 
          element={
            isAuthenticated ? 
              <Navigate to="/" replace /> : 
              <LoginPage onLogin={handleLogin} />
          } 
        />
        <Route 
          path="/" 
          element={
            !isAuthenticated ? 
              <Navigate to="/login" replace /> :
              hasCompletedOnboarding ? 
                <Navigate to="/hub" replace /> : 
                <OnboardingPage onComplete={() => setHasCompletedOnboarding(true)} />
          } 
        />
        <Route path="/hub" element={<AssistiveHub />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  )
}

export default App

