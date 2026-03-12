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
      
      if (auth.user) {
        // Синхронизируем вишлист и корзину
        await Promise.all([
          wishlist.syncLocalToServer?.(),
          cart.syncLocalToServer?.()
        ])
        
        // Потом загружаем остальные данные
        await Promise.all([
          orders.fetchOrders?.()
        ].filter(Boolean))
      }
    } catch (error) {
      console.error('Auth init error:', error)
      auth.clearAuthState()
    }
  } else {
    // Если пользователь не авторизован, загружаем из localStorage
    wishlist.loadLocal?.()
    cart.loadLocal?.()
  }

  auth.setInitialized()

  // Watcher для логина - убираем синхронизацию отсюда, так как она уже есть в инициализации
  watch(
    () => auth.isAuthenticated,
    async (isAuth, wasAuth) => {
      if (!isAuth || wasAuth) return
      
      // Только редирект и закрытие модалки, без синхронизации
      productModal.close()
      await router.push('/')
    }
  )

  // Watcher для логаута
  watch(
    () => !auth.isAuthenticated,
    async (isNotAuth, wasNotAuth) => {
      if (!isNotAuth || wasNotAuth) return
      
      productModal.close()
      cart.$reset?.()
      orders.$reset?.()
      wishlist.$reset?.()
      await router.push('/')
    }
  )
})