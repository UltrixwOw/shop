import { useAuthStore } from '~/stores/auth'
import { useCartStore } from '~/stores/cart'
import type { AxiosInstance } from 'axios'

export default defineNuxtPlugin(async (nuxtApp) => {

  const auth = useAuthStore()
  const cart = useCartStore()

  await until(() => auth.initialized).toBe(true)

  if (!auth.isAuthenticated) return

  const api = nuxtApp.$api as AxiosInstance

  try {

    const res = await api.get('/cart/')

    cart.setCart(res.data)

  } catch {

    cart.clearCartState()

  }

})