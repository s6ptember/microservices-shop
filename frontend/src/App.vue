<template>
  <div id="app" class="min-h-screen flex flex-col">
    <!-- Header -->
    <AppHeader />

    <!-- Main Content -->
    <main class="flex-1 bg-gray-50">
      <router-view />
    </main>

    <!-- Footer -->
    <AppFooter />

    <!-- Toast Notifications -->
    <Toast v-if="showToast" :message="toastMessage" :type="toastType" @close="hideToast" />
  </div>
</template>

<script>
import AppHeader from './components/layout/AppHeader.vue'
import AppFooter from './components/layout/AppFooter.vue'
import Toast from './components/common/Toast.vue'
import { useToast } from './composables/useToast.js'

export default {
  name: 'App',
  components: {
    AppHeader,
    AppFooter,
    Toast
  },
  setup() {
    const { showToast, toastMessage, toastType, hideToast } = useToast()

    return {
      showToast,
      toastMessage,
      toastType,
      hideToast
    }
  }
}
</script>
