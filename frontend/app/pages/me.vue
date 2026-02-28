<script setup lang="ts">
definePageMeta({ middleware: 'guest' })

const { $api } = useNuxtApp()

const user = ref<any>(null)
const addresses = ref<any[]>([])
const orders = ref<any[]>([])

const loadingOrders = ref(true)
const message = ref('')

// Пагинация для заказов - по 4 на страницу
const page = ref(1)
const itemsPerPage = ref(4)
const totalOrders = ref(0)

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

// Вычисляемые заказы для текущей страницы
const paginatedOrders = computed(() => {
  if (!orders.value.length) return []
  
  const start = (page.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return orders.value.slice(start, end)
})

// Общее количество страниц
const totalPages = computed(() => {
  return Math.ceil(orders.value.length / itemsPerPage.value)
})

// Следим за изменением страницы
watch(page, () => {
  // При смене страницы прокручиваем к заказам
  document.getElementById('orders-section')?.scrollIntoView({ behavior: 'smooth' })
})

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
    loadingOrders.value = true
    const res = await $api.get('/orders/')
    
    // Если API поддерживает пагинацию
    if (res.data.results) {
      orders.value = res.data.results
      totalOrders.value = res.data.count
    } else {
      // Если API возвращает все заказы сразу
      orders.value = res.data
      totalOrders.value = res.data.length
    }
    
    // Сбрасываем на первую страницу при загрузке новых заказов
    page.value = 1
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
    <h2 id="orders-section" class="text-xl font-semibold mb-4">
      My Orders
    </h2>

    <UCard v-if="loadingOrders">
      <div class="flex justify-center py-8">
        <UIcon name="i-heroicons-arrow-path" class="animate-spin h-6 w-6" />
      </div>
    </UCard>

    <div v-else-if="orders.length === 0">
      <UAlert title="No orders yet" />
    </div>

    <div v-else>
      <!-- Список заказов с пагинацией по 4 -->
      <div class="space-y-4">
        <UCard
          v-for="order in paginatedOrders"
          :key="order.uuid"
        >
          <div class="flex justify-between items-center">

            <div class="space-y-2">
              <p class="font-mono text-sm text-gray-500">
                {{ order.uuid }}
              </p>

              <div class="flex items-center gap-4">
                <p class="font-semibold">
                  ${{ Number(order.total_price).toFixed(2) }}
                </p>

                <UBadge
                  :color="order.status === 'paid' 
                    ? 'success' 
                    : order.status === 'pending' 
                    ? 'warning' 
                    : order.status === 'cancelled'
                    ? 'error'
                    : order.status === 'shipped'
                    ? 'primary'
                    : 'neutral'"
                  size="sm"
                  variant="soft"
                >
                  {{ order.status }}
                </UBadge>

                <p class="text-xs text-gray-400">
                  {{ new Date(order.created_at || order.date).toLocaleDateString() }}
                </p>
              </div>
            </div>

            <UButton
              size="sm"
              variant="soft"
              :to="`/order-success/${order.uuid}`"
            >
              View Details
            </UButton>

          </div>
        </UCard>
      </div>

      <!-- Пагинация -->
      <div v-if="orders.length > itemsPerPage" class="mt-6 flex justify-center">
        <UPagination
          v-model:page="page"
          :items-per-page="itemsPerPage"
          :total="orders.length"
          :sibling-count="1"
          show-edges
          color="neutral"
          variant="outline"
          active-color="primary"
          active-variant="solid"
        />
      </div>
      
      <!-- Информация о количестве заказов -->
      <p v-if="orders.length > 0" class="text-sm text-gray-500 text-center mt-4">
        Showing {{ ((page - 1) * itemsPerPage) + 1 }} 
        to {{ Math.min(page * itemsPerPage, orders.length) }} 
        of {{ orders.length }} orders
      </p>
    </div>

  </UContainer>
</template>