import { defineStore } from 'pinia'
import { useAuthStore } from './auth'

interface CartItem {
  id: number
  product: number
  product_name: string
  product_image?: string
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
  const syncing = ref(false)
  
  // Множество товаров, которые сейчас добавляются
  const pendingAdds = ref<Set<number>>(new Set())

  const authStore = useAuthStore()
  const isAuthenticated = computed(() => authStore.isAuthenticated)

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
      product_image: item.product_image,
      price: Number(item.price),
      quantity: Number(item.quantity),
      product_stock: Number(item.product_stock)
    }))

    initialized.value = true
  }

  const findItem = (id: number) =>
    items.value.find(i => i.id === id)

  const findItemByProduct = (productId: number) =>
    items.value.find(i => i.product === productId)

  // =============================
  // LOCAL STORAGE
  // =============================

  const loadLocal = () => {
    if (!import.meta.client) return

    try {
      const saved = localStorage.getItem('cart')
      if (saved) {
        const parsed = JSON.parse(saved)
        items.value = parsed.map((item: any) => ({
          ...item,
          price: Number(item.price),
          quantity: Number(item.quantity),
          product_stock: Number(item.product_stock)
        }))
      } else {
        items.value = []
      }
    } catch {
      items.value = []
    }
  }

  const saveLocal = () => {
    if (!import.meta.client) return
    localStorage.setItem('cart', JSON.stringify(items.value))
  }

  // =============================
  // FETCH
  // =============================

  const fetchCart = async () => {
    if (loading.value) return

    if (!isAuthenticated.value) {
      loadLocal()
      initialized.value = true
      return
    }

    const { $api } = useNuxtApp()
    loading.value = true

    try {
      const res = await $api.get<CartResponse>('/cart/')
      setCart(res.data)
      if (import.meta.client) {
        localStorage.removeItem('cart')
      }
    } catch (e: any) {
      if (e.response?.status === 401) {
        loadLocal()
      } else {
        console.error('Cart fetch error:', e)
        items.value = []
      }
    } finally {
      loading.value = false
    }
  }

  // =============================
  // ADD — ИСПРАВЛЕНА
  // =============================

  const addToCart = async (productId: number, quantity = 1) => {
    // Защита от двойных кликов
    if (pendingAdds.value.has(productId)) return
    pendingAdds.value.add(productId)

    try {
      // Проверяем существующий товар
      let existing = findItemByProduct(productId)

      if (existing) {
        const newQty = existing.quantity + quantity
        if (newQty > existing.product_stock) return
        
        existing.quantity = newQty
        saveLocal()
        
        if (isAuthenticated.value) {
          await updateQuantity(existing.id, newQty)
        }
        return
      }

      // === ТОВАРА НЕТ, НУЖНО ДОБАВИТЬ ===
      
      if (!isAuthenticated.value) {
        // Неавторизованный пользователь
        const { $api } = useNuxtApp()
        const res = await $api.get(`/shop/products/${productId}/`)
        const product = res.data
        
        // Повторная проверка (могло добавиться за время запроса)
        existing = findItemByProduct(productId)
        if (existing) {
          existing.quantity += quantity
        } else {
          items.value.push({
            id: Date.now(),
            product: productId,
            product_name: product.name,
            product_image: product.images?.[0]?.image || '/images/productPreview.png',
            price: Number(product.price),
            quantity: quantity,
            product_stock: product.stock
          })
        }
        saveLocal()
        return
      }

      // Авторизованный пользователь
      const { $api } = useNuxtApp()
      const res = await $api.post('/cart/add/', { 
        product_id: productId, 
        quantity 
      })
      
      // Повторная проверка (могло добавиться за время запроса)
      existing = findItemByProduct(productId)
      if (existing) {
        existing.quantity += quantity
        await updateQuantity(existing.id, existing.quantity)
      } else if (res.data?.id) {
        items.value.push({
          id: res.data.id,
          product: res.data.product,
          product_name: res.data.product_name,
          product_image: res.data.product_image,
          price: Number(res.data.price),
          quantity: Number(res.data.quantity),
          product_stock: Number(res.data.product_stock)
        })
        saveLocal()
      } else {
        await fetchCart()
      }
      
    } catch (e) {
      console.error('Add to cart failed', e)
    } finally {
      pendingAdds.value.delete(productId)
    }
  }

  // =============================
  // REMOVE
  // =============================

  const removeFromCart = async (itemId: number) => {
    const backup = [...items.value]
    items.value = items.value.filter(i => i.id !== itemId)

    if (!isAuthenticated.value) {
      saveLocal()
      return
    }

    const { $api } = useNuxtApp()
    try {
      await $api.delete(`/cart/remove/${itemId}/`)
      saveLocal()
    } catch (e: any) {
      items.value = backup
      if (e.response?.status === 401) {
        saveLocal()
      } else {
        console.error('Remove from cart failed', e)
      }
    }
  }

  // =============================
  // UPDATE QUANTITY
  // =============================

  const updateQuantity = async (itemId: number, quantity: number) => {
    if (quantity < 1) return

    const item = findItem(itemId)
    if (!item) return
    if (quantity > item.product_stock) return

    const oldQuantity = item.quantity
    item.quantity = quantity

    if (!isAuthenticated.value) {
      saveLocal()
      return
    }

    const { $api } = useNuxtApp()
    try {
      await $api.patch(`/cart/update/${itemId}/`, { quantity })
      saveLocal()
    } catch (e: any) {
      item.quantity = oldQuantity
      if (e.response?.status === 401) {
        saveLocal()
      } else {
        console.error('Update quantity failed', e)
      }
    }
  }

  // =============================
  // SYNC LOCAL TO SERVER
  // =============================

  const syncLocalToServer = async () => {
    if (!import.meta.client) return
    if (syncing.value) return

    loadLocal()

    if (isAuthenticated.value && items.value.length > 0) {
      syncing.value = true
      const localItems = [...items.value]

      try {
        const { $api } = useNuxtApp()
        const itemsToSync = localItems.map(item => ({
          product_id: item.product,
          quantity: item.quantity
        }))

        const response = await $api.post('/cart/sync/', {
          items: itemsToSync
        })

        if (response.data?.items) {
          setCart({ items: response.data.items })
        }

        if (import.meta.client) {
          localStorage.removeItem('cart')
        }

        return response.data

      } catch (e) {
        console.error('Failed to sync cart to server:', e)
        await fetchCart()
        throw e
      } finally {
        syncing.value = false
      }
    } else if (isAuthenticated.value) {
      await fetchCart()
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

  // =============================
  // INIT
  // =============================

  const init = async () => {
    if (!import.meta.client) return
    if (initialized.value) return

    if (isAuthenticated.value) {
      await syncLocalToServer()
    } else {
      loadLocal()
      initialized.value = true
    }
  }

  // =============================
  // RESET
  // =============================

  const $reset = () => {
    items.value = []
    saveLocal()
  }

  // Следим за изменением авторизации
  watch(() => authStore.isAuthenticated, async (newVal, oldVal) => {
    if (newVal && !oldVal) {
      await syncLocalToServer()
    } else if (!newVal && oldVal) {
      loadLocal()
    }
  })

  return {
    items,
    loading,
    initialized,
    isAuthenticated,
    syncing,
    pendingAdds,

    totalPrice,
    totalCount,
    isEmpty,

    fetchCart,
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCartState,
    checkout,
    setCart,
    syncLocalToServer,
    init,
    loadLocal,
    $reset
  }
})