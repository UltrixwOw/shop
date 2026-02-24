import { defineStore } from 'pinia'

interface Product {
  id: number
  name: string
  slug: string
  description: string
  price: string
  images: { image: string }[]
}

export const useProductsStore = defineStore('products', () => {
  const items = ref<Product[]>([])
  const loading = ref(false)

  const fetchProducts = async () => {
    if (items.value.length) return

    const { $api } = useNuxtApp()
    loading.value = true

    try {
      const res = await $api.get('/shop/products/')
      items.value = res.data
    } finally {
      loading.value = false
    }
  }

  return {
    items,
    loading,
    fetchProducts
  }
})