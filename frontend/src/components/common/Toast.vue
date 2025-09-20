<template>
  <transition name="slide-up">
    <div
      v-if="show"
      :class="[
        'fixed bottom-4 right-4 max-w-md w-full bg-white border border-gray-200 rounded-lg shadow-lg z-50',
        type === 'success' ? 'border-green-200' :
        type === 'error' ? 'border-red-200' :
        type === 'warning' ? 'border-yellow-200' :
        'border-blue-200'
      ]"
    >
      <div class="p-4">
        <div class="flex items-start">
          <!-- Icon -->
          <div class="flex-shrink-0">
            <svg v-if="type === 'success'" class="h-6 w-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <svg v-else-if="type === 'error'" class="h-6 w-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <svg v-else-if="type === 'warning'" class="h-6 w-6 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
            <svg v-else class="h-6 w-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>

          <!-- Content -->
          <div class="ml-3 w-0 flex-1">
            <p class="text-sm font-medium text-black">
              {{ message }}
            </p>
          </div>

          <!-- Close Button -->
          <div class="ml-4 flex-shrink-0 flex">
            <button
              @click="handleClose"
              class="inline-flex text-gray-400 hover:text-black focus:outline-none focus:ring-2 focus:ring-black focus:ring-offset-2 rounded-md"
            >
              <span class="sr-only">Close</span>
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Progress Bar -->
      <div v-if="showProgressBar" class="h-1 bg-gray-100 rounded-b-lg overflow-hidden">
        <div
          :class="[
            'h-full transition-all duration-100 ease-linear',
            type === 'success' ? 'bg-green-500' :
            type === 'error' ? 'bg-red-500' :
            type === 'warning' ? 'bg-yellow-500' :
            'bg-blue-500'
          ]"
          :style="{ width: `${progressWidth}%` }"
        ></div>
      </div>
    </div>
  </transition>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'

export default {
  name: 'Toast',
  props: {
    message: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: 'info',
      validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
    },
    duration: {
      type: Number,
      default: 5000
    },
    showProgressBar: {
      type: Boolean,
      default: true
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const show = ref(true)
    const progressWidth = ref(100)
    let timer = null
    let progressTimer = null

    const toastClasses = computed(() => {
      const borderColors = {
        success: 'border-l-4 border-l-green-500',
        error: 'border-l-4 border-l-red-500',
        warning: 'border-l-4 border-l-yellow-500',
        info: 'border-l-4 border-l-blue-500'
      }

      return borderColors[props.type] || borderColors.info
    })

    const progressBarClasses = computed(() => {
      const colors = {
        success: 'bg-green-500',
        error: 'bg-red-500',
        warning: 'bg-yellow-500',
        info: 'bg-blue-500'
      }

      return colors[props.type] || colors.info
    })

    const handleClose = () => {
      show.value = false
      clearTimers()
      emit('close')
    }

    const clearTimers = () => {
      if (timer) clearTimeout(timer)
      if (progressTimer) clearInterval(progressTimer)
    }

    const startTimer = () => {
      if (props.duration > 0) {
        // Auto close timer
        timer = setTimeout(handleClose, props.duration)

        // Progress bar timer
        if (props.showProgressBar) {
          const interval = 100
          const steps = props.duration / interval
          const decrement = 100 / steps

          progressTimer = setInterval(() => {
            progressWidth.value -= decrement
            if (progressWidth.value <= 0) {
              progressWidth.value = 0
              clearInterval(progressTimer)
            }
          }, interval)
        }
      }
    }

    onMounted(() => {
      startTimer()
    })

    onUnmounted(() => {
      clearTimers()
    })

    return {
      show,
      progressWidth,
      toastClasses,
      progressBarClasses,
      handleClose
    }
  }
}
</script>
