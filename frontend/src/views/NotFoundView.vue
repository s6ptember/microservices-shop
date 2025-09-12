<!-- src/views/NotFoundView.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="text-center">
      <h1 class="text-6xl font-bold text-gray-900 mb-4">404</h1>
      <h2 class="text-2xl font-semibold text-gray-700 mb-4">Page Not Found</h2>
      <p class="text-gray-500 mb-8">The page you're looking for doesn't exist.</p>
      <BaseButton @click="$router.push('/')">Go Home</BaseButton>
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
