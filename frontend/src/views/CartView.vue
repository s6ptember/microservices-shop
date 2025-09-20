<!-- frontend/src/views/CartView.vue -->
<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <!-- Header -->
    <div class="flex items-center justify-between mb-10">
      <h1 class="text-4xl font-extrabold text-gray-900">Shopping Cart</h1>
      <router-link
        to="/catalog"
        class="text-gray-600 hover:text-black flex items-center transition-colors duration-200"
      >
        <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16l-4-4m0 0l4-4m-4 4h18" />
        </svg>
        Continue Shopping
      </router-link>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-16">
      <LoadingSpinner size="lg" text="Loading cart..." />
    </div>

    <!-- Empty Cart -->
    <div v-else-if="isEmpty" class="text-center py-16 bg-white rounded-xl shadow-sm">
      <svg class="mx-auto h-16 w-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l-2.5 5m0 0h10.5" />
      </svg>
      <h3 class="mt-3 text-xl font-semibold text-gray-900">Your cart is empty</h3>
      <p class="mt-2 text-gray-500">Start adding some items to your cart!</p>
      <div class="mt-6">
        <BaseButton
          variant="primary"
          @click="$router.push('/catalog')"
        >
          Start Shopping
        </BaseButton>
      </div>
    </div>

    <!-- Cart Content -->
    <div v-else class="lg:grid lg:grid-cols-12 lg:gap-8">
      <!-- Cart Items -->
      <div class="lg:col-span-8">
        <div class="bg-white rounded-xl shadow-sm border border-gray-100">
          <div class="px-6 py-5 border-b border-gray-100">
            <h2 class="text-xl font-semibold text-gray-900">
              Cart Items ({{ totalItems }} {{ totalItems === 1 ? 'item' : 'items' }})
            </h2>
          </div>

          <div class="divide-y divide-gray-100">
            <div
              v-for="item in cartItems"
              :key="item.id"
              class="p-6 flex"
            >
              <!-- Product Image -->
              <div class="flex-shrink-0">
                <ProductImage
                  :product="getProductForItem(item)"
                  size="sm"
                  container-class="w-24 h-24 rounded-lg"
                />
              </div>

              <!-- Product Details -->
              <div class="ml-6 flex-1">
                <div class="flex items-start justify-between">
                  <div>
                    <h3 class="text-lg font-semibold text-gray-900">
                      <router-link
                        :to="`/products/${item.product_id}`"
                        class="hover:text-black transition-colors duration-200"
                      >
                        {{ item.product_name }}
                      </router-link>
                    </h3>
                    <p class="mt-1 text-sm text-gray-500">
                      ${{ formatPrice(item.price) }} each
                    </p>

                    <!-- Stock Warning -->
                    <div
                      v-if="item.product_info && item.quantity > item.product_info.stock_quantity"
                      class="mt-2 flex items-center text-amber-500"
                    >
                      <svg class="w-5 h-5 mr-1.5" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                      </svg>
                      <span class="text-sm">Only {{ item.product_info.stock_quantity }} left in stock</span>
                    </div>

                    <!-- Price Change Warning -->
                    <div
                      v-if="item.product_info && item.price !== item.product_info.current_price"
                      class="mt-2 flex items-center text-blue-500"
                    >
                      <svg class="w-5 h-5 mr-1.5" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
                      </svg>
                      <span class="text-sm">
                        Price changed to ${{ formatPrice(item.product_info.current_price) }}
                      </span>
                    </div>
                  </div>

                  <!-- Remove Button -->
                  <button
                    @click="removeItem(item.id)"
                    class="ml-4 text-gray-400 hover:text-red-500 transition-colors duration-200"
                    :disabled="updatingItems.has(item.id)"
                  >
                    <span class="sr-only">Remove</span>
                    <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>

                <!-- Quantity Controls -->
                <div class="mt-4 flex items-center space-x-4">
                  <label class="sr-only">Quantity</label>
                  <div class="flex items-center border border-gray-200 rounded-lg overflow-hidden">
                    <button
                      @click="updateQuantity(item.id, item.quantity - 1)"
                      :disabled="item.quantity <= 1 || updatingItems.has(item.id)"
                      class="p-2.5 text-gray-600 hover:text-black disabled:opacity-40 disabled:cursor-not-allowed transition-colors duration-200"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                      </svg>
                    </button>

                    <input
                      :value="item.quantity"
                      @blur="updateQuantity(item.id, $event.target.value)"
                      type="number"
                      min="1"
                      :max="item.product_info?.stock_quantity || 999"
                      class="w-16 text-center border-none focus:ring-0 focus:outline-none text-gray-900 text-sm"
                      :disabled="updatingItems.has(item.id)"
                    >

                    <button
                      @click="updateQuantity(item.id, item.quantity + 1)"
                      :disabled="updatingItems.has(item.id) || (item.product_info && item.quantity >= item.product_info.stock_quantity)"
                      class="p-2.5 text-gray-600 hover:text-black disabled:opacity-40 disabled:cursor-not-allowed transition-colors duration-200"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                      </svg>
                    </button>
                  </div>

                  <div class="flex items-center text-sm text-gray-600">
                    <span v-if="updatingItems.has(item.id)" class="flex items-center">
                      <div class="spinner mr-2"></div>
                      Updating...
                    </span>
                    <span v-else>
                      Subtotal: ${{ formatPrice(item.subtotal) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Clear Cart Button -->
        <div class="mt-6 flex justify-end">
          <BaseButton
            variant="outline"
            @click="clearAllItems"
            :loading="clearingCart"
          >
            Clear Cart
          </BaseButton>
        </div>
      </div>

      <!-- Order Summary -->
      <div class="mt-8 lg:mt-0 lg:col-span-4">
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 sticky top-8">
          <div class="px-6 py-5 border-b border-gray-100">
            <h2 class="text-xl font-semibold text-gray-900">Order Summary</h2>
          </div>

          <div class="p-6">
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <dt class="text-sm text-gray-600">Subtotal</dt>
                <dd class="text-sm font-medium text-gray-900">${{ formatPrice(totalAmount) }}</dd>
              </div>

              <div class="flex items-center justify-between">
                <dt class="text-sm text-gray-600">Shipping</dt>
                <dd class="text-sm font-medium text-gray-900">Free</dd>
              </div>

              <div class="flex items-center justify-between">
                <dt class="text-sm text-gray-600">Tax</dt>
                <dd class="text-sm font-medium text-gray-900">${{ formatPrice(totalAmount * 0.1) }}</dd>
              </div>

              <div class="border-t border-gray-100 pt-4 flex items-center justify-between">
                <dt class="text-lg font-semibold text-gray-900">Order total</dt>
                <dd class="text-lg font-semibold text-gray-900">${{ formatPrice(totalAmount * 1.1) }}</dd>
              </div>
            </div>

            <div class="mt-6">
              <BaseButton
                variant="primary"
                size="lg"
                block
                @click="proceedToCheckout"
                :disabled="!isAuthenticated || isEmpty"
              >
                Proceed to Checkout
              </BaseButton>

              <p v-if="!isAuthenticated" class="mt-2 text-sm text-center text-gray-600">
                Please <router-link to="/login" class="text-black hover:text-gray-700 font-medium transition-colors duration-200">sign in</router-link> to checkout
              </p>
            </div>

            <!-- Promo Code -->
            <div class="mt-6 border-t border-gray-100 pt-6">
              <label for="promo-code" class="block text-sm font-medium text-gray-700">
                Promo code
              </label>
              <div class="mt-1 flex space-x-2">
                <input
                  id="promo-code"
                  v-model="promoCode"
                  type="text"
                  placeholder="Enter promo code"
                  class="flex-1 px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-black text-sm"
                >
                <BaseButton
                  variant="outline"
                  size="sm"
                  @click="applyPromoCode"
                  :disabled="!promoCode.trim()"
                >
                  Apply
                </BaseButton>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Checkout Modal -->
    <CheckoutModal
      v-if="showCheckoutModal"
      :cart-items="cartItems"
      :total-amount="totalAmount * 1.1"
      @close="showCheckoutModal = false"
      @order-placed="handleOrderPlaced"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '../components/common/BaseButton.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import ProductImage from '../components/common/ProductImage.vue'
import CheckoutModal from '../components/checkout/CheckoutModal.vue'
import { useCartStore } from '../store/cart.js'
import { useAuthStore } from '../store/auth.js'
import { useToast } from '../composables/useToast.js'

export default {
  name: 'CartView',
  components: {
    BaseButton,
    LoadingSpinner,
    ProductImage,
    CheckoutModal
  },
  setup() {
    const router = useRouter()
    const cartStore = useCartStore()
    const authStore = useAuthStore()
    const { showSuccess, showError } = useToast()

    // Reactive data
    const updatingItems = ref(new Set())
    const clearingCart = ref(false)
    const promoCode = ref('')
    const showCheckoutModal = ref(false)

    // Computed
    const cartItems = computed(() => cartStore.cartItems)
    const totalItems = computed(() => cartStore.totalItems)
    const totalAmount = computed(() => cartStore.totalAmount)
    const isEmpty = computed(() => cartStore.isEmpty)
    const loading = computed(() => cartStore.loading)
    const isAuthenticated = computed(() => authStore.isAuthenticated)

    // Methods
    const formatPrice = (price) => {
      return parseFloat(price).toFixed(2)
    }

    const getProductForItem = (item) => {
      // Create a product object for the ProductImage component
      return {
        id: item.product_id,
        name: item.product_name,
        category_name: item.product_info?.category_name || 'Product',
        image_url: item.product_info?.image_url || null
      }
    }

    const updateQuantity = async (itemId, newQuantity) => {
      const quantity = parseInt(newQuantity)

      if (quantity < 1) return

      try {
        updatingItems.value.add(itemId)

        const result = await cartStore.updateCartItem(itemId, quantity)
        if (!result.success) {
          showError(result.error || 'Failed to update quantity')
        }
      } catch (error) {
        console.error('Error updating quantity:', error)
        showError('Failed to update quantity')
      } finally {
        updatingItems.value.delete(itemId)
      }
    }

    const removeItem = async (itemId) => {
      try {
        updatingItems.value.add(itemId)

        const result = await cartStore.removeCartItem(itemId)
        if (result.success) {
          showSuccess('Item removed from cart')
        } else {
          showError(result.error || 'Failed to remove item')
        }
      } catch (error) {
        console.error('Error removing item:', error)
        showError('Failed to remove item')
      } finally {
        updatingItems.value.delete(itemId)
      }
    }

    const clearAllItems = async () => {
      try {
        clearingCart.value = true

        const result = await cartStore.clearCart()
        if (result.success) {
          showSuccess('Cart cleared successfully')
        } else {
          showError(result.error || 'Failed to clear cart')
        }
      } catch (error) {
        console.error('Error clearing cart:', error)
        showError('Failed to clear cart')
      } finally {
        clearingCart.value = false
      }
    }

    const applyPromoCode = () => {
      // TODO: Implement promo code logic
      showSuccess('Promo code functionality coming soon!')
    }

    const proceedToCheckout = () => {
      if (!isAuthenticated.value) {
        router.push('/login?redirect=/cart')
        return
      }

      if (isEmpty.value) {
        showError('Your cart is empty')
        return
      }

      // Show checkout modal
      showCheckoutModal.value = true
    }

    const handleOrderPlaced = (orderData) => {
      showCheckoutModal.value = false
      showSuccess(`Order #${orderData.id} placed successfully!`)

      // Optionally redirect to order confirmation page
      router.push(`/orders/${orderData.id}`)
    }

    // Lifecycle
    onMounted(async () => {
      await cartStore.fetchCart()
    })

    return {
      // Data
      updatingItems,
      clearingCart,
      promoCode,
      showCheckoutModal,

      // Computed
      cartItems,
      totalItems,
      totalAmount,
      isEmpty,
      loading,
      isAuthenticated,

      // Methods
      formatPrice,
      getProductForItem,
      updateQuantity,
      removeItem,
      clearAllItems,
      applyPromoCode,
      proceedToCheckout,
      handleOrderPlaced
    }
  }
}
</script>
