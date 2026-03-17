import { defineStore } from 'pinia'

interface User {
  id: number
  email: string
  role: string
}

export const useAuthStore = defineStore('auth', {

  // =====================
  // STATE
  // =====================

  state: () => ({
    user: null as User | null,
    accessToken: null as string | null,
    loading: false,
    initialized: false
  }),

  // =====================
  // GETTERS
  // =====================

  getters: {

    isAuthenticated: (state) => !!state.accessToken,

    isAdmin: (state) => state.user?.role === 'admin',

    userEmail: (state) => state.user?.email || null

  },

  // =====================
  // ACTIONS
  // =====================

  actions: {

    setInitialized() {
      this.initialized = true
    },

    setAccessToken(token: string | null) {
      console.log('🔑 setAccessToken', token)
      this.accessToken = token
    },

    setUser(user: User | null) {
      console.log('👤 setUser', user)
      this.user = user
    },

    clearAuthState() {
      console.log('🚪 clearAuthState')
      this.user = null
      this.accessToken = null
    },

    async login(email: string, password: string) {
      const nuxtApp = useNuxtApp()
      const api = nuxtApp.$api

      console.log('🔐 LOGIN START')
      this.loading = true

      try {
        const res = await api.post('/users/login/', {
          email,
          password
        })

        console.log('🔑 access token received')
        this.setAccessToken(res.data.access)
        await this.fetchUser(api)

      } finally {
        this.loading = false
        console.log('🔐 LOGIN END')
      }
    },

    async fetchUser(api?: any) {
      try {
        const nuxtApp = useNuxtApp()
        const $api = api || nuxtApp.$api
        const res = await $api.get('/users/me/')
        this.setUser(res.data)
        return res.data
      } catch (error) {
        console.error('Fetch user error:', error)
        throw error
      }
    },

    async refresh(api?: any) {
      const nuxtApp = useNuxtApp()
      const $api = api || nuxtApp.$api
      const res = await $api.post('/users/refresh/')
      this.setAccessToken(res.data.access)
      return res.data
    },

    async logout() {
      const nuxtApp = useNuxtApp()
      const api = nuxtApp.$api
      try {
        await api.post('/users/logout/')
      } catch (e) {}
      this.clearAuthState()
    }
  },

  // =====================
  // HYDRATION
  // =====================

  hydrate(state, initialState) {
    // Эта функция вызывается при гидрации на клиенте
    // state - текущее состояние на клиенте
    // initialState - состояние, отправленное с сервера
    
    if (import.meta.client) {
      console.log('💧 hydrating auth store', {
        hasToken: !!state.accessToken,
        hasInitialToken: !!initialState.accessToken
      })

      // Сохраняем токен при гидрации если он есть
      if (state.accessToken && !initialState.accessToken) {
        initialState.accessToken = state.accessToken
      }

      // Сохраняем пользователя при гидрации если он есть
      if (state.user && !initialState.user) {
        initialState.user = state.user
      }
    }
  }
})