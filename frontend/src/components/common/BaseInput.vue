<template>
  <div class="w-full">
    <label v-if="label" :for="inputId" class="block text-sm font-medium text-black mb-1">
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1">*</span>
    </label>

    <div class="relative">
      <input
        :id="inputId"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :class="[
          'w-full px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-black focus:border-black transition-all duration-200',
          $slots.icon ? 'pl-10' : '',
          $slots.right ? 'pr-10' : '',
          disabled ? 'opacity-50 cursor-not-allowed' : '',
          error ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''
        ]"
        @input="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
      >

      <!-- Icon Slot -->
      <div v-if="$slots.icon" class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <slot name="icon" />
      </div>

      <!-- Right Side Content (e.g., clear button, validation icon) -->
      <div v-if="$slots.right" class="absolute inset-y-0 right-0 pr-3 flex items-center">
        <slot name="right" />
      </div>
    </div>

    <!-- Help Text -->
    <p v-if="helpText && !error" class="mt-1 text-sm text-gray-500">
      {{ helpText }}
    </p>

    <!-- Error Message -->
    <p v-if="error" class="mt-1 text-sm text-red-600">
      {{ error }}
    </p>
  </div>
</template>

<script>
import { computed, ref } from 'vue'

export default {
  name: 'BaseInput',
  props: {
    modelValue: {
      type: [String, Number],
      default: ''
    },
    type: {
      type: String,
      default: 'text'
    },
    label: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: ''
    },
    helpText: {
      type: String,
      default: ''
    },
    error: {
      type: String,
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    },
    readonly: {
      type: Boolean,
      default: false
    },
    required: {
      type: Boolean,
      default: false
    },
    size: {
      type: String,
      default: 'md',
      validator: (value) => ['sm', 'md', 'lg'].includes(value)
    }
  },
  emits: ['update:modelValue', 'blur', 'focus'],
  setup(props, { emit }) {
    const inputId = ref(`input-${Math.random().toString(36).substr(2, 9)}`)

    const inputClasses = computed(() => {
      const baseClasses = 'form-input'
      const sizeClasses = {
        sm: 'px-3 py-2 text-sm',
        md: 'px-4 py-3',
        lg: 'px-4 py-4 text-lg'
      }

      const iconPadding = props.$slots?.icon ? 'pl-10' : ''
      const errorClasses = props.error ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''
      const disabledClasses = props.disabled ? 'bg-gray-100 cursor-not-allowed' : ''

      return [
        baseClasses,
        sizeClasses[props.size],
        iconPadding,
        errorClasses,
        disabledClasses
      ].filter(Boolean).join(' ')
    })

    const handleInput = (event) => {
      emit('update:modelValue', event.target.value)
    }

    const handleBlur = (event) => {
      emit('blur', event)
    }

    const handleFocus = (event) => {
      emit('focus', event)
    }

    return {
      inputId,
      inputClasses,
      handleInput,
      handleBlur,
      handleFocus
    }
  }
}
</script>
