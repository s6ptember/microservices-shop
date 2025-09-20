<!-- frontend/src/views/ProfileView.vue -->
<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">My Profile</h1>
      <p class="mt-2 text-sm text-gray-500">Manage your account settings and view your order history</p>
    </div>

    <div class="lg:grid lg:grid-cols-3 lg:gap-8">
      <!-- Navigation Sidebar -->
      <div class="lg:col-span-1">
        <nav class="space-y-1">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'w-full text-left px-4 py-3 rounded-md text-sm font-medium transition-colors',
              activeTab === tab.id
                ? 'bg-gray-900 text-white'
                : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
            ]"
          >
            <div class="flex items-center">
              <component :is="tab.icon" class="w-5 h-5 mr-3" />
              {{ tab.name }}
            </div>
          </button>
        </nav>
      </div>

      <!-- Content Area -->
      <div class="mt-8 lg:mt-0 lg:col-span-2">
        <!-- Profile Information Tab -->
        <div v-if="activeTab === 'profile'" class="space-y-6">
          <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-6">Personal Information</h2>

            <form @submit.prevent="updateProfile" class="space-y-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <BaseInput
                  v-model="profileForm.first_name"
                  label="First Name"
                  :error="profileErrors.first_name"
                  required
                />
                <BaseInput
                  v-model="profileForm.last_name"
                  label="Last Name"
                  :error="profileErrors.last_name"
                  required
                />
              </div>

              <BaseInput
                v-model="profileForm.email"
                type="email"
                label="Email Address"
                :error="profileErrors.email"
                required
                readonly
                help-text="Email cannot be changed"
              />

              <BaseInput
                v-model="profileForm.username"
                label="Username"
                :error="profileErrors.username"
                required
                readonly
                help-text="Username cannot be changed"
              />

              <BaseInput
                v-model="profileForm.phone"
                type="tel"
                label="Phone Number"
                :error="profileErrors.phone"
              />

              <div>
                <label class="block text-sm font-semibold text-gray-900">Address</label>
                <textarea
                  v-model="profileForm.address"
                  rows="3"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-900 focus:ring-gray-900"
                  placeholder="Enter your address"
                ></textarea>
                <p v-if="profileErrors.address" class="mt-1 text-sm text-red-600">{{ profileErrors.address }}</p>
              </div>

              <BaseInput
                v-model="profileForm.date_of_birth"
                type="date"
                label="Date of Birth"
                :error="profileErrors.date_of_birth"
              />

              <div class="flex justify-end">
                <BaseButton
                  type="submit"
                  variant="primary"
                  :loading="updatingProfile"
                  class="bg-gray-900 text-white hover:bg-gray-800"
                >
                  Update Profile
                </BaseButton>
              </div>
            </form>
          </div>
        </div>

        <!-- Order History Tab -->
        <div v-if="activeTab === 'orders'" class="space-y-6">
          <div class="bg-white rounded-lg shadow-sm border border-gray-100">
            <div class="px-6 py-4 border-b border-gray-100">
              <h2 class="text-lg font-semibold text-gray-900">Order History</h2>
            </div>

            <!-- Loading State -->
            <div v-if="loadingOrders" class="p-6 text-center">
              <LoadingSpinner size="md" text="Loading orders..." />
            </div>

            <!-- Empty State -->
            <div v-else-if="orders.length === 0" class="p-6 text-center">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
              </svg>
              <h3 class="mt-4 text-lg font-semibold text-gray-900">No orders yet</h3>
              <p class="mt-2 text-sm text-gray-500">Start shopping to see your orders here.</p>
              <div class="mt-6">
                <BaseButton variant="primary" @click="$router.push('/catalog')" class="bg-gray-900 text-white hover:bg-gray-800">
                  Start Shopping
                </BaseButton>
              </div>
            </div>

            <!-- Orders List -->
            <div v-else class="divide-y divide-gray-100">
              <div
                v-for="order in orders"
                :key="order.id"
                class="p-6 hover:bg-gray-50 transition-colors"
              >
                <div class="flex items-center justify-between mb-4">
                  <div>
                    <h3 class="text-sm font-semibold text-gray-900">
                      Order #{{ order.id }}
                    </h3>
                    <p class="text-sm text-gray-500 mt-1">
                      Placed on {{ formatDate(order.created_at) }}
                    </p>
                  </div>
                  <div class="text-right">
                    <p class="text-sm font-semibold text-gray-900">
                      ${{ formatPrice(order.total_amount) }}
                    </p>
                    <span :class="getStatusClasses(order.status)" class="inline-block px-3 py-1 rounded-full text-sm font-medium">
                      {{ getStatusText(order.status) }}
                    </span>
                  </div>
                </div>

                <div class="space-y-3">
                  <div
                    v-for="item in order.items"
                    :key="item.id"
                    class="flex items-center space-x-4"
                  >
                    <div class="flex-shrink-0">
                      <div class="w-10 h-10 bg-gray-100 rounded-md flex items-center justify-center">
                        <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4-8-4m16 0v10l-8 4-8-4V7" />
                        </svg>
                      </div>
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-semibold text-gray-900 truncate">
                        {{ item.product_name }}
                      </p>
                      <p class="text-sm text-gray-500 mt-1">
                        Qty: {{ item.quantity }} × ${{ formatPrice(item.price) }}
                      </p>
                    </div>
                    <div class="text-sm font-semibold text-gray-900">
                      ${{ formatPrice(item.subtotal) }}
                    </div>
                  </div>
                </div>

                <div class="mt-4 flex justify-end">
                  <BaseButton
                    variant="outline"
                    size="sm"
                    @click="viewOrder(order.id)"
                    class="border-gray-900 text-gray-900 hover:bg-gray-900 hover:text-white"
                  >
                    View Details
                  </BaseButton>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Security Tab -->
        <div v-if="activeTab === 'security'" class="space-y-6">
          <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-6">Change Password</h2>

            <form @submit.prevent="changePassword" class="space-y-6">
              <BaseInput
                v-model="passwordForm.current_password"
                type="password"
                label="Current Password"
                :error="passwordErrors.current_password"
                required
              />

              <BaseInput
                v-model="passwordForm.new_password"
                type="password"
                label="New Password"
                :error="passwordErrors.new_password"
                required
                help-text="Password must be at least 8 characters long"
              />

              <BaseInput
                v-model="passwordForm.confirm_password"
                type="password"
                label="Confirm New Password"
                :error="passwordErrors.confirm_password"
                required
              />

              <div class="flex justify-end">
                <BaseButton
                  type="submit"
                  variant="primary"
                  :loading="changingPassword"
                  class="bg-gray-900 text-white hover:bg-gray-800"
                >
                  Change Password
                </BaseButton>
              </div>
            </form>
          </div>
        </div>

        <!-- Settings Tab -->
        <div v-if="activeTab === 'settings'" class="space-y-6">
          <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-6">Preferences</h2>

            <div class="space-y-6">
              <!-- Email Notifications -->
              <div>
                <h3 class="text-sm font-semibold text-gray-900 mb-3">Email Notifications</h3>
                <div class="space-y-3">
                  <label class="flex items-start">
                    <input
                      v-model="settings.emailNotifications.orders"
                      type="checkbox"
                      class="mt-1 rounded border-gray-300 text-gray-900 focus:ring-gray-900"
                    >
                    <div class="ml-3">
                      <div class="text-sm font-semibold text-gray-900">Order updates</div>
                      <div class="text-sm text-gray-500">Get notified about order status changes</div>
                    </div>
                  </label>

                  <label class="flex items-start">
                    <input
                      v-model="settings.emailNotifications.promotions"
                      type="checkbox"
                      class="mt-1 rounded border-gray-300 text-gray-900 focus:ring-gray-900"
                    >
                    <div class="ml-3">
                      <div class="text-sm font-semibold text-gray-900">Promotions and offers</div>
                      <div class="text-sm text-gray-500">Receive promotional emails and special offers</div>
                    </div>
                  </label>

                  <label class="flex items-start">
                    <input
                      v-model="settings.emailNotifications.newsletter"
                      type="checkbox"
                      class="mt-1 rounded border-gray-300 text-gray-900 focus:ring-gray-900"
                    >
                    <div class="ml-3">
                      <div class="text-sm font-semibold text-gray-900">Newsletter</div>
                      <div class="text-sm text-gray-500">Stay updated with our latest news and products</div>
                    </div>
                  </label>
                </div>
              </div>

              <!-- Privacy Settings -->
              <div>
                <h3 class="text-sm font-semibold text-gray-900 mb-3">Privacy</h3>
                <div class="space-y-3">
                  <label class="flex items-start">
                    <input
                      v-model="settings.privacy.profileVisible"
                      type="checkbox"
                      class="mt-1 rounded border-gray-300 text-gray-900 focus:ring-gray-900"
                    >
                    <div class="ml-3">
                      <div class="text-sm font-semibold text-gray-900">Public profile</div>
                      <div class="text-sm text-gray-500">Make your profile visible to other users</div>
                    </div>
                  </label>

                  <label class="flex items-start">
                    <input
                      v-model="settings.privacy.shareData"
                      type="checkbox"
                      class="mt-1 rounded border-gray-300 text-gray-900 focus:ring-gray-900"
                    >
                    <div class="ml-3">
                      <div class="text-sm font-semibold text-gray-900">Share data for improvements</div>
                      <div class="text-sm text-gray-500">Help us improve our services by sharing usage data</div>
                    </div>
                  </label>
                </div>
              </div>

              <div class="flex justify-end">
                <BaseButton
                  variant="primary"
                  @click="saveSettings"
                  :loading="savingSettings"
                  class="bg-gray-900 text-white hover:bg-gray-800"
                >
                  Save Settings
                </BaseButton>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BaseInput from '../components/common/BaseInput.vue'
