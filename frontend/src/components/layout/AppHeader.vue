<!-- frontend/src/components/layout/AppHeader.vue -->
<template>
  <header class="bg-white border-b border-gray-200 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <div class="flex items-center">
          <router-link to="/" class="flex items-center space-x-2">
            <div class="w-8 h-8 bg-black rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-sm">MS</span>
            </div>
            <span class="text-xl font-bold text-black">MicroShop</span>
          </router-link>
        </div>

        <!-- Navigation -->
        <nav class="hidden md:flex items-center space-x-8">
          <router-link
            to="/"
            class="text-gray-600 hover:text-black px-3 py-2 rounded-md text-sm font-medium transition-colors"
            :class="{ 'text-black font-semibold': $route.name === 'home' }"
          >
            Home
          </router-link>
          <router-link
            to="/catalog"
            class="text-gray-600 hover:text-black px-3 py-2 rounded-md text-sm font-medium transition-colors"
            :class="{ 'text-black font-semibold': $route.name === 'catalog' }"
          >
            Catalog
          </router-link>
        </nav>

        <!-- Search Bar -->
        <div class="flex-1 max-w-lg mx-8 hidden md:block">
          <div class="relative">
            <input
              type="text"
              v-model="searchQuery"
              @keyup.enter="handleSearch"
              placeholder="Search products..."
              class="w-full px-4 py-2 pl-10 pr-4 text-gray-700 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:bg-white focus:border-black focus:ring-2 focus:ring-black transition-all duration-200"
            >
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Right Side Actions -->
        <div class="flex items-center space-x-4">
          <!-- Debug Info (only in development) -->
          <div v-if="isDev" class="text-xs text-gray-500">
            Auth: {{ isAuthenticated ? 'Yes' : 'No' }} | Token: {{ hasToken ? 'Yes' : 'No' }}
          </div>

          <!-- Cart Icon -->
          <router-link
            to="/cart"
            class="relative p-2 text-gray-600 hover:text-black transition-colors group"
          >
            <svg class="h-6 w-6 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l-2.5 5m0 0h10.5" />
            </svg>
            <span
              v-if="cartItemsCount > 0"
              class="absolute -top-1 -right-1 bg-black text-white text-xs rounded-full h-5 w-5 flex items-center justify-center animate-pulse"
            >
              {{ cartItemsCount > 99 ? '99+' : cartItemsCount }}
            </span>
          </router-link>

          <!-- User Menu -->
          <div v-if="isAuthenticated" class="relative" ref="userMenu">
            <button
              @click="showUserMenu = !showUserMenu"
              class="flex items-center space-x-2 p-2 text-gray-600 hover:text-black focus:outline-none transition-colors"
            >
              <div class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                <svg class="h-5 w-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <span class="hidden sm:block text-sm font-medium">{{ userName }}</span>
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <!-- User Dropdown -->
            <transition name="fade">
              <div v-if="showUserMenu" class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1">
                <router-link
                  to="/profile"
                  class="block px-4 py-2 text-sm text-gray-600 hover:bg-gray-100 hover:text-black transition-colors"
                  @click="showUserMenu = false"
                >
                  <div class="flex items-center">
                    <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    Profile
                  </div>
                </router-link>
                <router-link
                  to="/cart"
                  class="block px-4 py-2 text-sm text-gray-600 hover:bg-gray-100 hover:text-black transition-colors"
                  @click="showUserMenu = false"
                >
                  <div class="flex items-center">
                    <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l-2.5 5m0 0h10.5" />
                    </svg>
                    My Cart
                    <span v-if="cartItemsCount > 0" class="ml-auto bg-black text-white text-xs rounded-full px-2 py-1">
                      {{ cartItemsCount }}
                    </span>
                  </div>
                </router-link>
                <router-link
                  to="/orders"
                  class="block px-4 py-2 text-sm text-gray-600 hover:bg-gray-100 hover:text-black transition-colors"
                  @click="showUserMenu = false"
                >
                  <div class="flex items-center">
                    <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                    </svg>
                    My Orders
                  </div>
                </router-link>
                <div class="border-t border-gray-100 my-1"></div>
                <button
                  @click="handleLogout"
                  class="block w-full text-left px-4 py-2 text-sm text-gray-600 hover:bg-gray-100 hover:text-black transition-colors"
                >
                  <div class="flex items-center">
                    <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    Sign out
                  </div>
                </button>
              </div>
            </transition>
          </div>

          <!-- Login/Register Buttons -->
          <div v-else class="flex items-center space-x-2">
            <router-link
              to="/login"
              class="px-4 py-2 text-sm font-medium text-gray-600 hover:text-black transition-colors"
            >
              Sign in
            </router-link>
            <router-link
              to="/register"
              class="px-4 py-2 text-sm font-medium bg-black text-white rounded-md hover:bg-gray-800 transition-colors"
            >
              Sign up
            </router-link>
          </div>

          <!-- Mobile menu button -->
          <button
            @click="showMobileMenu = !showMobileMenu"
            class="md:hidden p-2 text-gray-600 hover:text-black focus:outline-none transition-colors"
          >
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!showMobileMenu" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile Menu -->
      <transition name="slide-up">
        <div v-if="showMobileMenu" class="md:hidden py-4 border-t border-gray-200">
          <div class="space-y-1">
            <router-link
              to="/"
              class="block px-3 py-2 text-base font-medium text-gray-600 hover:text-black hover:bg-gray-100 rounded-md transition-colors"
              @click="showMobileMenu = false"
            >
              Home
            </router-link>
            <router-link
              to="/catalog"
              class="block px-3 py-2 text-base font-medium text-gray-600 hover:text-black hover:bg-gray-100 rounded-md transition-colors"
              @click="showMobileMenu = false"
            >
              Catalog
            </router-link>

            <!-- Mobile Search -->
            <div class="px-3 py-2">
              <input
                type="text"
                v-model="searchQuery"
                @keyup.enter="handleSearch"
                placeholder="Search products..."
                class="w-full px-4 py-2 text-gray-700 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:bg-white focus:border-black focus:ring-2 focus:ring-black transition-all duration-200"
              >
            </div>

            <!-- Mobile Cart Link -->
            <router-link
              to="/cart"
              class="flex items-center justify-between px-3 py-2 text-base font-medium text-gray-600 hover:text-black hover:bg-gray-100 rounded-md transition-colors"
              @click="showMobileMenu = false"
            >
              <span>Shopping Cart</span>
              <span v-if="cartItemsCount > 0" class="bg-black text-white text-xs rounded-full px-2 py-1">
                {{ cartItemsCount }}
              </span>
            </router-link>

            <!-- Mobile Auth Links -->
            <div v-if="!isAuthenticated" class="border-t border-gray-200 pt-4 mt-4">
              <router-link
                to="/login"
                class="block px-3 py-2 text-base font-medium text-gray-600 hover:text-black hover:bg-gray-100 rounded-md transition-colors"
                @click="showMobileMenu = false"
              >
                Sign in
              </router-link>
              <router-link
                to="/register"
                class="block px-3 py-2 text-base font-medium text-gray-600 hover:text-black hover:bg-gray-100 rounded-md transition-colors"
                @click="showMobileMenu = false"
              >
                Create account
              </router-link>
            </div>

            <!-- Mobile User Menu -->
            <div v-else class="border-t border-gray-200 pt-4 mt-4">
              <router-link
                to="/profile"
                class="block px-3 py-2 text-base font-medium text-gray-600 hover:text-black hover:bg-gray-100 rounded-md transition-colors"
                @click="showMobileMenu = false"
              >
                Profile
              </router-link>
              <button
                @click="handleLogout"
                class="block w-full text-left px-3 py-2 text-base font-medium text-gray-600 hover:text-black hover:bg-gray-100 rounded-md transition-colors"
              >
                Sign out
              </button>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </header>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'
