<script setup lang="ts">
import { useWishlistStore } from "~/stores/wishlist"

const props = defineProps<{
  productId: number
}>()

const wishlist = useWishlistStore()

// Используем ClientOnly для избежания гидратации
const isActive = computed(() => {
  // На сервере всегда возвращаем false для пустого сердца
  if (import.meta.server) return false
  return wishlist.isInWishlist(props.productId)
})
</script>

<template>
  <ClientOnly>
    <UButton
      :icon="isActive ? 'i-heroicons-heart-solid' : 'i-heroicons-heart'"
      color="neutral"
      variant="ghost"
      :class="[
        'transition-colors',
        isActive ? 'text-myPink-500 hover:text-myPink-600' : 'text-gray-500 hover:text-gray-700'
      ]"
      @click.stop="wishlist.toggleWishlist(productId)"
    />
    <template #fallback>
      <!-- Плейсхолдер для сервера - пустое сердце -->
      <UButton
        icon="i-heroicons-heart"
        color="neutral"
        variant="ghost"
        class="text-gray-500"
        disabled
      />
    </template>
  </ClientOnly>
</template>