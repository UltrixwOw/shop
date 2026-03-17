import { useAuthStore } from '~/stores/auth'

export default defineNuxtPlugin(() => {

  const auth = useAuthStore()

  console.log('🌐 CLIENT AUTH INIT')

  if (!auth.initialized) {

    console.warn('⚠️ SSR auth not initialized')

  }

})