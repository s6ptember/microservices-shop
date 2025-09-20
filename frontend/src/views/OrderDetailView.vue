<!-- frontend/src/views/OrderDetailView.vue -->
<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <!-- Breadcrumb -->
    <nav class="flex mb-8" aria-label="Breadcrumb">
      <ol class="inline-flex items-center space-x-2 md:space-x-4">
        <li class="inline-flex items-center">
          <router-link to="/" class="text-gray-600 hover:text-gray-900 inline-flex items-center text-sm font-medium">
            <svg class="w-4 h-4 mr-2 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"></path>
            </svg>
            Home
          </router-link>
        </li>
        <li>
          <div class="flex items-center">
            <svg class="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
            </svg>
            <router-link to="/orders" class="ml-2 text-gray-600 hover:text-gray-900 text-sm font-medium">Orders</router-link>
          </div>
        </li>
        <li v-if="order">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
            </svg>
            <span class="ml-2 text-gray-500 text-sm font-medium">Order #{{ order.id }}</span>
          </div>
        </li>
      </ol>
    </nav>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-16">
      <LoadingSpinner size="lg" text="Loading order..." />
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-16">
      <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-50">
        <svg class="h-6 w-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
      </div>
      <h3 class="mt-4 text-lg font-semibold text-gray-900">Order not found</h3>
      <p class="mt-2 text-sm text-gray-500">{{ error }}</p>
      <div class="mt-6">
        <BaseButton variant="primary" @click="$router.push('/orders')">
          Back to Orders
        </BaseButton>
      </div>
    </div>

    <!-- Order Details -->
    <div v-else-if="order" class="space-y-6">
      <!-- Order Header -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-6">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Order #{{ order.id }}</h1>
            <p class="text-sm text-gray-500 mt-1">Placed on {{ formatDate(order.created_at) }}</p>
          </div>
          <div class="text-right">
            <span :class="getStatusClasses(order.status)" class="inline-block px-3 py-1 rounded-full text-sm font-medium">
              {{ getStatusText(order.status) }}
            </span>
            <p class="text-xl font-semibold text-gray-900 mt-2">
              ${{ formatPrice(order.total_amount) }}
            </p>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <h3 class="text-sm font-semibold text-gray-900 mb-2">Customer Information</h3>
            <div class="text-sm text-gray-600">
              <p>{{ order.user_name }}</p>
              <p>{{ order.user_email }}</p>
            </div>
          </div>
          <div>
            <h3 class="text-sm font-semibold text-gray-900 mb-2">Shipping Address</h3>
            <div class="text-sm text-gray-600">
              <p>{{ order.shipping_address }}</p>
            </div>
          </div>
          <div>
            <h3 class="text-sm font-semibold text-gray-900 mb-2">Order Summary</h3>
            <div class="text-sm text-gray-600">
              <p>{{ order.items_count }} items</p>
              <p>{{ order.total_quantity }} total quantity</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Order Items -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-100">
        <div class="px-6 py-4 border-b border-gray-100">
          <h2 class="text-lg font-semibold text-gray-900">Order Items</h2>
        </div>
        <div class="divide-y divide-gray-100">
          <div
            v-for="item in order.items"
            :key="item.id"
            class="p-6 flex items-center space-x-4 hover:bg-gray-50 transition-colors"
          >
            <div class="flex-shrink-0">
              <ProductImage
                :product="getProductForItem(item)"
                size="sm"
                container-class="w-16 h-16 rounded-md"
              />
            </div>
            <div class="flex-1 min-w-0">
              <h3 class="text-base font-semibold text-gray-900">
                {{ item.product_name }}
              </h3>
              <p class="text-sm text-gray-500 mt-1">
                ${{ formatPrice(item.price) }} × {{ item.quantity }}
              </p>
            </div>
            <div class="text-base font-semibold text-gray-900">
              ${{ formatPrice(item.subtotal) }}
            </div>
          </div>
        </div>

        <!-- Order Total -->
        <div class="px-6 py-4 border-t border-gray-100 bg-gray-50">
          <div class="flex justify-end">
            <div class="text-right">
              <p class="text-base font-semibold text-gray-900">
                Total: ${{ formatPrice(order.total_amount) }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Order Actions -->
      <div class="flex justify-between">
        <BaseButton
          variant="outline"
          @click="$router.push('/orders')"
          class="border-gray-900 text-gray-900 hover:bg-gray-900 hover:text-white"
        >
          Back to Orders
        </BaseButton>

        <div class="flex space-x-3">
          <BaseButton
            v-if="order.status === 'pending'"
            variant="outline"
            @click="cancelOrder"
            :loading="cancelling"
            class="border-gray-900 text-gray-900 hover:bg-gray-900 hover:text-white"
          >
            Cancel Order
          </BaseButton>
          <BaseButton
            variant="primary"
            @click="reorder"
            class="bg-gray-900 text-white hover:bg-gray-800"
          >
            Reorder Items
          </BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BaseButton from '../components/common/BaseButton.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import ProductImage from '../components/common/ProductImage.vue'
import { useToast } from '../composables/useToast.js'
import { useCartStore } from '../store/cart.js'
import orderService from '../services/orders.js'

export default {
  name: 'OrderDetailView',
  components: {
    BaseButton,
    LoadingSpinner,
    ProductImage
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const { showSuccess, showError } = useToast()
    const cartStore = useCartStore()

    // Reactive data
    const order = ref(null)
    const loading = ref(false)
    const error = ref('')
    const cancelling = ref(false)

    // Methods
    const formatPrice = (price) => {
      return parseFloat(price).toFixed(2)
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const getStatusClasses = (status) => {
      const classes = 'px-3 py-1 text-sm font-medium rounded-full '

      switch (status) {
        case 'pending':
          return classes + 'bg-yellow-100 text-yellow-800'
        case 'confirmed':
          return classes + 'bg-blue-100 text-blue-800'
        case 'shipped':
          return classes + 'bg-purple-100 text-purple-800'
        case 'delivered':
          return classes + 'bg-green-100 text-green-800'
        case 'cancelled':
          return classes + 'bg-red-100 text-red-800'
        default:
          return classes + 'bg-gray-100 text-gray-800'
      }
    }

    const getStatusText = (status) => {
      const statusMap = {
        pending: 'Pending',
        confirmed: 'Confirmed',
        shipped: 'Shipped',
        delivered: 'Delivered',
        cancelled: 'Cancelled'
      }
      return statusMap[status] || status
    }

    const getProductForItem = (item) => {
      return {
        id: item.product_id,
        name: item.product_name,
        category_name: 'Product',
        image_url: null
      }
    }

    const fetchOrder = async () => {
      try {
        loading.value = true
        error.value = ''

        const orderId = route.params.id
        const response = await orderService.getOrder(orderId)

        if (response.data) {
          order.value = response.data
        } else {
          error.value = 'Order not found'
        }
      } catch (err) {
        console.error('Error fetching order:', err)
        if (err.response?.status === 404) {
          error.value = 'Order not found'
        } else {
          error.value = 'Failed to load order details'
        }
      } finally {
        loading.value = false
      }
    }

    const cancelOrder = async () => {
      try {
        cancelling.value = true

        await orderService.updateOrderStatus(order.value.id, 'cancelled')
        order.value.status = 'cancelled'

        showSuccess('Order cancelled successfully')
      } catch (error) {
        console.error('Error cancelling order:', error)
        showError('Failed to cancel order')
      } finally {
        cancelling.value = false
      }
    }

    const reorder = async () => {
      try {
        // Add all items from this order to cart
        for (const item of order.value.items) {
          await cartStore.addToCart(item.product_id, item.quantity)
        }

        showSuccess('Items added to cart!')
        router.push('/cart')
      } catch (error) {
        console.error('Error reordering:', error)
        showError('Failed to add items to cart')
      }
    }

    // Lifecycle
    onMounted(() => {
      fetchOrder()
    })

    return {
      // Data
      order,
      loading,
      error,
      cancelling,

      // Methods
      formatPrice,
      formatDate,
      getStatusClasses,
      getStatusText,
      getProductForItem,
      cancelOrder,
      reorder
    }
  }
}
</script>