import BaseButton from '../components/common/BaseButton.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import { useAuthStore } from '../store/auth.js'
import { useToast } from '../composables/useToast.js'
import orderService from '../services/orders.js'

// Icon components (simplified SVG components)
const UserIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>`
}

const ClipboardIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>`
}

const LockIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-4a2 2 0 00-2-2H6a2 2 0 00-2 2v4a2 2 0 002 2zM12 13a2 2 0 100-4 2 2 0 000 4z"/></svg>`
}

const CogIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>`
}

export default {
  name: 'ProfileView',
  components: {
    BaseInput,
    BaseButton,
    LoadingSpinner,
    UserIcon,
    ClipboardIcon,
    LockIcon,
    CogIcon
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const { showSuccess, showError } = useToast()

    // Reactive data
    const activeTab = ref('profile')
    const updatingProfile = ref(false)
    const changingPassword = ref(false)
    const savingSettings = ref(false)
    const loadingOrders = ref(false)
    const orders = ref([])

    const profileForm = ref({
      first_name: '',
      last_name: '',
      email: '',
      username: '',
      phone: '',
      address: '',
      date_of_birth: ''
    })

    const profileErrors = ref({})

    const passwordForm = ref({
      current_password: '',
      new_password: '',
      confirm_password: ''
    })

    const passwordErrors = ref({})

    const settings = ref({
      emailNotifications: {
        orders: true,
        promotions: false,
        newsletter: false
      },
      privacy: {
        profileVisible: false,
        shareData: true
      }
    })

    // Tab configuration
    const tabs = [
      { id: 'profile', name: 'Profile', icon: 'UserIcon' },
      { id: 'orders', name: 'Order History', icon: 'ClipboardIcon' },
      { id: 'security', name: 'Security', icon: 'LockIcon' },
      { id: 'settings', name: 'Settings', icon: 'CogIcon' }
    ]

    // Computed
    const user = computed(() => authStore.user)

    // Methods
    const formatPrice = (price) => {
      return parseFloat(price).toFixed(2)
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }

    const getStatusClasses = (status) => {
      const classes = 'px-2 py-1 text-xs font-medium rounded-full '

      switch (status) {
        case 'pending':
          return classes + 'bg-yellow-100 text-yellow-800'
        case 'confirmed':
          return classes + 'bg-blue-100 text-blue-800'
        case 'shipped':
          return classes + 'bg-purple-100 text-purple-800'
        case 'delivered':
          return classes + 'bg-green-100 text-green-800'
        case 'cancelled':
          return classes + 'bg-red-100 text-red-800'
        default:
          return classes + 'bg-gray-100 text-gray-800'
      }
    }

    const getStatusText = (status) => {
      const statusMap = {
        pending: 'Pending',
        confirmed: 'Confirmed',
        shipped: 'Shipped',
        delivered: 'Delivered',
        cancelled: 'Cancelled'
      }
      return statusMap[status] || status
    }

    const loadUserProfile = async () => {
      try {
        await authStore.fetchProfile()

        if (user.value) {
          profileForm.value = {
            first_name: user.value.first_name || '',
            last_name: user.value.last_name || '',
            email: user.value.email || '',
            username: user.value.username || '',
            phone: user.value.profile?.phone || '',
            address: user.value.profile?.address || '',
            date_of_birth: user.value.profile?.date_of_birth || ''
          }
        }
      } catch (error) {
        console.error('Error loading profile:', error)
        showError('Failed to load profile data')
      }
    }

    const updateProfile = async () => {
      try {
        updatingProfile.value = true
        profileErrors.value = {}

        // TODO: Implement profile update API call
        // const result = await authStore.updateProfile(profileForm.value)

        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000))

        showSuccess('Profile updated successfully!')
      } catch (error) {
        console.error('Error updating profile:', error)
        showError('Failed to update profile')
      } finally {
        updatingProfile.value = false
      }
    }

    const changePassword = async () => {
      try {
        changingPassword.value = true
        passwordErrors.value = {}

        // Validate passwords match
        if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
          passwordErrors.value.confirm_password = 'Passwords do not match'
          return
        }

        // TODO: Implement password change API call
        // const result = await authStore.changePassword(passwordForm.value)

        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000))

        // Clear form
        passwordForm.value = {
          current_password: '',
          new_password: '',
          confirm_password: ''
        }

        showSuccess('Password changed successfully!')
      } catch (error) {
        console.error('Error changing password:', error)
        showError('Failed to change password')
      } finally {
        changingPassword.value = false
      }
    }

    const saveSettings = async () => {
      try {
        savingSettings.value = true

        // TODO: Implement settings save API call
        // const result = await userService.updateSettings(settings.value)

        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000))

        showSuccess('Settings saved successfully!')
      } catch (error) {
        console.error('Error saving settings:', error)
        showError('Failed to save settings')
      } finally {
        savingSettings.value = false
      }
    }

    const loadOrders = async () => {
      try {
        loadingOrders.value = true

        // TODO: Implement orders API call
        // const response = await orderService.getUserOrders()

        // Simulate API call with mock data
        await new Promise(resolve => setTimeout(resolve, 1000))

        orders.value = [
          {
            id: 1,
            created_at: '2024-01-15T10:30:00Z',
            total_amount: 299.99,
            status: 'delivered',
            items: [
              {
                id: 1,
                product_name: 'iPhone 15',
                quantity: 1,
                price: 299.99,
                subtotal: 299.99
              }
            ]
          },
          {
            id: 2,
            created_at: '2024-01-10T14:20:00Z',
            total_amount: 49.99,
            status: 'shipped',
            items: [
              {
                id: 2,
                product_name: 'Python Programming Book',
                quantity: 1,
                price: 49.99,
                subtotal: 49.99
              }
            ]
          }
        ]
      } catch (error) {
        console.error('Error loading orders:', error)
        showError('Failed to load orders')
      } finally {
        loadingOrders.value = false
      }
    }

    const viewOrder = (orderId) => {
      // TODO: Navigate to order details page
      showSuccess(`Order details for order #${orderId} - Coming soon!`)
    }

    // Lifecycle
    onMounted(async () => {
      await loadUserProfile()

      // Load orders if orders tab is active
      if (activeTab.value === 'orders') {
        await loadOrders()
      }
    })

    // Watch for tab changes
    const watchActiveTab = () => {
      if (activeTab.value === 'orders' && orders.value.length === 0) {
        loadOrders()
      }
    }

    return {
      // Data
      activeTab,
      updatingProfile,
      changingPassword,
      savingSettings,
      loadingOrders,
      orders,
      profileForm,
      profileErrors,
      passwordForm,
      passwordErrors,
      settings,
      tabs,

      // Computed
      user,

      // Methods
      formatPrice,
      formatDate,
      getStatusClasses,
      getStatusText,
      updateProfile,
      changePassword,
      saveSettings,
      viewOrder,
      watchActiveTab
    }
  },

  watch: {
    activeTab: 'watchActiveTab'
  }
}
</script>
