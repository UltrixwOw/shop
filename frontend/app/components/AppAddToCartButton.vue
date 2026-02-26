<script setup>
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
  <button
    @click="add"
    :disabled="loading || isInCart"
    :class="[
      'btn',
      isInCart ? 'in-cart' : ''
    ]"
  >
    <span v-if="isInCart">✓ In cart</span>
    <span v-else>{{ loading ? 'Adding...' : 'Add to cart' }}</span>
  </button>
</template>

<style scoped>
.btn {
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  background: black;
  color: white;
}

.in-cart {
  background: green;
  cursor: not-allowed;
}
</style>