export const usePayment = () => {
  const { $api } = useNuxtApp()

  const loading = ref(false)
  const error = ref<string | null>(null)

  const pay = async (orderId: number, method: 'paypal' | 'card' | 'crypto') => {
    loading.value = true
    error.value = null

    try {
      const res = await $api.post('/payments/', {
        order_id: orderId,
        payment_method: method,
        idempotency_key: crypto.randomUUID()
      })

      return res.data
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Payment failed'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    pay,
    loading,
    error
  }
}