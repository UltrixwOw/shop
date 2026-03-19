import { useAuthStore } from '~/stores/auth'
import type { AxiosInstance } from 'axios'

export default defineNuxtPlugin(async (nuxtApp) => {
  console.log('🔥 SSR PLUGIN LOADED', process.server)
  const auth = useAuthStore()
  const headers = useRequestHeaders(['cookie'])

  console.log('🔥 SSR COOKIE:', headers.cookie)
  console.log('auth.initialized == true, return, ', auth.initialized)
  if (auth.initialized) return

  const api = nuxtApp.$api as AxiosInstance

  console.log('🖥 SSR AUTH INIT')

  try {

    const res = await api.post('/users/refresh/')

    auth.setAccessToken(res.data.access)

    const me = await api.get('/users/me/')

    auth.setUser(me.data)

  } catch (e) {

    auth.clearAuthState()

  } finally {

    auth.setInitialized()

  }

})