<!-- frontend/src/views/ProductView.vue -->
<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
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
            <router-link to="/catalog" class="ml-2 text-gray-600 hover:text-gray-900 text-sm font-medium">Catalog</router-link>
          </div>
        </li>
        <li v-if="product">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
            </svg>
            <span class="ml-2 text-gray-500 text-sm font-medium">{{ product.name }}</span>
          </div>
        </li>
      </ol>
    </nav>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-16">
      <LoadingSpinner size="lg" text="Loading product..." />
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-16">
      <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-50">
        <svg class="h-6 w-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
      </div>
      <h3 class="mt-4 text-lg font-semibold text-gray-900">Product not found</h3>
      <p class="mt-2 text-sm text-gray-500">{{ error }}</p>
      <div class="mt-6">
        <BaseButton variant="primary" @click="$router.push('/catalog')" class="bg-gray-900 text-white hover:bg-gray-800">
          Back to Catalog
        </BaseButton>
      </div>
    </div>

    <!-- Product Details -->
    <div v-else-if="product" class="lg:grid lg:grid-cols-2 lg:gap-x-8 lg:items-start">
      <!-- Image Gallery -->
      <div class="flex flex-col-reverse">
        <!-- Image selector -->
        <div class="mt-6 w-full max-w-2xl mx-auto sm:block lg:max-w-none">
          <div class="grid grid-cols-4 gap-4">
            <div v-for="i in 4" :key="i" class="relative h-24 bg-white rounded-md flex items-center justify-center text-sm font-medium uppercase text-gray-900 cursor-pointer hover:bg-gray-50 transition-colors focus:outline-none focus:ring-2 focus:ring-gray-900 focus:ring-offset-2">
              <span class="absolute inset-0 rounded-md overflow-hidden">
                <img :src="product.image_url || '/placeholder-product.jpg'" alt="" class="w-full h-full object-center object-cover">
              </span>
            </div>
          </div>
        </div>

        <div class="w-full aspect-w-1 aspect-h-1">
          <ProductImage
            :product="product"
            size="xl"
            container-class="w-full h-96 object-center object-cover rounded-lg"
          />
        </div>
      </div>

      <!-- Product info -->
      <div class="mt-10 px-4 sm:px-0 sm:mt-16 lg:mt-0">
        <h1 class="text-2xl font-bold text-gray-900">{{ product.name }}</h1>

        <div class="mt-3">
          <h2 class="sr-only">Product information</h2>
          <p class="text-2xl font-semibold text-gray-900">${{ formatPrice(product.price) }}</p>
        </div>

        <!-- Category -->
        <div class="mt-3">
          <router-link
            :to="`/catalog?category=${product.category}`"
            class="text-sm text-gray-600 hover:text-gray-900 font-medium"
          >
            {{ product.category_name }}
          </router-link>
        </div>

        <!-- Stock Status -->
        <div class="mt-6">
          <div class="flex items-center">
            <div v-if="product.is_in_stock" class="flex items-center">
              <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
              <span class="text-green-600 font-semibold">In Stock</span>
              <span class="text-gray-500 ml-2 text-sm">({{ product.stock_quantity }} available)</span>
            </div>
            <div v-else class="flex items-center">
              <svg class="w-5 h-5 text-red-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
              <span class="text-red-600 font-semibold">Out of Stock</span>
            </div>
          </div>
        </div>

        <div class="mt-6">
          <h3 class="sr-only">Description</h3>
          <div class="text-base text-gray-700 space-y-4">
            <p>{{ product.description }}</p>
          </div>
        </div>

        <form @submit.prevent="handleAddToCart" class="mt-6">
          <!-- Quantity -->
          <div class="mt-8">
            <div class="flex items-center justify-between">
              <h3 class="text-sm font-semibold text-gray-900">Quantity</h3>
            </div>

            <div class="mt-2">
              <div class="flex items-center space-x-3">
                <button
                  type="button"
                  @click="decrementQuantity"
                  :disabled="quantity <= 1"
                  class="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center text-gray-600 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                  </svg>
                </button>
                <input
                  v-model.number="quantity"
                  type="number"
                  min="1"
                  :max="product.stock_quantity"
                  class="w-16 text-center border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
                >
                <button
                  type="button"
                  @click="incrementQuantity"
                  :disabled="quantity >= product.stock_quantity"
                  class="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center text-gray-600 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <div class="mt-8 flex space-x-4">
            <BaseButton
              type="submit"
              variant="primary"
              size="lg"
              class="flex-1 bg-gray-900 text-white hover:bg-gray-800"
              :disabled="!product.is_in_stock"
              :loading="addingToCart"
            >
              <template #icon>
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l-2.5 5m0 0h10.5" />
                </svg>
              </template>
              Add to Cart
            </BaseButton>

            <BaseButton
              variant="outline"
              size="lg"
              @click="toggleWishlist"
              class="border-gray-900 text-gray-900 hover:bg-gray-900 hover:text-white"
            >
              <template #icon>
                <svg class="w-5 h-5" :class="isInWishlist ? 'text-red-500' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </template>
            </BaseButton>
          </div>
        </form>

        <!-- Product details -->
        <section aria-labelledby="details-heading" class="mt-12">
          <h2 id="details-heading" class="text-lg font-semibold text-gray-900">Additional Details</h2>

          <div class="mt-4 space-y-6">
            <div class="border-t border-gray-100 pt-6">
              <dl class="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
                <div>
                  <dt class="text-sm font-semibold text-gray-500">Category</dt>
                  <dd class="mt-1 text-sm text-gray-900">{{ product.category_name }}</dd>
                </div>
                <div>
                  <dt class="text-sm font-semibold text-gray-500">Stock</dt>
                  <dd class="mt-1 text-sm text-gray-900">{{ product.stock_quantity }} units</dd>
                </div>
                <div>
                  <dt class="text-sm font-semibold text-gray-500">Status</dt>
                  <dd class="mt-1 text-sm text-gray-900">{{ product.is_active ? 'Active' : 'Inactive' }}</dd>
                </div>
                <div>
                  <dt class="text-sm font-semibold text-gray-500">Added</dt>
                  <dd class="mt-1 text-sm text-gray-900">{{ formatDate(product.created_at) }}</dd>
                </div>
              </dl>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BaseButton from '../components/common/BaseButton.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import { useProductsStore } from '../store/products.js'
