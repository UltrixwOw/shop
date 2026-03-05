// plugins/initWishlist.ts
import { defineNuxtPlugin } from '#app'
import { useWishlistStore } from '~/stores/wishlist'
import { useAuthStore } from '~/stores/auth'
import type { AxiosInstance } from 'axios'

export default defineNuxtPlugin(async (nuxtApp) => {
  const wishlist = useWishlistStore()
  const auth = useAuthStore()
  const api = nuxtApp.$api as AxiosInstance

  // Если пользователь авторизован - загружаем с бэкенда
  if (auth.isAuthenticated) {
    try {
      const res = await api.get('/wishlist/')
      wishlist.setWishlist(res.data)
      
      // Загружаем информацию о шаринге
      await wishlist.fetchShareInfo()
    } catch {
      wishlist.clearWishlistState()
    }
  } else {
    // Если не авторизован - загружаем из localStorage
    wishlist.loadLocal()
    wishlist.initialized = true
  }
})