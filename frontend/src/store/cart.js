// frontend/src/store/cart.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import cartService from '../services/cart.js'
import { useAuthStore } from './auth.js'

export const useCartStore = defineStore('cart', () => {
  // State
  const cartItems = ref([])
  const loading = ref(false)
  const lastUpdated = ref(null)

  // Getters
  const totalItems = computed(() => {
    return cartItems.value.reduce((total, item) => total + item.quantity, 0)
  })

  const totalAmount = computed(() => {
    return cartItems.value.reduce((total, item) => total + (item.price * item.quantity), 0)
  })

  const itemsCount = computed(() => cartItems.value.length)

  const isEmpty = computed(() => cartItems.value.length === 0)

  // Actions
  async function fetchCart() {
    const authStore = useAuthStore()

    if (!authStore.isAuthenticated) {
      console.log('User not authenticated, clearing cart')
      cartItems.value = []
      return { success: true }
    }

    try {
      loading.value = true
      console.log('Fetching cart...')

      const response = await cartService.getCart()
      console.log('Cart fetch response:', response.data)

      if (response.data) {
        cartItems.value = response.data.items || []
        lastUpdated.value = new Date()
        console.log('Cart fetched successfully:', cartItems.value.length, 'items')
        return { success: true }
      }

      return { success: false, error: 'Failed to fetch cart' }
    } catch (error) {
      console.error('Fetch cart error:', error)

      // If user is not authenticated, just clear the cart
      if (error.response?.status === 401 || error.response?.status === 403) {
        cartItems.value = []
        return { success: true }
      }

      return {
        success: false,
        error: error.response?.data?.error || 'Failed to fetch cart'
      }
    } finally {
      loading.value = false
    }
  }

  async function addToCart(productId, quantity = 1) {
    const authStore = useAuthStore()

    if (!authStore.isAuthenticated) {
      console.error('User not authenticated for addToCart')
      return {
        success: false,
        error: 'Please sign in to add items to cart'
      }
    }

    try {
      console.log('Adding to cart:', { productId, quantity })
      console.log('Auth token available:', !!authStore.token)

      const response = await cartService.addToCart({
        product_id: productId,
        quantity: quantity
      })

      console.log('Add to cart response:', response.data)

      if (response.data) {
        // Refresh cart after adding
        await fetchCart()
        return { success: true, data: response.data }
      }

      return { success: false, error: 'Failed to add item to cart' }
    } catch (error) {
      console.error('Add to cart error:', error)
      console.error('Error details:', {
        status: error.response?.status,
        data: error.response?.data,
        message: error.message
      })

      return {
        success: false,
        error: error.response?.data?.error || error.message || 'Failed to add item to cart'
      }
    }
  }

  async function updateCartItem(itemId, quantity) {
    try {
      const response = await cartService.updateCartItem(itemId, { quantity })

      if (response.data) {
        // Update local cart
        const itemIndex = cartItems.value.findIndex(item => item.id === itemId)
        if (itemIndex !== -1) {
          cartItems.value[itemIndex].quantity = quantity
        }
        return { success: true, data: response.data }
      }

      return { success: false, error: 'Failed to update cart item' }
    } catch (error) {
      console.error('Update cart item error:', error)
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to update cart item'
      }
    }
  }

  async function removeCartItem(itemId) {
    try {
      await cartService.removeCartItem(itemId)

      // Remove from local cart
      cartItems.value = cartItems.value.filter(item => item.id !== itemId)

      return { success: true }
    } catch (error) {
      console.error('Remove cart item error:', error)
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to remove cart item'
      }
    }
  }

  async function clearCart() {
    try {
      await cartService.clearCart()
      cartItems.value = []
      return { success: true }
    } catch (error) {
      console.error('Clear cart error:', error)
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to clear cart'
      }
    }
  }

  async function getCartSummary() {
    try {
      const response = await cartService.getCartSummary()
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Get cart summary error:', error)
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to get cart summary'
      }
    }
  }

  function getCartItem(productId) {
    return cartItems.value.find(item => item.product_id === productId)
  }

  function isInCart(productId) {
    return cartItems.value.some(item => item.product_id === productId)
  }

  function reset() {
    cartItems.value = []
    loading.value = false
    lastUpdated.value = null
  }

  return {
    // State
    cartItems,
    loading,
    lastUpdated,

    // Getters
    totalItems,
    totalAmount,
    itemsCount,
    isEmpty,

    // Actions
    fetchCart,
    addToCart,
    updateCartItem,
    removeCartItem,
    clearCart,
    getCartSummary,
    getCartItem,
    isInCart,
    reset
  }
})