import { useCartStore } from '../../store/cart'

export default {
  name: 'AppHeader',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const cartStore = useCartStore()

    const searchQuery = ref('')
    const showUserMenu = ref(false)
    const showMobileMenu = ref(false)
    const userMenu = ref(null)

    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const userName = computed(() => authStore.userName)
    const cartItemsCount = computed(() => cartStore.totalItems)
    const hasToken = computed(() => !!authStore.token)
    const isDev = computed(() => import.meta.env.DEV)

    const handleSearch = () => {
      if (searchQuery.value.trim()) {
        router.push({
          name: 'catalog',
          query: { search: searchQuery.value.trim() }
        })
        showMobileMenu.value = false
        searchQuery.value = ''
      }
    }

    const handleLogout = async () => {
      await authStore.logout()
      await cartStore.reset() // Clear cart on logout
      showUserMenu.value = false
      showMobileMenu.value = false
      router.push('/')
    }

    // Close user menu when clicking outside
    const handleClickOutside = (event) => {
      if (userMenu.value && !userMenu.value.contains(event.target)) {
        showUserMenu.value = false
      }
    }

    onMounted(async () => {
      document.addEventListener('click', handleClickOutside)

      // Initialize auth state
      console.log('Initializing auth state in header...')
      await authStore.initialize()

      // Fetch cart if user is authenticated
      if (authStore.isAuthenticated) {
        console.log('User authenticated, fetching cart...')
        await cartStore.fetchCart()
      } else {
        console.log('User not authenticated, skipping cart fetch')
      }
    })

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
    })

    return {
      // Data
      searchQuery,
      showUserMenu,
      showMobileMenu,
      userMenu,

      // Computed
      isAuthenticated,
      userName,
      cartItemsCount,
      hasToken,
      isDev,

      // Methods
      handleSearch,
      handleLogout
    }
  }
}
</script>
