<!-- frontend/src/views/RegisterView.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full bg-white rounded-lg shadow-sm border border-gray-100 p-6">
      <RegisterForm />
    </div>
</div>
</template>

<script>
import RegisterForm from '../components/auth/RegisterForm.vue'

export default {
  name: 'RegisterView',
  components: {
    RegisterForm
  }
}
</script>
