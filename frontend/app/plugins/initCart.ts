import { defineNuxtPlugin } from '#app'
import { useCartStore } from '~/stores/cart'
import type { AxiosInstance } from 'axios'

export default defineNuxtPlugin(async (nuxtApp) => {
  const cart = useCartStore()
  const api = nuxtApp.$api as AxiosInstance

  try {
    const res = await api.get('/cart/')
    cart.setCart(res.data)
  } catch {
    cart.clearCartState()
  }
})