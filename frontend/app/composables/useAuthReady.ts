import { useAuthStore } from '~/stores/auth'

export async function useAuthReady() {

  const auth = useAuthStore()

  await until(() => auth.initialized).toBe(true)

  return auth

}