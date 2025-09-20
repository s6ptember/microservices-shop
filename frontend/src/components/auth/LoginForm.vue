<template>
  <div class="bg-white max-w-md mx-auto p-6 rounded-xl shadow-lg border border-gray-200">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-black">Sign In</h2>
      <p class="text-gray-500 mt-2 text-sm">Welcome back! Please sign in to your account.</p>
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

      <!-- Password Field -->
      <BaseInput
        v-model="formData.password"
        :type="showPassword ? 'text' : 'password'"
        label="Password"
        placeholder="Enter your password"
        :error="errors.password"
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

      <!-- Remember Me & Forgot Password -->
      <div class="flex items-center justify-between text-sm">
        <label class="flex items-center">
          <input
            v-model="formData.remember"
            type="checkbox"
            class="h-4 w-4 text-black focus:ring-black border-gray-300 rounded"
          >
          <span class="ml-2 text-gray-600">Remember me</span>
        </label>

        <a href="#" class="text-black hover:text-gray-700 font-medium">
          Forgot password?
        </a>
      </div>

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
        Sign In
      </BaseButton>

      <!-- Sign Up Link -->
      <div class="text-center text-sm">
        <p class="text-gray-600">
          Don't have an account?
          <router-link to="/register" class="text-black hover:text-gray-700 font-medium">
            Sign up here
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

export default {
  name: 'LoginForm',
  components: {
    BaseInput,
    BaseButton
  },
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()

    const formData = ref({
      email: '',
      password: '',
      remember: false
    })

    const errors = ref({})
    const loading = ref(false)
    const showPassword = ref(false)

    const isFormValid = computed(() => {
      return formData.value.email && formData.value.password
    })

    const validateForm = () => {
      errors.value = {}

      if (!formData.value.email) {
        errors.value.email = 'Email is required'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.value.email)) {
        errors.value.email = 'Please enter a valid email address'
      }

      if (!formData.value.password) {
        errors.value.password = 'Password is required'
      } else if (formData.value.password.length < 6) {
        errors.value.password = 'Password must be at least 6 characters'
      }

      return Object.keys(errors.value).length === 0
    }

    const handleSubmit = async () => {
      if (!validateForm()) return

      try {
        loading.value = true
        errors.value = {}

        const result = await authStore.login({
          email: formData.value.email,
          password: formData.value.password
        })

        if (result.success) {
          // Redirect to intended page or home
          const redirect = router.currentRoute.value.query.redirect || '/'
          router.push(redirect)
        } else {
          errors.value.general = result.error || 'Login failed'
        }
      } catch (error) {
        errors.value.general = 'An unexpected error occurred'
      } finally {
        loading.value = false
      }
    }

    return {
      formData,
      errors,
      loading,
      showPassword,
      isFormValid,
      handleSubmit
    }
  }
}
</script>
