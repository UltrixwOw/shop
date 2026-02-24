import { defineNuxtPlugin } from '#app'
import { useAuthStore } from '~/stores/auth'

export default defineNuxtPlugin(async () => {
  const auth = useAuthStore()
  const { $api } = useNuxtApp()

  if (auth.initialized) return

  try {
    const res = await $api.post('/users/refresh/')
    auth.setAccessToken(res.data.access)

    const me = await $api.get('/users/me/')
    auth.user = me.data
  } catch (e) {
    auth.clearAuthState()
  } finally {
    auth.setInitialized()
  }
})