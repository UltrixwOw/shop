// plugins/auth.client.ts
import { useAuthStore } from '~/stores/auth'
import { useCartStore } from '~/stores/cart'
import { useOrdersStore } from '~/stores/orders'
import { useWishlistStore } from '~/stores/wishlist'
import { useProductPreviewModalStore } from '~/stores/productPreviewModal'

export default defineNuxtPlugin(async (nuxtApp) => {
  const auth = useAuthStore()
  const cart = useCartStore()
  const orders = useOrdersStore()
  const router = useRouter()
  const wishlist = useWishlistStore()
  const productModal = useProductPreviewModalStore()
  
  const { $api } = nuxtApp

  // ===============================
  // Инициализация при загрузке
  // ===============================
  
  if (auth.accessToken && !auth.initialized) {
    try {
      await auth.fetchUser($api)
      
      // Загружаем данные только если пользователь успешно получен
      if (auth.user) {
        await Promise.all([
          cart.fetchCart?.(),
          orders.fetchOrders?.(),
          wishlist.fetchWishlist?.()
        ].filter(Boolean))
      }
    } catch (error) {
      console.error('Auth init error:', error)
      auth.clearAuthState()
    }
  }

  auth.setInitialized()

  // ===============================
  // Отдельные watcher'ы для логина и логаута
  // ===============================

  // Watcher для логина
  watch(
    () => auth.isAuthenticated,
    async (isAuth) => {
      if (!isAuth) return // Только для логина
      
      try {
        await auth.fetchUser($api)
        
        if (auth.user) {
          await Promise.all([
            cart.fetchCart?.(),
            orders.fetchOrders?.(),
            wishlist.fetchWishlist?.()
          ].filter(Boolean))
          
          productModal.close()
          await router.push('/')
        }
      } catch (error) {
        console.error('Login error:', error)
      }
    }
  )

  // Watcher для логаута
  watch(
    () => !auth.isAuthenticated,
    async (isNotAuth, wasNotAuth) => {
      if (!isNotAuth || wasNotAuth) return // Только при переходе в неавторизованное
      
      productModal.close()
      cart.$reset?.()
      orders.$reset?.()
      wishlist.$reset?.()
      await router.push('/')
    }
  )
})