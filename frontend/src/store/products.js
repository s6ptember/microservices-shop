import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import productService from '../services/products'

export const useProductsStore = defineStore('products', () => {
  // State
  const products = ref([])
  const categories = ref([])
  const currentProduct = ref(null)
  const loading = ref(false)
  const filters = ref({
    category: null,
    minPrice: null,
    maxPrice: null,
    search: '',
    inStock: false,
    sortBy: '-created_at'
  })
  const pagination = ref({
    currentPage: 1,
    totalPages: 0,
    totalCount: 0,
    pageSize: 20
  })

  // Getters
  const filteredProducts = computed(() => {
    let filtered = products.value

    if (filters.value.search) {
      const search = filters.value.search.toLowerCase()
      filtered = filtered.filter(product =>
        product.name.toLowerCase().includes(search) ||
        product.description.toLowerCase().includes(search)
      )
    }

    if (filters.value.category) {
      filtered = filtered.filter(product => product.category === filters.value.category)
    }

    if (filters.value.minPrice) {
      filtered = filtered.filter(product => product.price >= filters.value.minPrice)
    }

    if (filters.value.maxPrice) {
      filtered = filtered.filter(product => product.price <= filters.value.maxPrice)
    }

    if (filters.value.inStock) {
      filtered = filtered.filter(product => product.stock_quantity > 0)
    }

    return filtered
  })

  const availableCategories = computed(() => {
    return categories.value.filter(category => category.products_count > 0)
  })

  // Actions
  async function fetchProducts(params = {}) {
    try {
      loading.value = true
      const queryParams = {
        page: pagination.value.currentPage,
        page_size: pagination.value.pageSize,
        ...filters.value,
        ...params
      }

      const response = await productService.getProducts(queryParams)

      if (response.data) {
        products.value = response.data.results || response.data

        // Update pagination if response has pagination info
        if (response.data.count !== undefined) {
          pagination.value.totalCount = response.data.count
          pagination.value.totalPages = Math.ceil(response.data.count / pagination.value.pageSize)
        }
      }

      return { success: true }
    } catch (error) {
      console.error('Fetch products error:', error)
      return { success: false, error: error.message }
    } finally {
      loading.value = false
    }
  }

  async function fetchCategories() {
    try {
      const response = await productService.getCategories()
      if (response.data) {
        categories.value = response.data.results || response.data
      }
    } catch (error) {
      console.error('Fetch categories error:', error)
    }
  }

  async function fetchProduct(id) {
    try {
      loading.value = true
      const response = await productService.getProduct(id)

      if (response.data) {
        currentProduct.value = response.data
        return { success: true, data: response.data }
      }

      return { success: false, error: 'Product not found' }
    } catch (error) {
      console.error('Fetch product error:', error)
      return { success: false, error: error.message }
    } finally {
      loading.value = false
    }
  }

  function setFilters(newFilters) {
    filters.value = { ...filters.value, ...newFilters }
    pagination.value.currentPage = 1 // Reset to first page when filtering
  }

  function clearFilters() {
    filters.value = {
      category: null,
      minPrice: null,
      maxPrice: null,
      search: '',
      inStock: false,
      sortBy: '-created_at'
    }
    pagination.value.currentPage = 1
  }

  function setPage(page) {
    pagination.value.currentPage = page
  }

  function clearCurrentProduct() {
    currentProduct.value = null
  }

  return {
    // State
    products,
    categories,
    currentProduct,
    loading,
    filters,
    pagination,

    // Getters
    filteredProducts,
    availableCategories,

    // Actions
    fetchProducts,
    fetchCategories,
    fetchProduct,
    setFilters,
    clearFilters,
    setPage,
    clearCurrentProduct
  }
})
