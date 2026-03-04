import { defineStore } from 'pinia'

interface ImageItem {
  image: string
}

export const useImgModalStore = defineStore('imgModal', () => {
  const isOpen = ref(false)
  const images = ref<ImageItem[]>([])
  const activeIndex = ref(0)
  const title = ref('')
  const description = ref('')

  const open = (
    imgs: ImageItem[],
    index = 0,
    productTitle = '',
    productDescription = ''
  ) => {
    images.value = imgs
    activeIndex.value = index
    title.value = productTitle
    description.value = productDescription
    isOpen.value = true
  }

  const close = () => {
    isOpen.value = false
  }

  return {
    isOpen,
    images,
    activeIndex,
    title,
    description,
    open,
    close
  }
})