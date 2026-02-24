<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useCartStore } from '~/stores/cart'
import { useNuxtApp } from '#app'

const cart = useCartStore()
await cart.fetchCart()

const { $api } = useNuxtApp()

// адреса пользователя
const addresses = ref<any[]>([])
const selectedAddressId = ref<number | null>(null)

// форма нового адреса
const newAddress = reactive({
  full_name: '',
  street: '',
  city: '',
  postal_code: '',
  country: '',
  phone: '',
  is_default: false
})

const loading = ref(false)

// грузим адреса пользователя
onMounted(async () => {
  try {
    const res = await $api.get('/addresses/')
    addresses.value = res.data
    if (addresses.value.length) selectedAddressId.value = addresses.value[0].id
  } catch (e) {
    console.error("Failed to fetch addresses", e)
  }
})

// создаём новый адрес
const addAddress = async () => {
  try {
    const res = await $api.post('/addresses/', newAddress)
    addresses.value.push(res.data)
    selectedAddressId.value = res.data.id
  } catch (e) {
    console.error("Failed to add address", e)
    alert("Ошибка при добавлении адреса")
  }
}

// checkout
const checkoutOrder = async () => {
  if (!selectedAddressId.value) {
    alert('Выберите адрес доставки или создайте новый')
    return
  }

  try {
    loading.value = true
    const data = await cart.checkout(selectedAddressId.value)
    navigateTo(`/order-success/${data.order_uuid}`)
  } catch (e) {
    console.error(e)
    alert("Ошибка при оформлении заказа")
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div>
    <h1>Checkout</h1>

    <h2>Корзина</h2>
    <div v-for="item in cart.items" :key="item.id">
      {{ item.product_name }} x {{ item.quantity }} — {{ item.product_price }} ₽
    </div>
    <p>Итого: {{ cart.totalPrice }} ₽</p>

    <h2>Выберите существующий адрес</h2>
    <div v-if="addresses.length">
      <select v-model="selectedAddressId">
        <option v-for="a in addresses" :key="a.id" :value="a.id">
          {{ a.full_name }}, {{ a.street }}, {{ a.city }}, {{ a.postal_code }}, {{ a.country }}, {{ a.phone }}
        </option>
      </select>
    </div>

    <h2>Или добавьте новый адрес</h2>
    <div>
      <input v-model="newAddress.full_name" placeholder="Full name" />
      <input v-model="newAddress.street" placeholder="Street" />
      <input v-model="newAddress.city" placeholder="City" />
      <input v-model="newAddress.postal_code" placeholder="Postal code" />
      <input v-model="newAddress.country" placeholder="Country" />
      <input v-model="newAddress.phone" placeholder="Phone" />
      <label>
        <input type="checkbox" v-model="newAddress.is_default" /> Is default
      </label>
      <button @click="addAddress">Добавить адрес</button>
    </div>

    <button :disabled="cart.isEmpty || loading" @click="checkoutOrder">
      Оформить заказ
    </button>
  </div>
</template>