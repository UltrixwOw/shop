<script setup lang="ts">
import { useCartStore } from '~/stores/cart'

const { $api } = useNuxtApp()
const router = useRouter()
const cart = useCartStore()

await cart.fetchCart()

const selectedAddress = ref<number | null>(null)
const loading = ref(false)

const { data: addresses } = await useAsyncData('addresses', async () => {
  const res = await $api.get('/addresses/')
  return res.data
})

/**
 * 🔥 Автовыбор default адреса
 */
watch(
  addresses,
  (val) => {
    if (!val?.length) return

    const defaultAddr = val.find(a => a.is_default)
    selectedAddress.value = defaultAddr
      ? defaultAddr.id
      : val[0].id
  },
  { immediate: true }
)

const submitOrder = async () => {
  if (!selectedAddress.value) return

  try {
    loading.value = true

    const res = await $api.post('/orders/checkout/', {
      address_id: selectedAddress.value
    })

    const uuid = res.data?.order_uuid
    if (!uuid) throw new Error('Order UUID missing')

    await cart.fetchCart()

    router.push(`/order-success/${uuid}`)
  } catch (e: any) {
    console.error(e.response?.data || e.message)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <UContainer class="py-12 max-w-3xl">

    <h1 class="text-3xl font-bold mb-8">
      Checkout
    </h1>

    <!-- CART SUMMARY -->
    <UCard class="mb-8">
      <template #header>
        Order Summary
      </template>

      <div v-for="item in cart.items" :key="item.id"
           class="flex justify-between py-2">

        <span>
          {{ item.product_name }} × {{ item.quantity }}
        </span>

        <span>
          ${{ Number(item.product_price) * item.quantity }}
        </span>
      </div>

      <div class="flex justify-between pt-4 border-t font-semibold text-lg">
        <span>Total:</span>
        <span>${{ cart.totalPrice }}</span>
      </div>
    </UCard>

    <!-- ADDRESS SELECTION -->
    <UCard v-if="addresses?.length">
      <template #header>
        Select Address
      </template>

      <URadioGroup
        v-model="selectedAddress"
        :items="addresses.map(a => ({
          label: `${a.full_name} — ${a.street}, ${a.city}`,
          value: a.id
        }))"
      />
    </UCard>

    <UAlert
      v-else
      color="error"
      variant="soft"
      title="No addresses found"
      class="my-6"
    />

    <!-- SUBMIT -->
    <UButton
      block
      size="lg"
      class="mt-8"
      :loading="loading"
      :disabled="cart.isEmpty || !selectedAddress"
      @click="submitOrder"
    >
      Place Order
    </UButton>

  </UContainer>
</template>