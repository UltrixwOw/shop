import axios, { type AxiosInstance } from 'axios'
import { defineNuxtPlugin, useRuntimeConfig, useRequestHeaders } from '#app'
import { useAuthStore } from '~/stores/auth'

export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig()
  const auth = useAuthStore()

  // 🔹 SSR cookie headers
  const headers = useRequestHeaders(['cookie'])

  // 🔹 основной axios
  const api: AxiosInstance = axios.create({
    baseURL: config.public.apiBase,
    withCredentials: true,
    headers
  })

  // 🔹 axios без интерцепторов (для refresh)
  const plainAxios = axios.create({
    baseURL: config.public.apiBase,
    withCredentials: true,
    headers
  })

  // =====================
  // REQUEST
  // =====================
  api.interceptors.request.use((config) => {
    if (auth.accessToken) {
      config.headers.Authorization = `Bearer ${auth.accessToken}`
    }
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
          const refreshRes = await plainAxios.post('/users/refresh/')
          const newAccess = refreshRes.data.access

          auth.setAccessToken(newAccess)

          originalRequest.headers.Authorization = `Bearer ${newAccess}`

          return api(originalRequest)
        } catch (refreshError) {
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