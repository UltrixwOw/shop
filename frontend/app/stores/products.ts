import { defineStore } from 'pinia'

interface Product {
  id: number
  name: string
  slug: string
  description: string
  price: string
  stock: number
  images: { image: string }[]
}

export const useProductsStore = defineStore('products', () => {
  const items = ref<Product[]>([])
  const loading = ref(false)
  const initialized = ref(false)

  // =============================
  // FETCH
  // =============================

  const fetchProducts = async (): Promise<Product[]> => {
    if (initialized.value) {
      return items.value
    }

    const { $api } = useNuxtApp()
    loading.value = true

    try {
      const res = await $api.get<Product[]>('/shop/products/')
      items.value = res.data
      initialized.value = true
      return res.data
    } finally {
      loading.value = false
    }
  }

  // =============================
  // STOCK HELPERS
  // =============================

  const updateStock = (productId: number, newStock: number) => {
    const product = items.value.find(p => p.id === productId)
    if (product) {
      product.stock = newStock
    }
  }

  const decreaseStock = (productId: number, quantity: number) => {
    const product = items.value.find(p => p.id === productId)
    if (product) {
      product.stock = Math.max(0, product.stock - quantity)
    }
  }

  const increaseStock = (productId: number, quantity: number) => {
    const product = items.value.find(p => p.id === productId)
    if (product) {
      product.stock += quantity
    }
  }

  return {
    items,
    loading,
    initialized,
    fetchProducts,
    updateStock,
    decreaseStock,
    increaseStock
  }
})