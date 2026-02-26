<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useCartStore } from "~/stores/cart";
import { useNuxtApp } from "#app";

const cart = useCartStore();
await cart.fetchCart();

const increase = (item) => {
  cart.updateQuantity(item.id, item.quantity + 1);
};

const decrease = (item) => {
  if (item.quantity > 1) {
    cart.updateQuantity(item.id, item.quantity - 1);
  }
};

const remove = (id) => {
  cart.removeFromCart(id);
};

// checkout
const checkoutOrder = async () => {
  try {
    if (cart.isEmpty) {
      return;
    } else {
      navigateTo(`/checkout`);
    }
  } catch (e) {
    console.error(e);
    alert("Ошибка при оформлении заказа");
  }
};
</script>

<template>
  <div>
    <h1>Корзина</h1>

    <div v-for="item in cart.items" :key="item.id" class="cart-item">
      <h4>{{ item.product_name }}</h4>
      <p>${{ item.product_price }}</p>

      <div class="quantity-controls">
        <button @click="decrease(item)">-</button>
        <span>{{ item.quantity }}</span>
        <button @click="increase(item)">+</button>
      </div>

      <button class="remove" @click="remove(item.id)">Remove</button>
    </div>

    <p>Итого: {{ cart.totalPrice }} ₽</p>

    <button :disabled="cart.isEmpty" @click="checkoutOrder">Оформить заказ</button>
  </div>
</template>
