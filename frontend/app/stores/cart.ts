import { defineStore } from 'pinia'

interface CartItem {
  id: number
  product: number
  product_name: string
  product_price: number
  quantity: number
}

interface CartResponse {
  items: CartItem[]
}

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])
  const loading = ref(false)
  const initialized = ref(false)

  // =============================
  // COMPUTED
  // =============================

  const totalPrice = computed(() =>
    items.value.reduce(
      (sum, item) => sum + item.product_price * item.quantity,
      0
    )
  )

  const totalCount = computed(() =>
    items.value.reduce((sum, item) => sum + item.quantity, 0)
  )

  const isEmpty = computed(() => items.value.length === 0)

  // =============================
  // INTERNAL HELPERS
  // =============================

  const setCart = (data: CartResponse) => {
    items.value = data.items || []
    initialized.value = true
  }

  const findItem = (itemId: number) =>
    items.value.find(i => i.id === itemId)

  // =============================
  // FETCH (SSR-safe)
  // =============================

  const fetchCart = async () => {
    if (loading.value) return

    const { $api } = useNuxtApp()
    loading.value = true

    try {
      const res = await $api.get<CartResponse>('/cart/')
      setCart(res.data)
    } catch (e) {
      items.value = []
    } finally {
      loading.value = false
    }
  }

  // =============================
  // ADD (Optimistic)
  // =============================

  const addToCart = async (productId: number, quantity = 1) => {
    const { $api } = useNuxtApp()

    try {
      const existing = items.value.find(i => i.product === productId)

      if (existing) {
        await updateQuantity(existing.id, existing.quantity + quantity)
        return
      }

      const res = await $api.post('/cart/add/', {
        product_id: productId,
        quantity
      })

      // если backend не возвращает item → делаем fetch
      if (res.data?.id) {
        items.value.push(res.data)
      } else {
        await fetchCart()
      }

    } catch (e) {
      console.error('Add to cart failed', e)
    }
  }

  // =============================
  // REMOVE (Optimistic)
  // =============================

  const removeFromCart = async (itemId: number) => {
    const { $api } = useNuxtApp()

    const backup = [...items.value]

    // optimistic remove
    items.value = items.value.filter(i => i.id !== itemId)

    try {
      await $api.delete(`/cart/remove/${itemId}/`)
    } catch (e) {
      items.value = backup
      console.error('Remove failed', e)
    }
  }

  // =============================
  // UPDATE QUANTITY
  // =============================

  const updateQuantity = async (itemId: number, quantity: number) => {
    if (quantity < 1) return

    const { $api } = useNuxtApp()

    const item = findItem(itemId)
    if (!item) return

    const oldQuantity = item.quantity

    // 🔥 Optimistic UI
    item.quantity = quantity

    try {
      await $api.patch(`/cart/update/${itemId}/`, { quantity })
    } catch (e) {
      // rollback если ошибка
      item.quantity = oldQuantity
      console.error('Update failed', e)
    }
  }

  // =============================
  // CLEAR (local only)
  // =============================

  const clearCartState = () => {
    items.value = []
    initialized.value = false
  }

  const checkout = async (addressId: number) => {
    const { $api } = useNuxtApp()

    const res = await $api.post('/orders/checkout/', { address_id: addressId })

    // Очистка корзины уже делается на сервере
    await fetchCart()

    return res.data
  }

  return {
    // state
    items,
    loading,
    initialized,

    // computed
    totalPrice,
    totalCount,
    isEmpty,

    // methods
    fetchCart,
    addToCart,
    setCart,
    checkout,
    removeFromCart,
    updateQuantity,
    clearCartState
  }
})