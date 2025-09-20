<template>
  <div class="bg-white h-full rounded-xl shadow-md hover:shadow-xl transition-shadow duration-300 group border border-gray-200">
    <!-- Product Image -->
    <div class="relative overflow-hidden rounded-t-xl">
      <ProductImage
        :product="product"
        size="md"
        container-class="w-full h-48 group-hover:scale-105 transition-transform duration-300"
      />

      <!-- Stock Badge -->
      <div v-if="!product.is_in_stock" class="absolute top-2 left-2">
        <span class="px-2 py-1 bg-red-100 text-red-600 text-xs font-medium rounded-full">
          Out of Stock
        </span>
      </div>

      <!-- Quick Actions -->
      <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-300 flex items-center justify-center opacity-0 group-hover:opacity-100">
        <div class="space-x-2">
          <BaseButton
            variant="secondary"
            size="sm"
            @click="viewProduct"
            class="bg-white text-black hover:bg-gray-100 focus:ring-black"
          >
            <template #icon>
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </template>
          </BaseButton>

          <BaseButton
            variant="primary"
            size="sm"
            :disabled="!product.is_in_stock"
            @click="addToCart"
            class="bg-black text-white hover:bg-gray-800 focus:ring-black"
          >
            <template #icon>
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l-2.5 5m0 0h10.5" />
              </svg>
            </template>
          </BaseButton>
        </div>
      </div>
    </div>

    <!-- Product Info -->
    <div class="p-4">
      <!-- Category -->
      <div class="mb-2">
        <span class="text-sm text-gray-500">{{ product.category_name }}</span>
      </div>

      <!-- Product Name -->
      <h3 class="text-lg font-semibold text-black mb-2 line-clamp-2 group-hover:text-gray-700 transition-colors">
        <router-link :to="`/products/${product.id}`">
          {{ product.name }}
        </router-link>
      </h3>

      <!-- Description -->
      <p class="text-gray-600 text-sm mb-3 line-clamp-2">
        {{ product.description }}
      </p>

      <!-- Price and Stock -->
      <div class="flex items-center justify-between">
        <div>
          <span class="text-xl font-bold text-black">${{ formatPrice(product.price) }}</span>
        </div>
        <div class="text-sm text-gray-500">
          {{ product.stock_quantity }} in stock
        </div>
      </div>
    </div>

    <!-- Card Footer -->
    <div class="p-4 border-t border-gray-200">
      <div class="flex space-x-2">
        <BaseButton
          variant="outline"
          size="sm"
          class="flex-1 border-black text-black hover:bg-gray-100 focus:ring-black"
          @click="viewProduct"
        >
          View Details
        </BaseButton>

        <BaseButton
          variant="primary"
          size="sm"
          class="flex-1 bg-black text-white hover:bg-gray-800 focus:ring-black"
          :disabled="!product.is_in_stock"
          :loading="addingToCart"
          @click="addToCart"
        >
          Add to Cart
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '../common/BaseButton.vue'
import ProductImage from '../common/ProductImage.vue'
import { useToast } from '../../composables/useToast.js'

export default {
  name: 'ProductCard',
  components: {
    BaseButton,
    ProductImage
  },
  props: {
    product: {
      type: Object,
      required: true
    }
  },
  emits: ['add-to-cart'],
  setup(props, { emit }) {
    const router = useRouter()
    const { showToast } = useToast()

    const addingToCart = ref(false)

    const formatPrice = (price) => {
      return parseFloat(price).toFixed(2)
    }

    const viewProduct = () => {
      router.push(`/products/${props.product.id}`)
    }

    const addToCart = async () => {
      if (!props.product.is_in_stock) {
        showToast('Product is out of stock', 'error')
        return
      }

      try {
        addingToCart.value = true

        // Emit event to parent or handle cart logic
        emit('add-to-cart', props.product)

        showToast(`${props.product.name} added to cart!`, 'success')
      } catch (error) {
        showToast('Failed to add product to cart', 'error')
      } finally {
        addingToCart.value = false
      }
    }

    return {
      addingToCart,
      formatPrice,
      viewProduct,
      addToCart
    }
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
