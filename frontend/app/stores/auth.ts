import { defineStore } from 'pinia'

interface User {
  id: number
  email: string
  role: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(null)
  const loading = ref(false)
  const initialized = ref(false)

  const isAuthenticated = computed(() => !!accessToken.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  const login = async (email: string, password: string) => {
    const { $api } = useNuxtApp()
    loading.value = true

    try {
      const res = await $api.post('/users/login/', {
        email,
        password
      })

      accessToken.value = res.data.access
      await fetchUser()

    } finally {
      loading.value = false
    }
  }

  const setInitialized = () => {
    initialized.value = true
  }

  const setAccessToken = (token: string) => {
    accessToken.value = token
  }

  // 🔧 ИСПРАВЛЕНО: может принимать api как параметр, но не обязательно
  const fetchUser = async (api?: any) => {
    try {
      // Используем переданный api или получаем из контекста
      let $api
      if (api) {
        $api = api
      } else {
        const nuxtApp = useNuxtApp()
        $api = nuxtApp.$api
      }
      
      const res = await $api.get('/users/me/')
      user.value = res.data
      return res.data
    } catch (error) {
      console.error('Fetch user error:', error)
      throw error
    }
  }

  const refresh = async () => {
    const { $api } = useNuxtApp()
    const res = await $api.post('/users/refresh/')
    accessToken.value = res.data.access
  }

  const clearAuthState = () => {
    user.value = null
    accessToken.value = null
  }

  const logout = async () => {
    const { $api } = useNuxtApp()
    try {
      await $api.post('/users/logout/')
    } catch (e) { }
    clearAuthState()
  }

  return {
    user,
    accessToken,
    loading,
    initialized,
    isAuthenticated,
    login,
    setInitialized,
    setAccessToken,
    fetchUser,
    refresh,
    clearAuthState,
    logout
  }
})