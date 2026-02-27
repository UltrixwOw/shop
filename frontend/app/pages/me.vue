<script setup lang="ts">
definePageMeta({ middleware: 'guest' })

const { $api } = useNuxtApp()

const user = ref<any>(null)
const addresses = ref<any[]>([])
const orders = ref<any[]>([])

const loadingOrders = ref(true)
const message = ref('')

const addressForm = reactive({
  id: null,
  full_name: '',
  street: '',
  city: '',
  postal_code: '',
  country: '',
  phone: '',
  is_default: false
})

const editingAddress = ref<number | null>(null)

onMounted(async () => {
  await loadUser()
  await loadAddresses()
  await loadOrders()
})

const loadUser = async () => {
  const res = await $api.get('/users/me/')
  user.value = res.data
}

const loadAddresses = async () => {
  const res = await $api.get('/addresses/')
  addresses.value = res.data
}

const loadOrders = async () => {
  try {
    const res = await $api.get('/orders/')
    orders.value = res.data
  } finally {
    loadingOrders.value = false
  }
}

const startEdit = (addr: any) => {
  editingAddress.value = addr.id
  Object.assign(addressForm, addr)
}

const cancelEdit = () => {
  editingAddress.value = null
  Object.assign(addressForm, {
    id: null,
    full_name: '',
    street: '',
    city: '',
    postal_code: '',
    country: '',
    phone: '',
    is_default: false
  })
}

const saveAddress = async () => {
  if (editingAddress.value) {
    await $api.put(`/addresses/${editingAddress.value}/`, addressForm)
  } else {
    await $api.post('/addresses/', addressForm)
  }

  await loadAddresses()
  cancelEdit()
}

const deleteAddress = async (id: number) => {
  await $api.delete(`/addresses/${id}/`)
  await loadAddresses()
}
</script>

<template>
  <UContainer class="py-12 max-w-4xl">

    <h1 class="text-3xl font-bold mb-8">
      My Profile
    </h1>

    <!-- USER INFO -->
    <UCard class="mb-8">
      <p><strong>Email:</strong> {{ user?.email }}</p>

      <UBadge
        :color="user?.is_verified ? 'primary' : 'error'"
        class="mt-2"
      >
        {{ user?.is_verified ? 'Verified' : 'Not Verified' }}
      </UBadge>
    </UCard>

    <!-- ADDRESSES -->
    <h2 class="text-xl font-semibold mb-4">
      My Addresses
    </h2>

    <div class="grid gap-4 mb-8">
      <UCard
        v-for="addr in addresses"
        :key="addr.id"
      >
        <div class="flex justify-between">

          <div>
            <p class="font-semibold">
              {{ addr.full_name }}
              <UBadge
                v-if="addr.is_default"
                color="primary"
                size="xs"
              >
                Default
              </UBadge>
            </p>

            <p class="text-sm text-gray-500">
              {{ addr.street }}, {{ addr.city }}
            </p>
          </div>

          <div class="flex gap-2">
            <UButton size="xs" variant="soft" @click="startEdit(addr)">
              Edit
            </UButton>

            <UButton size="xs" color="error" variant="ghost"
                     @click="deleteAddress(addr.id)">
              Delete
            </UButton>
          </div>

        </div>
      </UCard>
    </div>

    <!-- ADDRESS FORM -->
    <UCard class="mb-12">
      <template #header>
        {{ editingAddress ? 'Edit Address' : 'Add Address' }}
      </template>

      <div class="grid gap-4">
        <UInput v-model="addressForm.full_name" placeholder="Full name" />
        <UInput v-model="addressForm.street" placeholder="Street" />
        <UInput v-model="addressForm.city" placeholder="City" />
        <UInput v-model="addressForm.postal_code" placeholder="Postal code" />
        <UInput v-model="addressForm.country" placeholder="Country" />
        <UInput v-model="addressForm.phone" placeholder="Phone" />

        <UCheckbox
          v-model="addressForm.is_default"
          label="Set as default"
        />

        <div class="flex gap-3">
          <UButton @click="saveAddress">
            Save
          </UButton>

          <UButton
            variant="ghost"
            @click="cancelEdit"
          >
            Cancel
          </UButton>
        </div>
      </div>
    </UCard>

    <!-- ORDERS -->
    <h2 class="text-xl font-semibold mb-4">
      My Orders
    </h2>

    <UCard v-if="loadingOrders">
      Loading...
    </UCard>

    <div v-else-if="orders.length === 0">
      <UAlert title="No orders yet" />
    </div>

    <div v-else class="space-y-4">
      <UCard
        v-for="order in orders"
        :key="order.uuid"
      >
        <div class="flex justify-between items-center">

          <div>
            <p class="font-mono text-sm">
              {{ order.uuid }}
            </p>

            <p class="text-sm">
              ${{ order.total_price }}
            </p>
          </div>

          <UButton
            size="sm"
            variant="soft"
            :to="`/order-success/${order.uuid}`"
          >
            View
          </UButton>

        </div>
      </UCard>
    </div>

  </UContainer>
</template>