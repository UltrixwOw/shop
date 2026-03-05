// plugins/auth.client.ts
import { useAuthStore } from '~/stores/auth'
import { useCartStore } from '~/stores/cart'
import { useOrdersStore } from '~/stores/orders'
import { useWishlistStore } from '~/stores/wishlist'

export default defineNuxtPlugin(async () => {
  const auth = useAuthStore()
  const cart = useCartStore()
  const orders = useOrdersStore()
  const router = useRouter()
  const wishlist = useWishlistStore()

  // ===============================
  // INIT при загрузке приложения
  // ===============================

  if (auth.accessToken && !auth.initialized) {
    try {
      await auth.fetchUser()
      
      // Загружаем данные последовательно
      if (cart.fetchCart) await cart.fetchCart()
      if (orders.fetchOrders) await orders.fetchOrders()
      if (wishlist.fetchWishlist) await wishlist.fetchWishlist()
      
    } catch (error) {
      console.error('Auth init error:', error)
      auth.clearAuthState()
    }
  }

  auth.setInitialized()

  // ===============================
  // WATCH login/logout
  // ===============================

  watch(
    () => auth.isAuthenticated,
    async (isAuth, wasAuth) => {

      // LOGIN
      if (isAuth && !wasAuth) {
        try {
          await auth.fetchUser()
          
          // Загружаем данные
          if (cart.fetchCart) await cart.fetchCart()
          if (orders.fetchOrders) await orders.fetchOrders()
          if (wishlist.fetchWishlist) await wishlist.fetchWishlist()

          await router.push('/')
        } catch (error) {
          console.error('Login data load error:', error)
        }
      }

      // LOGOUT
      if (!isAuth && wasAuth) {
        cart.$reset?.()
        orders.$reset?.()
        wishlist.$reset?.()

        await router.push('/')
      }
    },
    { immediate: true }
  )
})