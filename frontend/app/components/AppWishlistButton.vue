<script setup lang="ts">
import { useWishlistStore } from "~/stores/wishlist"

const wishlist = useWishlistStore()

const mounted = ref(false)

onMounted(() => {
  mounted.value = true
})
</script>

<template>
  <UChip
    :show="mounted && wishlist.items.length > 0"
    position="my-bottom-left"
    color="myPink"
  >
    <AppLink to="/wishlist">
      <UButton
        icon="i-heroicons-heart"
        variant="ghost"
      />
    </AppLink>
  </UChip>
</template>