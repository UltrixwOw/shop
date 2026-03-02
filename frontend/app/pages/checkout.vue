<script setup lang="ts">
import { useCartStore } from "~/stores/cart";

const { $api } = useNuxtApp();
const router = useRouter();
const cart = useCartStore();

await cart.fetchCart();

const selectedAddress = ref<number | null>(null);
const loading = ref(false);

const { data: addresses } = await useAsyncData("addresses", async () => {
  const res = await $api.get("/addresses/");
  return res.data;
});

const newAddress = reactive({
  full_name: '',
  street: '',
  city: '',
  postal_code: '',
  country: '',
  phone: '',
  is_default: false
})

const createAddress = async () => {
  const res = await $api.post('/addresses/', newAddress)
  addresses.value.push(res.data)
  selectedAddress.value = res.data.id
}

watch(
  addresses,
  (val) => {
    if (!val?.length) return;

    const defaultAddr = val.find((a) => a.is_default);
    selectedAddress.value = defaultAddr ? defaultAddr.id : val[0].id;
  },
  { immediate: true }
);

const submitOrder = async () => {
  if (!selectedAddress.value) return;

  try {
    loading.value = true;

    const res = await $api.post("/orders/checkout/", {
      address_id: selectedAddress.value,
    });

    const uuid = res.data?.order_uuid;
    if (!uuid) throw new Error("Order UUID missing");

    await cart.fetchCart();
    router.push(`/order-success/${uuid}`);
  } catch (e: any) {
    console.error(e.response?.data || e.message);
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <UContainer class="py-12 max-w-3xl">
    <h1 class="text-3xl font-bold mb-8">Checkout</h1>

    <!-- SUMMARY -->
    <UCard class="mb-8">
      <template #header> Order Summary </template>

      <div v-for="item in cart.items" :key="item.id" class="flex justify-between py-2">
        <span> {{ item.product_name }} × {{ item.quantity }} </span>

        <span> ${{ (item.price * item.quantity).toFixed(2) }} </span>
      </div>

      <div class="flex justify-between pt-4 border-t font-semibold text-lg">
        <span>Total:</span>
        <span>${{ cart.totalPrice.toFixed(2) }}</span>
      </div>
    </UCard>

    <!-- ADDRESS -->
    <UCard v-if="addresses?.length">
      <template #header> Select Address </template>

      <URadioGroup
        v-model="selectedAddress"
        :items="
          addresses.map((a) => ({
            label: `${a.full_name} — ${a.street}, ${a.city}`,
            value: a.id,
          }))
        "
      />
    </UCard>

    <UAlert v-else color="error" variant="soft" title="No addresses found" class="my-6" />

    <UCard class="mt-6">
      <template #header> Add New Address </template>

      <div class="grid gap-4">
        <UInput v-model="newAddress.full_name" placeholder="Full name" />
        <UInput v-model="newAddress.street" placeholder="Street" />
        <UInput v-model="newAddress.city" placeholder="City" />
        <UInput v-model="newAddress.postal_code" placeholder="Postal code" />
        <UInput v-model="newAddress.country" placeholder="Country" />
        <UInput v-model="newAddress.phone" placeholder="Phone" />

        <UButton @click="createAddress"> Save Address </UButton>
      </div>
    </UCard>

    <!-- BUTTON -->
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
