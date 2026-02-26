<script setup lang="ts">
const route = useRoute();
const { $api } = useNuxtApp();
const { pay, loading } = usePayment();

const order = ref(null);
const error = ref(null);
const paymentLoading = ref(false);

const fetchOrder = async () => {
  const res = await $api.get(`/orders/by-uuid/${route.params.uuid}/`);
  order.value = res.data;
};

const handlePayment = async (method: "paypal" | "card" | "crypto") => {
  try {
    paymentLoading.value = true;

    await pay(order.value.id, method);

    await fetchOrder(); // обновить статус
  } catch (e) {
    console.error(e);
  } finally {
    paymentLoading.value = false;
  }
};

onMounted(async () => {
  try {
    const res = await $api.get(`/orders/${route.params.uuid}/`);
    order.value = res.data;
  } catch (e) {
    error.value = true;
  }
});
onMounted(fetchOrder)
</script>

<template>
  <div v-if="error">Failed to load order</div>

  <div v-else-if="order">
    <h1>Order successful 🎉</h1>
    <p>Order UUID: {{ order.uuid }}</p>
    <p>Status: {{ order.status }}</p>
    <p>Total: {{ order.total_price }}</p>

    <ul>
      <li v-for="item in order.items" :key="item.product_name">
        {{ item.product_name }} × {{ item.quantity }}
      </li>
    </ul>
  </div>
  <div v-if="order?.status === 'pending'" class="payment-box">
    <h3>Оплатить заказ</h3>

    <button @click="handlePayment('card')" :disabled="paymentLoading">
      💳 Оплатить картой
    </button>

    <button @click="handlePayment('paypal')" :disabled="paymentLoading">🅿 PayPal</button>

    <button @click="handlePayment('crypto')" :disabled="paymentLoading">₿ Crypto</button>
  </div>
</template>
