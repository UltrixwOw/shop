import { defineStore } from 'pinia'

interface Product {
  id: number
  name: string
  slug: string
  description: string
  price: string
  stock: number
  images: { image: string }[]

  average_rating?: number
  reviews_count?: number
}

export const useProductPreviewModalStore = defineStore('productPreviewModal', () => {
  const isOpen = ref(false)

  const product = ref<Product | null>(null)

  const loading = ref(false)

  // cache products
  const cache = reactive<Record<number, Product>>({})

  const open = async (
    productId: number,
    initialData?: Product
  ) => {
    isOpen.value = true

    // 1. Есть уже полный продукт в кеше
    if (cache[productId]) {
      product.value = cache[productId]
      return
    }

    // 2. Есть initialData (например из products page)
    if (initialData) {
      product.value = initialData
      cache[productId] = initialData
      return
    }

    // 3. Грузим с API
    loading.value = true

    try {
      const { $api } = useNuxtApp()

      const res = await $api.get<Product>(
        `/shop/products/${productId}/`
      )

      product.value = res.data

      // сохраняем в cache
      cache[productId] = res.data
    } catch (error) {
      console.error('Failed load product preview', error)
    } finally {
      loading.value = false
    }
  }

  const close = () => {
    isOpen.value = false
    product.value = null
  }

  return {
    isOpen,
    product,
    loading,
    cache,
    open,
    close
  }
})