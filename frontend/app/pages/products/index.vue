<script setup lang="ts">
import { useProductsStore } from '~/stores/products'
import { useCartStore } from '~/stores/cart'
const productsStore = useProductsStore()
const cart = useCartStore()

await productsStore.fetchProducts()

const add = async (id: number) => {
  await cart.addToCart(id, 1)
}
</script>

<template>
  <div class="catalog">
    <div v-for="p in productsStore.items" :key="p.id" class="card">


      <p>{{ p.price }} ₽</p>

      <button @click="add(p.id)">
        В корзину
      </button>
    </div>
  </div>
</template>