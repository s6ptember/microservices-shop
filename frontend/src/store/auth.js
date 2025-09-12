// frontend/src/store/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import authService from '../services/auth.js'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(localStorage.getItem('access_token') || null)
  const refreshToken = ref(localStorage.getItem('refresh_token') || null)
  const loading = ref(false)

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const userName = computed(() => {
    if (!user.value) return ''
    return `${user.value.first_name} ${user.value.last_name}`.trim() || user.value.email
  })

  // Actions
  async function login(credentials) {
    try {
      loading.value = true
      console.log('Attempting login with:', { email: credentials.email })

      const response = await authService.login(credentials)
      console.log('Login response:', response.data)

      if (response.data) {
        token.value = response.data.access
        refreshToken.value = response.data.refresh
        user.value = response.data.user

        // Store in localStorage
        localStorage.setItem('access_token', response.data.access)
        localStorage.setItem('refresh_token', response.data.refresh)

        console.log('Login successful, token stored:', !!token.value)
        return { success: true }
      }

      return { success: false, error: 'Invalid response from server' }
    } catch (error) {
      console.error('Login error:', error)
      return {
        success: false,
        error: error.response?.data?.error || 'Login failed'
      }
    } finally {
      loading.value = false
    }
  }

  async function register(userData) {
    try {
      loading.value = true
      const response = await authService.register(userData)

      if (response.data) {
        return { success: true, message: 'Registration successful' }
      }

      return { success: false, error: 'Registration failed' }
    } catch (error) {
      console.error('Registration error:', error)
      return {
        success: false,
        error: error.response?.data?.error || 'Registration failed'
      }
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    console.log('Logging out user')
    token.value = null
    refreshToken.value = null
    user.value = null

    // Clear localStorage
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  async function fetchProfile() {
    try {
      if (!token.value) {
        console.log('No token available for profile fetch')
        return
      }

      console.log('Fetching user profile...')
      const response = await authService.getProfile()
      if (response.data) {
        user.value = response.data
        console.log('Profile fetched successfully:', user.value)
      }
    } catch (error) {
      console.error('Fetch profile error:', error)
      if (error.response?.status === 401 || error.response?.status === 403) {
        console.log('Profile fetch failed with auth error, logging out')
        await logout()
      }
    }
  }

  async function refreshAccessToken() {
    try {
      if (!refreshToken.value) {
        console.log('No refresh token available')
        return false
      }

      console.log('Refreshing access token...')
      const response = await authService.refreshToken(refreshToken.value)
      if (response.data?.access) {
        token.value = response.data.access
        localStorage.setItem('access_token', response.data.access)
        console.log('Token refreshed successfully')
        return true
      }
    } catch (error) {
      console.error('Token refresh error:', error)
      await logout()
    }
    return false
  }

  // Initialize auth state
  async function initialize() {
    console.log('Initializing auth store...')
    console.log('Has stored token:', !!token.value)

    if (token.value) {
      await fetchProfile()
    }
  }

  return {
    // State
    user,
    token,
    refreshToken,
    loading,

    // Getters
    isAuthenticated,
    userName,

    // Actions
    login,
    register,
    logout,
    fetchProfile,
    refreshAccessToken,
    initialize
  }
})
