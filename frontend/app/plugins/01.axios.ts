import axios, { type AxiosInstance } from 'axios'
import { defineNuxtPlugin, useRuntimeConfig, useRequestHeaders } from '#app'
import { useAuthStore } from '~/stores/auth'

export default defineNuxtPlugin((nuxtApp) => {

  const config = useRuntimeConfig()
  const auth = useAuthStore()

  const locale = (nuxtApp.$i18n as any).locale

  const headers = process.server
    ? useRequestHeaders(['cookie'])
    : {}

  const isRender = process.env.RENDER === 'true'

  let api, plainAxios

  if (isRender) {
    // 📦 Режим Render.com (прод)
    api = axios.create({
      baseURL: process.server
        ? config.API_BASE_URL as string
        : config.public.apiBase as string,
      withCredentials: true,
      headers: process.server
        ? { cookie: headers.cookie ?? '' }
        : {}
    })

    plainAxios = axios.create({
      baseURL: process.server
        ? config.API_BASE_URL as string
        : config.public.apiBase as string,
      withCredentials: true,
      headers: process.server
        ? { cookie: headers.cookie ?? '' }
        : {}
    })
  } else {
    // 💻 Режим разработки (локально)
    api = axios.create({
      baseURL: config.public.apiBase as string,
      withCredentials: true,
      headers
    })

    plainAxios = axios.create({
      baseURL: config.public.apiBase as string,
      withCredentials: true,
      headers
    })
  }


  // =====================
  // REQUEST
  // =====================

  api.interceptors.request.use((config) => {

    if (auth.accessToken) {
      config.headers?.set(
        'Authorization',
        `Bearer ${auth.accessToken}`
      )
    }

    // ✅ i18n
    config.headers?.set('Accept-Language', locale.value)

    console.log('🌍 language:', locale.value)

    return config
  })

  // =====================
  // RESPONSE
  // =====================

  api.interceptors.response.use(
    (response) => response,

    async (error) => {

      const originalRequest = error.config

      if (
        originalRequest?.url?.includes('/users/refresh/') ||
        originalRequest?.url?.includes('/users/logout/')
      ) {
        return Promise.reject(error)
      }

      if (originalRequest?._retry) {
        return Promise.reject(error)
      }

      if (error.response?.status === 401) {

        originalRequest._retry = true

        try {

          console.log('🔄 refreshing token')

          const refreshRes = await plainAxios.post('/users/refresh/')
          const newAccess = refreshRes.data.access

          auth.setAccessToken(newAccess)

          originalRequest.headers.Authorization = `Bearer ${newAccess}`

          return api(originalRequest)

        } catch (refreshError) {

          console.log('❌ refresh failed')

          auth.clearAuthState()

          return Promise.reject(refreshError)

        }

      }

      return Promise.reject(error)
    }
  )

  return {
    provide: {
      api
    }
  }

})