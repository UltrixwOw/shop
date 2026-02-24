<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useCartStore } from '~/stores/cart'
import { useNuxtApp } from '#app'

const cart = useCartStore()
await cart.fetchCart()

// checkout
const checkoutOrder = async () => {
  try {
    navigateTo(`/checkout`)
  } catch (e) {
    console.error(e)
    alert("Ошибка при оформлении заказа")
  }
}
</script>

<template>
  <div>
    <h1>Корзина</h1>

    <div v-for="item in cart.items" :key="item.id">
      {{ item.product_name }} x {{ item.quantity }} — {{ item.product_price }} ₽
    </div>

    <p>Итого: {{ cart.totalPrice }} ₽</p>

    <button :disabled="cart.isEmpty" @click="checkoutOrder">
      Оформить заказ
    </button>
  </div>
</template>