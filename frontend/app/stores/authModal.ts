import { defineStore } from 'pinia'

export const useAuthModalStore = defineStore('authModal', () => {
  const isOpen = ref(false)

  const open = () => isOpen.value = true
  const close = () => isOpen.value = false

  return {
    isOpen,
    open,
    close
  }
})