<script setup lang="ts">
import { useCartStore } from '~/stores/cart'
import { useProductsStore } from '~/stores/products'

const props = defineProps({
  productId: Number,
  disabled: Boolean
})

const cart = useCartStore()
const products = useProductsStore()

const loading = ref(false)
const mounted = ref(false)

onMounted(async () => {
  if (!cart.initialized) {
    await cart.fetchCart()
  }
  mounted.value = true
})

const product = computed(() =>
  products.items.find(p => p.id === props.productId)
)

const isOutOfStock = computed(() =>
  !product.value || product.value.stock <= 0
)

const isInCart = computed(() =>
  cart.items.some(i => i.product === props.productId)
)

const add = async () => {
  if (loading.value || isOutOfStock.value) return

  loading.value = true
  await cart.addToCart(props.productId!, 1)
  loading.value = false
}
</script>

<template>
  <!-- SSR SAFE PLACEHOLDER -->
  <UButton
    v-if="!mounted"
    block
    color="neutral"
    loading
    disabled
  >
    Loading
  </UButton>

  <!-- OUT OF STOCK -->
  <UButton
    v-else-if="isOutOfStock"
    block
    color="neutral"
    disabled
    class="opacity-60 cursor-not-allowed"
  >
    Out of stock
  </UButton>

  <!-- NORMAL -->
  <UButton
    v-else
    block
    :loading="loading"
    :disabled="disabled || isInCart"
    :color="isInCart ? 'myPink' : 'primary'"
    @click="add"
  >
    <span v-if="isInCart">✓ In cart</span>
    <span v-else>Add</span>
  </UButton>
</template>