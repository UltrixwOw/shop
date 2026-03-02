import { defineStore } from 'pinia'

interface CartItem {
  id: number
  product: number
  product_name: string
  price: number
  quantity: number
  product_stock: number
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
    items.value.reduce((sum, i) => sum + i.price * i.quantity, 0)
  )

  const totalCount = computed(() =>
    items.value.reduce((sum, i) => sum + i.quantity, 0)
  )

  const isEmpty = computed(() => items.value.length === 0)

  // =============================
  // INTERNAL
  // =============================

  const setCart = (data: any) => {
    items.value = (data.items || []).map((item: any) => ({
      id: item.id,
      product: item.product,
      product_name: item.product_name,
      price: Number(item.price),
      quantity: Number(item.quantity),
      product_stock: Number(item.product_stock)
    }))

    initialized.value = true
  }

  const findItem = (id: number) =>
    items.value.find(i => i.id === id)

  // =============================
  // FETCH
  // =============================

  const fetchCart = async () => {
    if (loading.value) return

    const { $api } = useNuxtApp()
    loading.value = true

    try {
      const res = await $api.get<CartResponse>('/cart/')
      setCart(res.data)
    } catch {
      items.value = []
    } finally {
      loading.value = false
    }
  }

  // =============================
  // ADD
  // =============================

  const addToCart = async (productId: number, quantity = 1) => {
    const { $api } = useNuxtApp()

    try {
      const existing = items.value.find(i => i.product === productId)

      if (existing) {
        const newQty = existing.quantity + quantity

        if (newQty > existing.product_stock) return

        await updateQuantity(existing.id, newQty)
        return
      }

      const res = await $api.post('/cart/add/', {
        product_id: productId,
        quantity
      })

      if (res.data?.id) {
        items.value.push({
          id: res.data.id,
          product: res.data.product,
          product_name: res.data.product_name,
          price: Number(res.data.price),
          quantity: Number(res.data.quantity),
          product_stock: Number(res.data.product_stock)
        })
      } else {
        await fetchCart()
      }

    } catch (e) {
      console.error('Add to cart failed', e)
    }
  }

  // =============================
  // REMOVE
  // =============================

  const removeFromCart = async (itemId: number) => {
    const { $api } = useNuxtApp()

    const backup = [...items.value]
    items.value = items.value.filter(i => i.id !== itemId)

    try {
      await $api.delete(`/cart/remove/${itemId}/`)
    } catch (e) {
      items.value = backup
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

    if (quantity > item.product_stock) return

    const oldQuantity = item.quantity
    item.quantity = quantity // optimistic

    try {
      await $api.patch(`/cart/update/${itemId}/`, { quantity })
    } catch (e: any) {
      item.quantity = oldQuantity // rollback

      if (e.response?.data?.detail) {
        console.error(e.response.data.detail)
      }
    }
  }

  // =============================
  // CLEAR
  // =============================

  const clearCartState = () => {
    items.value = []
    initialized.value = false
  }

  // =============================
  // CHECKOUT
  // =============================

  const checkout = async (addressId: number) => {
    const { $api } = useNuxtApp()

    const res = await $api.post('/orders/checkout/', {
      address_id: addressId
    })

    await fetchCart()
    return res.data
  }

  return {
    items,
    loading,
    initialized,

    totalPrice,
    totalCount,
    isEmpty,

    fetchCart,
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCartState,
    checkout,
    setCart
  }
})