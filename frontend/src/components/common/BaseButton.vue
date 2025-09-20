<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="[
      'inline-flex items-center justify-center px-4 py-2 rounded-md font-medium transition-all duration-200',
      disabled || loading ? 'opacity-50 cursor-not-allowed' : 'hover:shadow-md',
      variant === 'primary' ? 'bg-black text-white hover:bg-gray-800 focus:ring-2 focus:ring-black focus:ring-offset-2' :
      variant === 'secondary' ? 'bg-white text-black border border-black hover:bg-gray-100 focus:ring-2 focus:ring-black focus:ring-offset-2' :
      variant === 'outline' ? 'border border-black text-black hover:bg-gray-100 focus:ring-2 focus:ring-black focus:ring-offset-2' :
      'bg-gray-200 text-black hover:bg-gray-300 focus:ring-2 focus:ring-black focus:ring-offset-2',
      size === 'sm' ? 'text-sm px-3 py-1' : size === 'lg' ? 'text-base px-6 py-3' : 'text-base px-4 py-2',
      block ? 'w-full' : ''
    ]"
    @click="handleClick"
  >
    <div class="flex items-center justify-center space-x-2">
      <div v-if="loading" class="animate-spin h-5 w-5 border-2 border-t-black rounded-full"></div>
      <slot v-else name="icon" />
      <span v-if="$slots.default || text">{{ text }}</span>
      <slot />
    </div>
  </button>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'BaseButton',
  props: {
    variant: {
      type: String,
      default: 'primary',
      validator: (value) => ['primary', 'secondary', 'outline', 'ghost', 'danger'].includes(value)
    },
    size: {
      type: String,
      default: 'md',
      validator: (value) => ['sm', 'md', 'lg'].includes(value)
    },
    type: {
      type: String,
      default: 'button'
    },
    disabled: {
      type: Boolean,
      default: false
    },
    loading: {
      type: Boolean,
      default: false
    },
    text: {
      type: String,
      default: ''
    },
    block: {
      type: Boolean,
      default: false
    }
  },
  emits: ['click'],
  setup(props, { emit }) {
    const buttonClasses = computed(() => {
      const baseClasses = 'inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2'

      const variantClasses = {
        primary: 'bg-gray-900 text-white hover:bg-gray-800 focus:ring-gray-900 disabled:bg-gray-400',
        secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200 focus:ring-gray-500 disabled:bg-gray-100 disabled:text-gray-400',
        outline: 'border border-gray-900 text-gray-900 hover:bg-gray-900 hover:text-white focus:ring-gray-900 disabled:border-gray-300 disabled:text-gray-300',
        ghost: 'text-gray-900 hover:bg-gray-100 focus:ring-gray-500 disabled:text-gray-400',
        danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-600 disabled:bg-red-400'
      }

      const sizeClasses = {
        sm: 'px-3 py-2 text-sm',
        md: 'px-4 py-2',
        lg: 'px-6 py-3 text-lg'
      }

      const widthClass = props.block ? 'w-full' : ''
      const disabledClass = (props.disabled || props.loading) ? 'cursor-not-allowed opacity-60' : 'cursor-pointer'

      return [
        baseClasses,
        variantClasses[props.variant],
        sizeClasses[props.size],
        widthClass,
        disabledClass
      ].join(' ')
    })

    const handleClick = (event) => {
      if (!props.disabled && !props.loading) {
        emit('click', event)
      }
    }

    return {
      buttonClasses,
      handleClick
    }
  }
}
</script>
