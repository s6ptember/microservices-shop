<!-- src/views/NotFoundView.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="text-center bg-white rounded-xl shadow-sm p-8 border border-gray-100">
      <h1 class="text-7xl font-extrabold text-gray-900 mb-4">404</h1>
      <h2 class="text-3xl font-semibold text-gray-900 mb-4">Page Not Found</h2>
      <p class="text-gray-600 text-lg mb-8">The page you're looking for doesn't exist.</p>
      <BaseButton variant="primary" @click="$router.push('/')">Go Home</BaseButton>
    </div>
  </div>
</template>

<script>
import BaseButton from '../components/common/BaseButton.vue'

export default {
  name: 'NotFoundView',
  components: {
    BaseButton
  }
}
</script>
