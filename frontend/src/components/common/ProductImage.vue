<!-- frontend/src/components/common/ProductImage.vue -->
<template>
  <div
    :class="[
      'flex items-center justify-center rounded-lg overflow-hidden',
      containerClass,
      hasValidImage && !imageError ? '' : 'bg-gray-100'
    ]"
    :style="{ backgroundColor: bgColor }"
  >
    <!-- Real Image Display -->
    <img
      v-if="hasValidImage && !imageError"
      :src="imageUrl"
      :alt="productName"
      class="w-full h-full object-cover"
      @error="handleImageError"
      @load="handleImageLoad"
    />

    <!-- Font Awesome Icon Display (fallback) -->
    <div v-else class="text-center flex flex-col items-center justify-center h-full">
      <i
        :class="iconClass"
        :style="{ fontSize: iconSize + 'px', color: iconColor || '#6B7280' }"
      ></i>
      <div
        v-if="showLabel && size !== 'sm'"
        class="mt-2 text-gray-700 font-medium text-center px-2"
        :style="{ fontSize: labelSize + 'px' }"
      >
        {{ truncatedProductName }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'ProductImage',
  props: {
    product: {
      type: Object,
      required: true
    },
    size: {
      type: String,
      default: 'md',
      validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value)
    },
    containerClass: {
      type: String,
      default: ''
    }
  },
  setup(props) {
    const imageError = ref(false)
    const imageLoaded = ref(false)

    const sizeConfig = {
      sm: { container: 'w-16 h-16', icon: 20, label: 8 },
      md: { container: 'w-48 h-48', icon: 40, label: 12 },
      lg: { container: 'w-64 h-64', icon: 56, label: 14 },
      xl: { container: 'w-96 h-96', icon: 72, label: 16 }
    }

    const config = computed(() => sizeConfig[props.size])

    // Определяем иконку и цвет на основе категории и названия товара
    const getProductIcon = (product) => {
      const name = product.name?.toLowerCase() || ''
      const category = product.category_name?.toLowerCase() || ''

      // Electronics
      if (name.includes('iphone') || name.includes('phone') || name.includes('mobile')) {
        return { icon: 'fas fa-mobile-alt', color: '#1f2937' }
      }
      if (name.includes('macbook') || name.includes('laptop')) {
        return { icon: 'fas fa-laptop', color: '#1f2937' }
      }
      if (name.includes('airpods') || name.includes('headphone') || name.includes('sony')) {
        return { icon: 'fas fa-headphones', color: '#1f2937' }
      }
      if (name.includes('keyboard')) {
        return { icon: 'fas fa-keyboard', color: '#6366f1' }
      }
      if (name.includes('webcam') || name.includes('camera')) {
        return { icon: 'fas fa-video', color: '#7c3aed' }
      }
      if (name.includes('mouse')) {
        return { icon: 'fas fa-mouse', color: '#ef4444' }
      }
      if (name.includes('ipad') || name.includes('tablet')) {
        return { icon: 'fas fa-tablet-alt', color: '#1f2937' }
      }
      if (name.includes('nintendo') || name.includes('switch') || name.includes('gaming')) {
        return { icon: 'fas fa-gamepad', color: '#e11d48' }
      }
      if (name.includes('galaxy') || name.includes('samsung')) {
        return { icon: 'fas fa-mobile-alt', color: '#1f2937' }
      }

      // Books
      if (name.includes('python')) {
        return { icon: 'fab fa-python', color: '#3b82f6' }
      }
      if (name.includes('javascript') || name.includes('js')) {
        return { icon: 'fab fa-js-square', color: '#f59e0b' }
      }
      if (name.includes('react')) {
        return { icon: 'fab fa-react', color: '#0891b2' }
      }
      if (name.includes('django')) {
        return { icon: 'fas fa-code', color: '#059669' }
      }
      if (name.includes('clean code') || name.includes('system design')) {
        return { icon: 'fas fa-book-open', color: '#7c3aed' }
      }
      if (category.includes('book')) {
        return { icon: 'fas fa-book', color: '#3b82f6' }
      }

      // Clothing
      if (name.includes('shirt') || name.includes('t-shirt')) {
        return { icon: 'fas fa-tshirt', color: '#6b7280' }
      }
      if (name.includes('jeans') || name.includes('pants') || name.includes('levi')) {
        return { icon: 'fas fa-user-tie', color: '#1e40af' }
      }
      if (name.includes('nike') || name.includes('shoes') || name.includes('air force')) {
        return { icon: 'fas fa-shoe-prints', color: '#000000' }
      }
      if (name.includes('hoodie') || name.includes('adidas')) {
        return { icon: 'fas fa-tshirt', color: '#1f2937' }
      }
      if (category.includes('clothing')) {
        return { icon: 'fas fa-tshirt', color: '#6b7280' }
      }

      // Home & Garden
      if (name.includes('lamp') || name.includes('light')) {
        return { icon: 'fas fa-lightbulb', color: '#dc2626' }
      }
      if (name.includes('coffee') || name.includes('maker')) {
        return { icon: 'fas fa-coffee', color: '#8b5cf6' }
      }
      if (name.includes('vacuum') || name.includes('robot')) {
        return { icon: 'fas fa-robot', color: '#059669' }
      }
      if (name.includes('air purifier') || name.includes('purifier')) {
        return { icon: 'fas fa-wind', color: '#0891b2' }
      }
      if (name.includes('smart') && name.includes('home')) {
        return { icon: 'fas fa-home', color: '#059669' }
      }
      if (category.includes('home')) {
        return { icon: 'fas fa-home', color: '#059669' }
      }

      // Sports & Outdoors
      if (name.includes('yoga') || name.includes('mat')) {
        return { icon: 'fas fa-pray', color: '#ec4899' }
      }
      if (name.includes('dumbbell') || name.includes('weight')) {
        return { icon: 'fas fa-dumbbell', color: '#374151' }
      }
      if (name.includes('resistance') && name.includes('band')) {
        return { icon: 'fas fa-grip-lines', color: '#f59e0b' }
      }
      if (category.includes('sports')) {
        return { icon: 'fas fa-dumbbell', color: '#374151' }
      }

      // Default Electronics
      if (category.includes('electronics')) {
        return { icon: 'fas fa-microchip', color: '#1f2937' }
      }

      // Fallback
      return { icon: 'fas fa-box', color: '#6b7280' }
    }

    const iconInfo = computed(() => getProductIcon(props.product))

    const hasValidImage = computed(() => {
      const url = props.product.image_url || ''
      return url &&
             !url.includes('placeholder') &&
             !url.includes('data:image/svg') &&
             url.startsWith('http')
    })

    const iconClass = computed(() => iconInfo.value.icon)
    const iconColor = computed(() => iconInfo.value.color)
    const iconSize = computed(() => config.value.icon)
    const labelSize = computed(() => config.value.label)

    const bgColor = computed(() => {
      // Определяем цвет фона на основе категории
      const category = props.product.category_name?.toLowerCase() || ''

      if (category.includes('electronics')) return '#f3f4f6'
      if (category.includes('books')) return '#eff6ff'
      if (category.includes('clothing')) return '#fefefe'
      if (category.includes('home')) return '#f0fdf4'
      if (category.includes('sports')) return '#fef3e2'

      return '#f9fafb'
    })

    const productName = computed(() => props.product.name || 'Product')
    const imageUrl = computed(() => props.product.image_url || '')

    const truncatedProductName = computed(() => {
      const name = productName.value
      if (props.size === 'sm') return ''
      if (name.length > 20) {
        return name.substring(0, 17) + '...'
      }
      return name
    })

    const showLabel = computed(() => props.size !== 'sm')

    const handleImageError = () => {
      imageError.value = true
      console.log('Image failed to load:', imageUrl.value)
    }

    const handleImageLoad = () => {
      imageLoaded.value = true
      console.log('Image loaded successfully:', imageUrl.value)
    }

    return {
      imageError,
      imageLoaded,
      hasValidImage,
      iconClass,
      iconColor,
      iconSize,
      labelSize,
      bgColor,
      productName,
      imageUrl,
      truncatedProductName,
      showLabel,
      handleImageError,
      handleImageLoad
    }
  }
}
</script>
