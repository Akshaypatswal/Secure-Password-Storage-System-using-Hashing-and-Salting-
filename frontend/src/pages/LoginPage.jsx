import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { loginUser } from '../utils/api'
import './LoginPage.css'

/**
 * LoginPage - Modern login page with animations
 */
const LoginPage = ({ onLogin }) => {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  })
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showPassword, setShowPassword] = useState(false)

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
    setError(null)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)

    try {
      const response = await loginUser(formData)
      if (response) {
        // Save auth token
        if (response.token) {
          localStorage.setItem('auth_token', response.token)
        }
        if (response.user_id) {
          localStorage.setItem('user_id', response.user_id)
        }
        
        onLogin?.(response)
        navigate('/')
      }
    } catch (err) {
      console.error('Login error:', err)
      setError('Login failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleGuestMode = () => {
    localStorage.setItem('guest_mode', 'true')
    navigate('/')
  }

  return (
    <div className="login-page">
      <div className="login-background">
        <div className="floating-shapes">
          <div className="shape shape-1"></div>
          <div className="shape shape-2"></div>
          <div className="shape shape-3"></div>
          <div className="shape shape-4"></div>
          <div className="shape shape-5"></div>
        </div>
      </div>

      <div className="login-container">
        <div className="login-card">
          <div className="login-header">
            <div className="logo-container">
              <div className="logo-icon">♿</div>
              <h1 className="logo-text">InclusiveAI</h1>
            </div>
            <p className="login-subtitle">Welcome back! Please login to continue</p>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label htmlFor="username" className="form-label">
                Username or Email
              </label>
              <div className="input-wrapper">
                <span className="input-icon">👤</span>
                <input
                  type="text"
                  id="username"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  className="form-input"
                  placeholder="Enter your username"
                  required
                  autoComplete="username"
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="password" className="form-label">
                Password
              </label>
              <div className="input-wrapper">
                <span className="input-icon">🔒</span>
                <input
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="form-input"
                  placeholder="Enter your password"
                  required
                  autoComplete="current-password"
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword(!showPassword)}
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                >
                  {showPassword ? '👁️' : '👁️‍🗨️'}
                </button>
              </div>
            </div>

            {error && (
              <div className="error-message" role="alert">
                <span className="error-icon">⚠️</span>
                {error}
              </div>
            )}

            <div className="form-options">
              <label className="remember-me">
                <input type="checkbox" />
                <span>Remember me</span>
              </label>
              <a href="#" className="forgot-password">Forgot password?</a>
            </div>

            <button
              type="submit"
              className="btn btn-primary btn-login"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <span className="spinner-small"></span>
                  Logging in...
                </>
              ) : (
                <>
                  <span>Login</span>
                  <span className="arrow">→</span>
                </>
              )}
            </button>

            <div className="divider">
              <span>OR</span>
            </div>

            <button
              type="button"
              className="btn btn-secondary btn-guest"
              onClick={handleGuestMode}
            >
              Continue as Guest
            </button>

            <div className="signup-link">
              <p>Don't have an account? <a href="#" onClick={(e) => { e.preventDefault(); }}>Sign up</a></p>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default LoginPage

