// middleware/auth.ts
import { defineNuxtRouteMiddleware } from '#app'
import { useAuthStore } from '~/stores/auth'

export default defineNuxtRouteMiddleware(async (to) => {
  const auth = useAuthStore()
  
  // Если store не инициализирован, ждем
  if (!auth.initialized) {
    // Можно добавить логику ожидания
    return
  }
  
  if (!auth.accessToken) {
    return navigateTo('/login')
  }
})