import { useCartStore } from '../store/cart.js'
import { useToast } from '../composables/useToast.js'
import ProductImage from '../components/common/ProductImage.vue'

export default {
  name: 'ProductView',
  components: {
    BaseButton,
    LoadingSpinner,
    ProductImage
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const productsStore = useProductsStore()
    const cartStore = useCartStore()
    const { showSuccess, showError } = useToast()

    // Reactive data
    const loading = ref(false)
    const error = ref('')
    const quantity = ref(1)
    const addingToCart = ref(false)
    const isInWishlist = ref(false)

    // Computed
    const product = computed(() => productsStore.currentProduct)

    // Methods
    const formatPrice = (price) => {
      return parseFloat(price).toFixed(2)
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }

    const handleImageError = (event) => {
      event.target.src = '/placeholder-product.jpg'
    }

    const incrementQuantity = () => {
      if (quantity.value < product.value.stock_quantity) {
        quantity.value++
      }
    }

    const decrementQuantity = () => {
      if (quantity.value > 1) {
        quantity.value--
      }
    }

    const handleAddToCart = async () => {
      if (!product.value.is_in_stock) {
        showError('Product is out of stock')
        return
      }

      try {
        addingToCart.value = true
        const result = await cartStore.addToCart(product.value.id, quantity.value)

        if (result.success) {
          showSuccess(`${quantity.value}x ${product.value.name} added to cart!`)
        } else {
          showError(result.error || 'Failed to add product to cart')
        }
      } catch (error) {
        console.error('Error adding to cart:', error)
        showError('Failed to add product to cart')
      } finally {
        addingToCart.value = false
      }
    }

    const toggleWishlist = () => {
      isInWishlist.value = !isInWishlist.value
      const message = isInWishlist.value
        ? `${product.value.name} added to wishlist!`
        : `${product.value.name} removed from wishlist!`
      showSuccess(message)
    }

    const fetchProduct = async () => {
      try {
        loading.value = true
        error.value = ''

        const productId = route.params.id
        const result = await productsStore.fetchProduct(productId)

        if (!result.success) {
          error.value = result.error || 'Product not found'
        }
      } catch (err) {
        console.error('Error fetching product:', err)
        error.value = 'Failed to load product'
      } finally {
        loading.value = false
      }
    }

    // Lifecycle
    onMounted(() => {
      fetchProduct()
    })

    return {
      // Data
      loading,
      error,
      quantity,
      addingToCart,
      isInWishlist,

      // Computed
      product,

      // Methods
      formatPrice,
      formatDate,
      handleImageError,
      incrementQuantity,
      decrementQuantity,
      handleAddToCart,
      toggleWishlist
    }
  }
}
</script>
