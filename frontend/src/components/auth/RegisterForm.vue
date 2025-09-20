<!-- frontend/src/components/auth/RegisterForm.vue -->
<template>
  <div class="bg-white max-w-md mx-auto p-6 rounded-xl shadow-lg border border-gray-200">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-black">Create Account</h2>
      <p class="text-gray-500 mt-2 text-sm">Join MicroShop and start shopping today!</p>
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-5">
      <!-- Email Field -->
      <BaseInput
        v-model="formData.email"
        type="email"
        label="Email Address"
        placeholder="Enter your email"
        :error="errors.email"
        :required="true"
      >
        <template #icon>
          <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 7.89a1 1 0 001.415 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        </template>
      </BaseInput>

      <!-- Username Field -->
      <BaseInput
        v-model="formData.username"
        type="text"
        label="Username"
        placeholder="Choose a username"
        :error="errors.username"
        :required="true"
      >
        <template #icon>
          <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </template>
      </BaseInput>

      <!-- First Name Field -->
      <BaseInput
        v-model="formData.first_name"
        type="text"
        label="First Name"
        placeholder="Enter your first name"
        :error="errors.first_name"
        :required="true"
      >
        <template #icon>
          <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </template>
      </BaseInput>

      <!-- Last Name Field -->
      <BaseInput
        v-model="formData.last_name"
        type="text"
        label="Last Name"
        placeholder="Enter your last name"
        :error="errors.last_name"
        :required="true"
      >
        <template #icon>
          <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </template>
      </BaseInput>

      <!-- Password Field -->
      <BaseInput
        v-model="formData.password"
        :type="showPassword ? 'text' : 'password'"
        label="Password"
        placeholder="Create a password"
        :error="errors.password"
        :required="true"
        help-text="Password must be at least 8 characters long"
      >
        <template #icon>
          <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-4a2 2 0 00-2-2H6a2 2 0 00-2 2v4a2 2 0 002 2zM12 13a2 2 0 100-4 2 2 0 000 4z" />
          </svg>
        </template>
        <template #right>
          <button
            type="button"
            @click="showPassword = !showPassword"
            class="text-gray-400 hover:text-black focus:outline-none"
          >
            <svg v-if="showPassword" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L12 12m-2.122-2.122L4.242 4.242" />
            </svg>
          </button>
        </template>
      </BaseInput>

      <!-- Confirm Password Field -->
      <BaseInput
        v-model="formData.password_confirm"
        :type="showConfirmPassword ? 'text' : 'password'"
        label="Confirm Password"
        placeholder="Confirm your password"
        :error="errors.password_confirm"
        :required="true"
      >
        <template #icon>
          <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-4a2 2 0 00-2-2H6a2 2 0 00-2 2v4a2 2 0 002 2zM12 13a2 2 0 100-4 2 2 0 000 4z" />
          </svg>
        </template>
        <template #right>
          <button
            type="button"
            @click="showConfirmPassword = !showConfirmPassword"
            class="text-gray-400 hover:text-black focus:outline-none"
          >
            <svg v-if="showConfirmPassword" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L12 12m-2.122-2.122L4.242 4.242" />
            </svg>
          </button>
        </template>
      </BaseInput>

      <!-- Terms and Conditions -->
      <div class="flex items-start text-sm">
        <div class="flex items-center h-5">
          <input
            id="terms"
            v-model="formData.agree_terms"
            type="checkbox"
            class="h-4 w-4 text-black focus:ring-black border-gray-300 rounded"
          >
        </div>
        <div class="ml-3">
          <label for="terms" class="text-gray-700">
            I agree to the
            <a href="#" class="text-black hover:text-gray-700 font-medium">Terms and Conditions</a>
            and
            <a href="#" class="text-black hover:text-gray-700 font-medium">Privacy Policy</a>
          </label>
        </div>
      </div>
      <div v-if="errors.agree_terms" class="text-red-600 text-sm">{{ errors.agree_terms }}</div>

      <!-- Error Message -->
      <div v-if="errors.general" class="p-3 bg-red-50 border border-red-200 rounded-md">
        <p class="text-red-600 text-sm">{{ errors.general }}</p>
      </div>

      <!-- Submit Button -->
      <BaseButton
        type="submit"
        variant="primary"
        size="lg"
        :loading="loading"
        :disabled="!isFormValid"
        block
        class="bg-black text-white hover:bg-gray-800 focus:ring-black"
      >
        Create Account
      </BaseButton>

      <!-- Sign In Link -->
      <div class="text-center text-sm">
        <p class="text-gray-600">
          Already have an account?
          <router-link to="/login" class="text-black hover:text-gray-700 font-medium">
            Sign in here
          </router-link>
        </p>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import BaseInput from '../common/BaseInput.vue'
