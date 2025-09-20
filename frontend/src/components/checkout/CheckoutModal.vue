<!-- frontend/src/components/checkout/CheckoutModal.vue -->
<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl shadow-2xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
        <h2 class="text-2xl font-bold text-black">Checkout</h2>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-black transition-colors"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Content -->
      <div class="p-6">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Personal Information -->
          <div>
            <h3 class="text-lg font-medium text-black mb-4">Personal Information</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <BaseInput
                v-model="formData.firstName"
                label="First Name"
                :error="errors.firstName"
                required
                class="focus:ring-black"
              />
              <BaseInput
                v-model="formData.lastName"
                label="Last Name"
                :error="errors.lastName"
                required
                class="focus:ring-black"
              />
            </div>
            <div class="mt-4">
              <BaseInput
                v-model="formData.email"
                type="email"
                label="Email Address"
                :error="errors.email"
                required
                class="focus:ring-black"
              />
            </div>
            <div class="mt-4">
              <BaseInput
                v-model="formData.phone"
                type="tel"
                label="Phone Number"
                :error="errors.phone"
                required
                class="focus:ring-black"
              />
            </div>
          </div>

          <!-- Shipping Address -->
          <div>
            <h3 class="text-lg font-medium text-black mb-4">Shipping Address</h3>
            <div class="space-y-4">
              <BaseInput
                v-model="formData.address"
                label="Street Address"
                :error="errors.address"
                required
                class="focus:ring-black"
              />
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <BaseInput
                  v-model="formData.city"
                  label="City"
                  :error="errors.city"
                  required
                  class="focus:ring-black"
                />
                <BaseInput
                  v-model="formData.state"
                  label="State"
                  :error="errors.state"
                  required
                  class="focus:ring-black"
                />
                <BaseInput
                  v-model="formData.zipCode"
                  label="ZIP Code"
                  :error="errors.zipCode"
                  required
                  class="focus:ring-black"
                />
              </div>
            </div>
          </div>

          <!-- Order Summary -->
          <div class="border-t border-gray-200 pt-6">
            <h3 class="text-lg font-medium text-black mb-4">Order Summary</h3>

            <!-- Cart Items -->
            <div class="bg-gray-50 rounded-md p-4 mb-4">
              <div class="space-y-3">
                <div
                  v-for="item in cartItems"
                  :key="item.id"
                  class="flex items-center justify-between"
                >
                  <div class="flex items-center space-x-3">
                    <ProductImage
                      :product="getProductForItem(item)"
                      size="sm"
                      container-class="w-12 h-12 rounded"
                    />
                    <div>
                      <p class="text-sm font-medium text-black">{{ item.product_name }}</p>
                      <p class="text-xs text-gray-500">Qty: {{ item.quantity }}</p>
                    </div>
                  </div>
                  <p class="text-sm font-medium text-black">
                    ${{ formatPrice(item.subtotal) }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Totals -->
            <div class="space-y-2">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Subtotal</span>
                <span class="text-black">${{ formatPrice(subtotal) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Shipping</span>
                <span class="text-black">Free</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Tax</span>
                <span class="text-black">${{ formatPrice(tax) }}</span>
              </div>
              <div class="border-t border-gray-200 pt-2 flex justify-between text-base font-medium">
                <span class="text-black">Total</span>
                <span class="text-black">${{ formatPrice(totalAmount) }}</span>
              </div>
            </div>
          </div>

          <!-- Payment Note -->
          <div class="bg-blue-50 border border-blue-200 rounded-md p-4">
            <div class="flex items-start">
              <svg class="w-5 h-5 text-blue-400 mt-0.5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
              </svg>
              <div>
                <h4 class="text-sm font-medium text-blue-900">Payment Information</h4>
                <p class="text-sm text-blue-700 mt-1">
                  This is a demo checkout. No actual payment will be processed.
                  Your order will be placed for demonstration purposes only.
                </p>
              </div>
            </div>
          </div>

          <!-- Special Instructions -->
          <div>
            <label class="block text-sm font-medium text-black mb-2">
              Special Instructions (Optional)
            </label>
            <textarea
              v-model="formData.instructions"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent"
              placeholder="Any special delivery instructions..."
            ></textarea>
          </div>

          <!-- Error Message -->
          <div v-if="errors.general" class="p-3 bg-red-50 border border-red-200 rounded-md">
            <p class="text-red-600 text-sm">{{ errors.general }}</p>
          </div>

          <!-- Actions -->
          <div class="flex space-x-4 pt-6">
            <BaseButton
              variant="outline"
              @click="$emit('close')"
              class="flex-1 border-black text-black hover:bg-gray-100 focus:ring-black"
            >
              Cancel
            </BaseButton>
            <BaseButton
              type="submit"
              variant="primary"
              :loading="submitting"
              class="flex-1 bg-black text-white hover:bg-gray-800 focus:ring-black"
            >
              Place Order
            </BaseButton>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import BaseInput from '../common/BaseInput.vue'
import BaseButton from '../common/BaseButton.vue'
import ProductImage from '../common/ProductImage.vue'
import { useAuthStore } from '../../store/auth'
import { useToast } from '../../composables/useToast'
import orderService from '../../services/orders'

export default {
  name: 'CheckoutModal',
  components: {
    BaseInput,
    BaseButton,
    ProductImage
  },
  props: {
    cartItems: {
      type: Array,
      required: true
    },
    totalAmount: {
      type: Number,
      required: true
    }
  },
  emits: ['close', 'order-placed'],
  setup(props, { emit }) {
    const authStore = useAuthStore()
    const { showError } = useToast()

    const formData = ref({
      firstName: '',
      lastName: '',
      email: '',
      phone: '',
      address: '',
      city: '',
      state: '',
      zipCode: '',
      instructions: ''
    })

    const errors = ref({})
    const submitting = ref(false)

    // Computed
    const subtotal = computed(() => props.totalAmount / 1.1) // Remove tax to get subtotal
    const tax = computed(() => subtotal.value * 0.1)

    const formatPrice = (price) => {
      return parseFloat(price).toFixed(2)
    }

    const getProductForItem = (item) => {
      return {
        id: item.product_id,
        name: item.product_name,
        category_name: item.product_info?.category_name || 'Product',
        image_url: item.product_info?.image_url || null
      }
    }

    // Validation
    const validateForm = () => {
      errors.value = {}

      if (!formData.value.firstName.trim()) {
        errors.value.firstName = 'First name is required'
      }

      if (!formData.value.lastName.trim()) {
        errors.value.lastName = 'Last name is required'
      }

      if (!formData.value.email.trim()) {
        errors.value.email = 'Email is required'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.value.email)) {
        errors.value.email = 'Please enter a valid email address'
      }

      if (!formData.value.phone.trim()) {
        errors.value.phone = 'Phone number is required'
      }

      if (!formData.value.address.trim()) {
        errors.value.address = 'Street address is required'
      }

      if (!formData.value.city.trim()) {
        errors.value.city = 'City is required'
      }

      if (!formData.value.state.trim()) {
        errors.value.state = 'State is required'
      }

      if (!formData.value.zipCode.trim()) {
        errors.value.zipCode = 'ZIP code is required'
      }

      return Object.keys(errors.value).length === 0
    }

    // Form submission
    const handleSubmit = async () => {
      if (!validateForm()) {
        return
      }

      try {
        submitting.value = true
        errors.value = {}

        // Prepare shipping address
        const shippingAddress = `${formData.value.address}, ${formData.value.city}, ${formData.value.state} ${formData.value.zipCode}`

        // Create order
        const response = await orderService.createOrder({
          shipping_address: shippingAddress,
          customer_info: {
            first_name: formData.value.firstName,
            last_name: formData.value.lastName,
            email: formData.value.email,
            phone: formData.value.phone
          },
          special_instructions: formData.value.instructions
        })

        if (response.data) {
          emit('order-placed', response.data)
        } else {
          throw new Error('Failed to create order')
        }

      } catch (error) {
        console.error('Order creation error:', error)
        errors.value.general = error.response?.data?.error || 'Failed to place order. Please try again.'
        showError(errors.value.general)
      } finally {
        submitting.value = false
      }
    }

    // Load user data
    onMounted(() => {
      if (authStore.user) {
        formData.value.firstName = authStore.user.first_name || ''
        formData.value.lastName = authStore.user.last_name || ''
        formData.value.email = authStore.user.email || ''

        // Load profile data if available
        if (authStore.user.profile) {
          formData.value.phone = authStore.user.profile.phone || ''
          // Parse address if stored as single string
          const address = authStore.user.profile.address || ''
          if (address) {
            formData.value.address = address
          }
        }
      }
    })

    return {
      // Data
      formData,
      errors,
      submitting,

      // Computed
      subtotal,
      tax,

      // Methods
      formatPrice,
      getProductForItem,
      validateForm,
      handleSubmit
    }
  }
}
</script>
