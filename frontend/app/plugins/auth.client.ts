import { useAuthStore } from '~/stores/auth'
import { useCartStore } from '~/stores/cart'
import { useOrdersStore } from '~/stores/orders'

export default defineNuxtPlugin(async () => {
  const auth = useAuthStore()
  const cart = useCartStore()
  const orders = useOrdersStore()
  const router = useRouter()

  // ===============================
  // INIT при загрузке приложения
  // ===============================

  if (auth.accessToken && !auth.initialized) {
    try {
      await auth.fetchUser()
      await Promise.all([
        cart.fetchCart?.(),
        orders.fetchOrders?.()
      ])
    } catch {
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
        await Promise.all([
          auth.fetchUser(),
          cart.fetchCart?.(),
          orders.fetchOrders?.()
        ])

        await router.push('/')
      }

      // LOGOUT
      if (!isAuth && wasAuth) {
        cart.$reset?.()
        orders.$reset?.()

        await router.push('/')
      }
    }
  )
})