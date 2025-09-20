<!-- frontend/src/views/OrdersView.vue -->
<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">My Orders</h1>
      <p class="mt-2 text-sm text-gray-500">Track and manage your orders</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-16">
      <LoadingSpinner size="lg" text="Loading orders..." />
    </div>

    <!-- Empty State -->
    <div v-else-if="orders.length === 0" class="text-center py-16">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
      </svg>
      <h3 class="mt-4 text-lg font-semibold text-gray-900">No orders yet</h3>
      <p class="mt-2 text-sm text-gray-500">Start shopping to see your orders here.</p>
      <div class="mt-6">
        <BaseButton variant="primary" @click="$router.push('/catalog')" class="bg-gray-900 text-white hover:bg-gray-800">
          Start Shopping
        </BaseButton>
      </div>
    </div>

    <!-- Orders List -->
    <div v-else class="space-y-6">
      <div
        v-for="order in orders"
        :key="order.id"
        class="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden"
      >
        <!-- Order Header -->
        <div class="px-6 py-4 border-b border-gray-100 bg-gray-50">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-semibold text-gray-900">
                Order #{{ order.id }}
              </h3>
              <p class="text-sm text-gray-500 mt-1">
                Placed on {{ formatDate(order.created_at) }}
              </p>
            </div>
            <div class="text-right">
              <p class="text-lg font-semibold text-gray-900">
                ${{ formatPrice(order.total_amount) }}
              </p>
              <span :class="getStatusClasses(order.status)" class="inline-block px-3 py-1 rounded-full text-sm font-medium">
                {{ getStatusText(order.status) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Order Items -->
        <div class="px-6 py-4">
          <h4 class="text-sm font-semibold text-gray-900 mb-3">Items ({{ order.items_count }})</h4>
          <div class="space-y-3">
            <div
              v-for="item in order.items"
              :key="item.id"
              class="flex items-center space-x-4 hover:bg-gray-50 transition-colors"
            >
              <div class="flex-shrink-0">
                <ProductImage
                  :product="getProductForItem(item)"
                  size="sm"
                  container-class="w-12 h-12 rounded-md"
                />
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-semibold text-gray-900 truncate">
                  {{ item.product_name }}
                </p>
                <p class="text-sm text-gray-500 mt-1">
                  Qty: {{ item.quantity }} × ${{ formatPrice(item.price) }}
                </p>
              </div>
              <div class="text-sm font-semibold text-gray-900">
                ${{ formatPrice(item.subtotal) }}
              </div>
            </div>
          </div>
        </div>

        <!-- Order Footer -->
        <div class="px-6 py-4 border-t border-gray-100 bg-gray-50">
          <div class="flex items-center justify-between">
            <div class="text-sm text-gray-500">
              <p><strong>Shipping Address:</strong></p>
              <p>{{ order.shipping_address }}</p>
            </div>
            <div class="flex space-x-3">
              <BaseButton
                variant="outline"
                size="sm"
                @click="viewOrderDetails(order.id)"
                class="border-gray-900 text-gray-900 hover:bg-gray-900 hover:text-white"
              >
                View Details
              </BaseButton>
              <BaseButton
                v-if="order.status === 'pending'"
                variant="ghost"
                size="sm"
                @click="cancelOrder(order.id)"
                class="text-gray-600 hover:text-gray-900"
              >
                Cancel Order
              </BaseButton>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="mt-8 flex items-center justify-center">
      <div class="flex items-center space-x-2">
        <BaseButton
          variant="outline"
          size="sm"
          :disabled="currentPage === 1"
          @click="changePage(currentPage - 1)"
          class="border-gray-900 text-gray-900 hover:bg-gray-900 hover:text-white"
        >
          Previous
        </BaseButton>

        <div class="flex items-center space-x-1">
          <button
            v-for="page in visiblePages"
            :key="page"
            @click="changePage(page)"
            :class="[
              'px-3 py-2 text-sm font-medium rounded-md transition-colors',
              page === currentPage
                ? 'bg-gray-900 text-white'
                : 'text-gray-600 hover:bg-gray-100'
            ]"
          >
            {{ page }}
          </button>
        </div>

        <BaseButton
          variant="outline"
          size="sm"
          :disabled="currentPage === totalPages"
          @click="changePage(currentPage + 1)"
          class="border-gray-900 text-gray-900 hover:bg-gray-900 hover:text-white"
        >
          Next
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '../components/common/BaseButton.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import ProductImage from '../components/common/ProductImage.vue'
import { useToast } from '../composables/useToast.js'
import orderService from '../services/orders.js'

export default {
  name: 'OrdersView',
  components: {
    BaseButton,
    LoadingSpinner,
    ProductImage
  },
  setup() {
    const router = useRouter()
    const { showSuccess, showError } = useToast()

    // Reactive data
    const orders = ref([])
    const loading = ref(false)
    const currentPage = ref(1)
    const totalPages = ref(1)

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
      const classes = 'px-2 py-1 text-xs font-medium rounded-full '

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
        category_name: 'Product', // Default category for orders
        image_url: null // Will use icon fallback
      }
    }

    const fetchOrders = async (page = 1) => {
      try {
        loading.value = true
        const response = await orderService.getUserOrders({
          page: page,
          page_size: 10
        })

        if (response.data) {
          orders.value = response.data.results || response.data

          // Handle pagination
          if (response.data.count !== undefined) {
            totalPages.value = Math.ceil(response.data.count / 10)
          }
        }
      } catch (error) {
        console.error('Error fetching orders:', error)
        showError('Failed to load orders')
      } finally {
        loading.value = false
      }
    }

    const changePage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
        fetchOrders(page)
      }
    }

    const visiblePages = computed(() => {
      const pages = []
      const total = totalPages.value
      const current = currentPage.value

      if (total <= 7) {
        for (let i = 1; i <= total; i++) {
          pages.push(i)
        }
      } else {
        if (current <= 4) {
          for (let i = 1; i <= 5; i++) {
            pages.push(i)
          }
          pages.push('...')
          pages.push(total)
        } else if (current >= total - 3) {
          pages.push(1)
          pages.push('...')
          for (let i = total - 4; i <= total; i++) {
            pages.push(i)
          }
        } else {
          pages.push(1)
          pages.push('...')
          for (let i = current - 1; i <= current + 1; i++) {
            pages.push(i)
          }
          pages.push('...')
          pages.push(total)
        }
      }

      return pages
    })

    const viewOrderDetails = (orderId) => {
      router.push(`/orders/${orderId}`)
    }

    const cancelOrder = async (orderId) => {
      try {
        await orderService.updateOrderStatus(orderId, 'cancelled')
        showSuccess('Order cancelled successfully')
        await fetchOrders(currentPage.value)
      } catch (error) {
        console.error('Error cancelling order:', error)
        showError('Failed to cancel order')
      }
    }

    // Lifecycle
    onMounted(() => {
      fetchOrders()
    })

    return {
      // Data
      orders,
      loading,
      currentPage,
      totalPages,

      // Computed
      visiblePages,

      // Methods
      formatPrice,
      formatDate,
      getStatusClasses,
      getStatusText,
      getProductForItem,
      changePage,
      viewOrderDetails,
      cancelOrder
    }
  }
}
</script>
