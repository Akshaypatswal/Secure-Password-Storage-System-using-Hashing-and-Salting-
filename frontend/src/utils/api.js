import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

/**
 * Submit camera scan data for analysis
 * @param {Object} scanData - Keypoint summaries and features
 * @returns {Promise} Recommendation with confidence and cues
 */
export const submitAssistScan = async (scanData) => {
  try {
    const response = await api.post('/assist-scan', scanData)
    return response.data
  } catch (error) {
    console.error('Error submitting assist scan:', error)
    throw error
  }
}

/**
 * Save user preferences
 * @param {Object} preferences - User's selected assist mode and settings
 * @returns {Promise}
 */
export const saveUserPreferences = async (preferences) => {
  try {
    const response = await api.post('/preferences', preferences)
    return response.data
  } catch (error) {
    console.error('Error saving preferences:', error)
    throw error
  }
}

/**
 * Get assist mode preview/demo
 * @param {string} mode - Assist mode name
 * @returns {Promise}
 */
export const getAssistPreview = async (mode) => {
  try {
    const response = await api.get(`/assist-preview?mode=${mode}`)
    return response.data
  } catch (error) {
    console.error('Error fetching assist preview:', error)
    throw error
  }
}

/**
 * Login user
 * @param {Object} credentials - Username and password
 * @returns {Promise}
 */
export const loginUser = async (credentials) => {
  try {
    const response = await api.post('/auth/login', credentials)
    return response.data
  } catch (error) {
    console.error('Error logging in:', error)
    throw error
  }
}

/**
 * Register user
 * @param {Object} userData - Username and password
 * @returns {Promise}
 */
export const registerUser = async (userData) => {
  try {
    const response = await api.post('/auth/register', userData)
    return response.data
  } catch (error) {
    console.error('Error registering:', error)
    throw error
  }
}

export default api

