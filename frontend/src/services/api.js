// frontend/src/services/api.js
import axios from 'axios'
import { useAuthStore } from '../store/auth'

// Create axios instance
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()

    // Add auth token if available
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }

    console.log('API Request:', {
      url: config.url,
      method: config.method,
      headers: config.headers,
      hasToken: !!authStore.token
    })

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config
    const authStore = useAuthStore()

    console.error('API Error:', {
      url: originalRequest?.url,
      status: error.response?.status,
      message: error.message
    })

    // Handle 401/403 errors (unauthorized)
    if ((error.response?.status === 401 || error.response?.status === 403) && !originalRequest._retry) {
      originalRequest._retry = true

      // If we have a refresh token, try to refresh
      if (authStore.refreshToken) {
        const refreshed = await authStore.refreshAccessToken()

        if (refreshed) {
          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${authStore.token}`
          return api(originalRequest)
        }
      }

      // Refresh failed or no refresh token, logout user
      authStore.logout()

      // Only redirect if we're not already on login page
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

export default api
