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

// Проверяем, добавляется ли этот товар прямо сейчас
const isPending = computed(() =>
  cart.pendingAdds.has(props.productId!)
)

// Кнопка должна быть disabled если:
// - disabled из props
// - товар уже в корзине
// - товар сейчас добавляется
// - товара нет в наличии
const isButtonDisabled = computed(() =>
  props.disabled || isInCart.value || isPending.value || isOutOfStock.value
)

const add = async () => {
  if (isButtonDisabled.value) return

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
  />
    
  <!-- OUT OF STOCK -->
  <UButton
    v-else-if="isOutOfStock"
    block
    color="neutral"
    disabled
    class="opacity-60 cursor-not-allowed"
  >
    {{ $t('out_of_stock') }}
  </UButton>

  <!-- IN CART (уже в корзине) -->
  <UButton
    v-else-if="isInCart"
    block
    color="myPink"
    disabled
    class="flex-row-reverse"
  >
    ✓ {{ $t('in_cart') }}
  </UButton>

  <!-- NORMAL / PENDING -->
  <UButton
    v-else
    block
    :loading="loading || isPending"
    :disabled="isButtonDisabled"
    color="primary"
    icon="i-heroicons-shopping-bag"
    class="flex-row-reverse"
    @click="add"
  >
    <span v-if="isPending">{{ $t('adding') }}...</span>
    <span v-else>{{ $t('add') }}</span>
  </UButton>
</template>