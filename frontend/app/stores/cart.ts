import { defineStore } from 'pinia'

interface CartItem {
  id: number
  product: number
  product_name: string
  product_price: number
  quantity: number
}

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])
  const loading = ref(false)

  const totalPrice = computed(() =>
    items.value.reduce(
      (sum, item) => sum + item.product_price * item.quantity,
      0
    )
  )

  const totalCount = computed(() =>
    items.value.reduce((sum, item) => sum + item.quantity, 0)
  )

  // 📦 загрузка корзины
  const fetchCart = async () => {
    const { $api } = useNuxtApp()
    loading.value = true
    try {
      const res = await $api.get('/cart/')
      items.value = res.data.items
    } finally {
      loading.value = false
    }
  }

  // ➕ добавить товар
  const addToCart = async (productId: number, quantity = 1) => {
    const { $api } = useNuxtApp()
    await $api.post('/cart/add/', {
      product_id: productId,
      quantity
    })
    await fetchCart()
  }

  // ➖ удалить товар
  const removeFromCart = async (itemId: number) => {
    const { $api } = useNuxtApp()
    await $api.delete(`/cart/remove/${itemId}/`)
    await fetchCart()
  }

  // 🔄 обновить количество
  const updateQuantity = async (itemId: number, quantity: number) => {
    const { $api } = useNuxtApp()
    await $api.patch(`/cart/update/${itemId}/`, {
      quantity
    })
    await fetchCart()
  }

  const clearCart = () => {
    items.value = []
  }

  return {
    items,
    loading,
    totalPrice,
    totalCount,
    fetchCart,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart
  }
})