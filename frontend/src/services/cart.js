// frontend/src/services/cart.js
import api from './api'

const cartService = {
  async getCart() {
    return await api.get('/cart/')
  },

  async addToCart(data) {
    return await api.post('/cart/add/', data)
  },

  async updateCartItem(itemId, data) {
    return await api.put(`/cart/update/${itemId}/`, data)
  },

  async removeCartItem(itemId) {
    return await api.delete(`/cart/remove/${itemId}/`)
  },

  async clearCart() {
    return await api.delete('/cart/clear/')
  },

  async getCartSummary() {
    return await api.get('/cart/summary/')
  }
}

export default cartService
