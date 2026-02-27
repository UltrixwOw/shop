<script setup lang="ts">
import { useCartStore } from '~/stores/cart'

const props = defineProps({
  productId: Number
})

const cart = useCartStore()
const loading = ref(false)

const isInCart = computed(() =>
  cart.items.some(i => i.product === props.productId)
)

const add = async () => {
  if (isInCart.value) return
  loading.value = true
  await cart.addToCart(props.productId, 1)
  loading.value = false
}
</script>

<template>
  <UButton
    color="primary"
    :loading="loading"
    :disabled="isInCart"
    block
    @click="add"
  >
    <span v-if="isInCart">✓ In cart</span>
    <span v-else>Add</span>
  </UButton>
</template>