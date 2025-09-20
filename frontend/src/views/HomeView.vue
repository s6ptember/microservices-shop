<!-- frontend/src/views/HomeView.vue -->
<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section class="bg-white text-gray-900 py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-5xl md:text-6xl font-extrabold text-gray-900 mb-6">
            Welcome to MicroShop
          </h1>
          <p class="text-xl md:text-2xl mb-8 text-gray-600 max-w-3xl mx-auto">
            Discover amazing products with our modern microservices-powered shopping experience.
            Fast, secure, and reliable.
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <BaseButton
              variant="primary"
              size="lg"
              @click="$router.push('/catalog')"
            >
              Shop Now
            </BaseButton>
            <BaseButton
              variant="outline"
              size="lg"
              @click="$router.push('/register')"
            >
              Create Account
            </BaseButton>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-extrabold text-gray-900 mb-4">Why Choose MicroShop?</h2>
          <p class="text-gray-600 text-lg max-w-2xl mx-auto">
            Built with modern microservices architecture for the best shopping experience
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="text-center">
            <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="h-8 w-8 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">Lightning Fast</h3>
            <p class="text-gray-600">Optimized performance with microservices architecture for instant loading</p>
          </div>

          <div class="text-center">
            <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="h-8 w-8 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">Secure & Reliable</h3>
            <p class="text-gray-600">Enterprise-grade security with reliable distributed systems</p>
          </div>

          <div class="text-center">
            <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="h-8 w-8 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">User Friendly</h3>
            <p class="text-gray-600">Intuitive design and smooth user experience across all devices</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Products Section -->
    <section class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between mb-12">
          <div>
            <h2 class="text-4xl font-extrabold text-gray-900 mb-3">Featured Products</h2>
            <p class="text-gray-600 text-lg">Discover our most popular items</p>
          </div>
          <BaseButton
            variant="outline"
            @click="$router.push('/catalog')"
          >
            View All Products
          </BaseButton>
        </div>

        <!-- Loading State -->
        <div v-if="productsLoading" class="flex justify-center py-16">
          <LoadingSpinner size="lg" text="Loading products..." />
        </div>

        <!-- Products Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <ProductCard
            v-for="product in featuredProducts"
            :key="product.id"
            :product="product"
            @add-to-cart="handleAddToCart"
          />
        </div>

        <!-- Empty State -->
        <div v-if="!productsLoading && featuredProducts.length === 0" class="text-center py-16 bg-white rounded-xl shadow-sm">
          <p class="text-gray-600 text-lg">No featured products available at the moment.</p>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-16 bg-gray-50 text-gray-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-4xl font-extrabold text-gray-900 mb-4">Ready to Start Shopping?</h2>
        <p class="text-gray-600 text-lg mb-8 max-w-2xl mx-auto">
          Join thousands of satisfied customers who trust MicroShop for their online shopping needs.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <BaseButton
            variant="primary"
            size="lg"
            @click="$router.push('/register')"
          >
            Create Free Account
          </BaseButton>
          <BaseButton
            variant="outline"
            size="lg"
            @click="$router.push('/catalog')"
          >
            Browse Products
          </BaseButton>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '../components/common/BaseButton.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import ProductCard from '../components/product/ProductCard.vue'
import { useProductsStore } from '../store/products.js'
import { useCartStore } from '../store/cart.js'
import { useAuthStore } from '../store/auth.js'
import { useToast } from '../composables/useToast.js'

export default {
  name: 'HomeView',
  components: {
    BaseButton,
    LoadingSpinner,
    ProductCard
  },
  setup() {
    const router = useRouter()
    const { showToast } = useToast()
    const productsStore = useProductsStore()
    const cartStore = useCartStore()
    const authStore = useAuthStore()

    const featuredProducts = ref([])
    const productsLoading = ref(false)

    const fetchFeaturedProducts = async () => {
      try {
        productsLoading.value = true
        const result = await productsStore.fetchProducts({
          page_size: 8,
          ordering: '-created_at'
        })

        if (result.success) {
          featuredProducts.value = productsStore.products.slice(0, 4)
        }
      } catch (error) {
        console.error('Error fetching featured products:', error)
        showToast('Failed to load featured products', 'error')
      } finally {
        productsLoading.value = false
      }
    }

    const handleAddToCart = async (product) => {
      try {
        if (!authStore.isAuthenticated) {
          showToast('Please sign in to add items to cart', 'error')
          router.push('/login')
          return
        }

        const result = await cartStore.addToCart(product.id, 1)
        if (result.success) {
          showToast(`${product.name} added to cart!`, 'success')
        } else {
          showToast(result.error || 'Failed to add product to cart', 'error')
        }
      } catch (error) {
        console.error('Error adding to cart:', error)
        showToast('Failed to add product to cart', 'error')
      }
    }

    onMounted(() => {
      fetchFeaturedProducts()
    })

    return {
      featuredProducts,
      productsLoading,
      handleAddToCart
    }
  }
}
</script>
