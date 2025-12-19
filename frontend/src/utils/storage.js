/**
 * Local storage utilities for user preferences
 * All data is stored locally and encrypted where sensitive
 */

const STORAGE_KEY = 'inclusiveai_preferences'
const CONSENT_KEY = 'inclusiveai_consent'

/**
 * Get stored user preferences
 */
export const getStoredPreferences = () => {
  try {
    const data = localStorage.getItem(STORAGE_KEY)
    return data ? JSON.parse(data) : null
  } catch (error) {
    console.error('Error reading preferences:', error)
    return null
  }
}

/**
 * Save user preferences
 */
export const savePreferences = (preferences) => {
  try {
    const data = {
      ...preferences,
      updatedAt: new Date().toISOString()
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
    return true
  } catch (error) {
    console.error('Error saving preferences:', error)
    return false
  }
}

/**
 * Get consent status
 */
export const getConsentStatus = () => {
  try {
    const data = localStorage.getItem(CONSENT_KEY)
    return data ? JSON.parse(data) : null
  } catch (error) {
    return null
  }
}

/**
 * Save consent status
 */
export const saveConsent = (consentData) => {
  try {
    const data = {
      ...consentData,
      timestamp: new Date().toISOString()
    }
    localStorage.setItem(CONSENT_KEY, JSON.stringify(data))
    return true
  } catch (error) {
    console.error('Error saving consent:', error)
    return false
  }
}

/**
 * Delete all user data (privacy feature)
 */
export const deleteAllUserData = () => {
  try {
    localStorage.removeItem(STORAGE_KEY)
    localStorage.removeItem(CONSENT_KEY)
    localStorage.removeItem('inclusiveai_camera_data')
    return true
  } catch (error) {
    console.error('Error deleting user data:', error)
    return false
  }
}

/**
 * Clear camera-derived data only
 */
export const clearCameraData = () => {
  try {
    localStorage.removeItem('inclusiveai_camera_data')
    return true
  } catch (error) {
    console.error('Error clearing camera data:', error)
    return false
  }
}

