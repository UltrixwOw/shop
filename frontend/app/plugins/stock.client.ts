import { useProductsStore } from '~/stores/products'

export default defineNuxtPlugin(() => {
  const productsStore = useProductsStore()

  const ws = new WebSocket(`ws://127.0.0.1:8000/ws/stock/`)

  ws.onopen = () => {
    console.log('Stock WebSocket connected')
  }

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)

      if (data.product_id && data.stock !== undefined) {
        productsStore.updateStock(data.product_id, data.stock)
      }
    } catch (e) {
      console.error("WS parse error", e)
    }
  }

  ws.onerror = (error) => {
    console.error('WS error', error)
  }

  ws.onclose = () => {
    console.log('Stock WebSocket closed')
  }
})