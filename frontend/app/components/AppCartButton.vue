<script setup lang="ts">
import { useCartModalStore } from '~/stores/cartModal'
import { useCartStore } from '~/stores/cart'

const modal = useCartModalStore()
const cart = useCartStore()
</script>

<template>
  <UButton
    icon="i-heroicons-shopping-cart"
    variant="ghost"
    :badge="cart.items.length"
    @click="modal.open()"
  />
</template>