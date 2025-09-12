import api from './api'

const productService = {
  async getProducts(params = {}) {
    return await api.get('/products/', { params })
  },

  async getProduct(id) {
    return await api.get(`/products/${id}/`)
  },

  async getCategories(params = {}) {
    return await api.get('/categories/', { params })
  },

  async getCategory(slug) {
    return await api.get(`/categories/${slug}/`)
  },

  async checkAvailability(productId, quantity) {
    return await api.get(`/products/${productId}/check-availability/`, {
      params: { quantity }
    })
  }
}

export default productService
