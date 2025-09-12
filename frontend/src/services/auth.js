import api from './api'

const authService = {
  async login(credentials) {
    return await api.post('/auth/login/', credentials)
  },

  async register(userData) {
    return await api.post('/users/register/', userData)
  },

  async refreshToken(refresh) {
    return await api.post('/auth/refresh/', { refresh })
  },

  async getProfile() {
    return await api.get('/users/profile/')
  },

  async updateProfile(userData) {
    return await api.put('/users/profile/update/', userData)
  },

  async logout() {
    // In a real app, you might want to call a logout endpoint
    // to invalidate the token on the server
    return Promise.resolve()
  }
}

export default authService
