import { defineStore } from 'pinia'

export const useProductPreviewModalStore = defineStore('productPreviewModal', () => {
  const isOpen = ref(false)
  const product = ref<any>(null)

  const open = (data: any) => {
    product.value = data
    isOpen.value = true
  }

  const close = () => {
    isOpen.value = false
    product.value = null
  }

  return {
    isOpen,
    product,
    open,
    close
  }
})