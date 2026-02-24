// middleware/auth.ts
import { defineNuxtRouteMiddleware } from '#app'
import { useAuthStore } from '~/stores/auth'

export default defineNuxtRouteMiddleware(async (to) => {
  const auth = useAuthStore()
  
  if (!auth.accessToken) {
    return navigateTo('/')
  }
})