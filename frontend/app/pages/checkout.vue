<script setup>
import { useCartStore } from '~/stores/cart'

const { $api } = useNuxtApp()
const router = useRouter()
const cartStore = useCartStore()

// ✅ ВАЖНО — объявляем
const selectedAddress = ref(null)

const { data: addresses } = await useAsyncData('addresses', async () => {
  const res = await $api.get('/addresses/')
  return res.data
})

const loading = ref(false)

const submitOrder = async () => {
  if (!selectedAddress.value) {
    alert('Select address')
    return
  }

  try {
    loading.value = true

    const res = await $api.post('/orders/checkout/', {
      address_id: selectedAddress.value,
    })

    const uuid = res.data?.order_uuid

    if (!uuid) {
      throw new Error('Order UUID missing')
    }

    await cartStore.fetchCart()

    router.push(`/order-success/${uuid}`)

  } catch (e) {
    console.error(e.response?.data || e.message)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div>
    <h1>Checkout</h1>

    <!-- Выбор адреса -->
    <div v-if="addresses?.length">
      <h3>Select address</h3>

      <div
        v-for="address in addresses"
        :key="address.id"
      >
        <input
          type="radio"
          :value="address.id"
          v-model="selectedAddress"
        />
        {{ address.full_name }} —
        {{ address.street }},
        {{ address.city }}
      </div>
    </div>

    <button
      @click="submitOrder"
      :disabled="loading"
    >
      {{ loading ? 'Processing...' : 'Place order' }}
    </button>
  </div>
</template>