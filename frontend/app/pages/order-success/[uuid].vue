<script setup lang="ts">
const route = useRoute()
const { $api } = useNuxtApp()
const { pay } = usePayment()

const order = ref<any>(null)
const error = ref(false)
const paymentLoading = ref(false)

const fetchOrder = async () => {
  const res = await $api.get(`/orders/by-uuid/${route.params.uuid}/`)
  order.value = res.data
}

const handlePayment = async (method: "paypal" | "card" | "crypto") => {
  try {
    paymentLoading.value = true
    await pay(order.value.id, method)
    await fetchOrder()
  } catch (e) {
    console.error(e)
  } finally {
    paymentLoading.value = false
  }
}

onMounted(async () => {
  try {
    await fetchOrder()
  } catch {
    error.value = true
  }
})

// Вспомогательная функция для безопасного получения цены
const getItemPrice = (item: any) => {
  // Проверьте возможные названия поля с ценой
  return item.price || item.unit_price || item.product_price || 0
}

const getItemTotal = (item: any) => {
  const price = Number(getItemPrice(item))
  const quantity = Number(item.quantity) || 1
  return (price * quantity).toFixed(2)
}
</script>

<template>
  <UContainer class="py-16">

    <UAlert
      v-if="error"
      color="error"
      title="Failed to load order"
    />

    <UCard
      v-else-if="order"
      class="max-w-3xl mx-auto p-8 space-y-8"
    >

      <!-- HEADER -->
      <div class="flex justify-between items-start">

        <div>
          <h1 class="text-3xl font-bold mb-2">
            🎉 Заказ создан
          </h1>

          <p class="text-sm text-zinc-500">
            UUID: {{ order.uuid }}
          </p>
        </div>

        <UBadge
          size="lg"
          :color="order.status === 'paid'
            ? 'success'
            : order.status === 'pending'
            ? 'warning'
            : 'neutral'"
          variant="soft"
        >
          {{ order.status }}
        </UBadge>

      </div>

      <USeparator />

      <!-- ITEMS -->
      <div class="space-y-4">

        <div
          v-for="item in order.items"
          :key="item.product_name || item.id"
          class="flex justify-between items-center py-2"
        >
          <div>
            <p class="font-medium">
              {{ item.product_name || item.name }}
            </p>
            <p class="text-sm text-zinc-500">
              × {{ item.quantity }}
              <span v-if="getItemPrice(item)" class="ml-2 text-zinc-400">
                (${{ Number(getItemPrice(item)).toFixed(2) }} each)
              </span>
            </p>
          </div>

          <p class="font-semibold text-lg">
            ${{ getItemTotal(item) }}
          </p>
        </div>

      </div>

      <USeparator />

      <!-- TOTAL -->
      <div class="flex justify-between text-xl font-bold">
        <span>Total:</span>
        <span class="text-primary">
          ${{ Number(order.total_price).toFixed(2) }}
        </span>
      </div>

      <!-- PAYMENT -->
      <div
        v-if="order.status === 'pending'"
        class="pt-6 space-y-4"
      >
        <h3 class="text-lg font-semibold">
          Оплатить заказ
        </h3>

        <div class="flex flex-wrap gap-3">

          <UButton
            icon="i-lucide-credit-card"
            size="lg"
            @click="handlePayment('card')"
            :loading="paymentLoading"
          >
            Оплатить картой
          </UButton>

          <UButton
            icon="i-entypo-social:paypal"
            size="lg"
            color="secondary"
            @click="handlePayment('paypal')"
            :loading="paymentLoading"
          >
            PayPal
          </UButton>

          <UButton
            icon="i-lucide-bitcoin"
            size="lg"
            color="warning"
            @click="handlePayment('crypto')"
            :loading="paymentLoading"
          >
            Crypto
          </UButton>

        </div>
      </div>

    </UCard>

  </UContainer>
</template>