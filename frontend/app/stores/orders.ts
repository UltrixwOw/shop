import { defineStore } from 'pinia'

interface Order {
  uuid: string
  status: string
  total_price: string
  created_at: string
}

export const useOrdersStore = defineStore('orders', () => {
  const orders = ref<Order[]>([])
  const loading = ref(false)

  const fetchOrders = async () => {
    const { $api } = useNuxtApp()   // ✅ ОБЯЗАТЕЛЬНО внутри функции

    loading.value = true
    try {
      const res = await $api.get('/orders/')
      orders.value = res.data
    } finally {
      loading.value = false
    }
  }

  const $reset = () => {
    orders.value = []
  }

  return {
    orders,
    loading,
    fetchOrders,
    $reset
  }
})