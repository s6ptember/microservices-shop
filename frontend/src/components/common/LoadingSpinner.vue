<template>
  <div :class="containerClasses">
    <div :class="spinnerClasses"></div>
    <p v-if="text" :class="textClasses">{{ text }}</p>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'LoadingSpinner',
  props: {
    size: {
      type: String,
      default: 'md',
      validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value)
    },
    text: {
      type: String,
      default: ''
    },
    color: {
      type: String,
      default: 'gray',
      validator: (value) => ['gray', 'blue', 'green', 'red', 'yellow', 'purple'].includes(value)
    },
    overlay: {
      type: Boolean,
      default: false
    },
    center: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const containerClasses = computed(() => {
      const baseClasses = 'flex items-center'
      const directionClass = props.text ? 'flex-col space-y-2' : 'justify-center'
      const centerClass = props.center ? 'justify-center' : ''
      const overlayClass = props.overlay
        ? 'fixed inset-0 bg-white bg-opacity-75 z-50 flex items-center justify-center'
        : ''

      return [
        baseClasses,
        directionClass,
        centerClass,
        overlayClass
      ].filter(Boolean).join(' ')
    })

    const spinnerClasses = computed(() => {
      const sizes = {
        sm: 'w-4 h-4 border-2',
        md: 'w-6 h-6 border-2',
        lg: 'w-8 h-8 border-3',
        xl: 'w-12 h-12 border-4'
      }

      const colors = {
        gray: 'border-gray-200 border-t-gray-900',
        blue: 'border-blue-200 border-t-blue-600',
        green: 'border-green-200 border-t-green-600',
        red: 'border-red-200 border-t-red-600',
        yellow: 'border-yellow-200 border-t-yellow-600',
        purple: 'border-purple-200 border-t-purple-600'
      }

      return [
        'animate-spin rounded-full',
        sizes[props.size],
        colors[props.color]
      ].join(' ')
    })

    const textClasses = computed(() => {
      const sizes = {
        sm: 'text-sm',
        md: 'text-base',
        lg: 'text-lg',
        xl: 'text-xl'
      }

      return [
        'text-gray-600 font-medium',
        sizes[props.size]
      ].join(' ')
    })

    return {
      containerClasses,
      spinnerClasses,
      textClasses
    }
  }
}
</script>