import BaseButton from '../common/BaseButton.vue'
import { useAuthStore } from '../../store/auth'
import { useRouter } from 'vue-router'
import { useToast } from '../../composables/useToast.js'

export default {
  name: 'RegisterForm',
  components: {
    BaseInput,
    BaseButton
  },
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    const { showSuccess, showError } = useToast()

    const formData = ref({
      email: '',
      username: '',
      first_name: '',
      last_name: '',
      password: '',
      password_confirm: '',
      agree_terms: false
    })

    const errors = ref({})
    const loading = ref(false)
    const showPassword = ref(false)
    const showConfirmPassword = ref(false)

    const isFormValid = computed(() => {
      return (
        formData.value.email &&
        formData.value.username &&
        formData.value.first_name &&
        formData.value.last_name &&
        formData.value.password &&
        formData.value.password_confirm &&
        formData.value.agree_terms
      )
    })

    const validateForm = () => {
      errors.value = {}

      // Email validation
      if (!formData.value.email) {
        errors.value.email = 'Email is required'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.value.email)) {
        errors.value.email = 'Please enter a valid email address'
      }

      // Username validation
      if (!formData.value.username) {
        errors.value.username = 'Username is required'
      } else if (formData.value.username.length < 3) {
        errors.value.username = 'Username must be at least 3 characters'
      }

      // First name validation
      if (!formData.value.first_name) {
        errors.value.first_name = 'First name is required'
      }

      // Last name validation
      if (!formData.value.last_name) {
        errors.value.last_name = 'Last name is required'
      }

      // Password validation
      if (!formData.value.password) {
        errors.value.password = 'Password is required'
      } else if (formData.value.password.length < 8) {
        errors.value.password = 'Password must be at least 8 characters'
      }

      // Confirm password validation
      if (!formData.value.password_confirm) {
        errors.value.password_confirm = 'Please confirm your password'
      } else if (formData.value.password !== formData.value.password_confirm) {
        errors.value.password_confirm = 'Passwords do not match'
      }

      // Terms validation
      if (!formData.value.agree_terms) {
        errors.value.agree_terms = 'You must agree to the terms and conditions'
      }

      return Object.keys(errors.value).length === 0
    }

    const handleSubmit = async () => {
      if (!validateForm()) return

      try {
        loading.value = true
        errors.value = {}

        const result = await authStore.register({
          email: formData.value.email,
          username: formData.value.username,
          first_name: formData.value.first_name,
          last_name: formData.value.last_name,
          password: formData.value.password,
          password_confirm: formData.value.password_confirm
        })

        if (result.success) {
          showSuccess('Account created successfully! Please sign in.')
          router.push('/login')
        } else {
          errors.value.general = result.error || 'Registration failed'
        }
      } catch (error) {
        console.error('Registration error:', error)
        errors.value.general = 'An unexpected error occurred'
        showError('Registration failed. Please try again.')
      } finally {
        loading.value = false
      }
    }

    return {
      formData,
      errors,
      loading,
      showPassword,
      showConfirmPassword,
      isFormValid,
      handleSubmit
    }
  }
}
</script>
