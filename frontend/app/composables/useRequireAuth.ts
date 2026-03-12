import { useAuthStore } from "~/stores/auth"
import { useAuthModalStore } from "~/stores/authModal"

export function useRequireAuth() {
  const auth = useAuthStore()
  const authModal = useAuthModalStore()

  async function requireAuth(action: () => Promise<void> | void) {
    if (!auth.isAuthenticated) {
      authModal.open()
      return
    }

    await action()
  }

  return { requireAuth }
}