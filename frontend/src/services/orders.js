// frontend/src/services/orders.js
import api from './api'

const orderService = {
  async getUserOrders(params = {}) {
    return await api.get('/orders/', { params })
  },

  async getOrder(orderId) {
    return await api.get(`/orders/${orderId}/`)
  },

  async createOrder(data) {
    console.log('Creating order with data:', data)
    return await api.post('/orders/create/', data)
  },

  async getOrderStatistics() {
    return await api.get('/orders/statistics/')
  },

  async updateOrderStatus(orderId, status) {
    return await api.put(`/orders/${orderId}/status/`, { status })
  }
}

export default orderService
