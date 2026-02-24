<script setup lang="ts">

const { $api } = useNuxtApp()

const { data: products, pending, error } = await useAsyncData(
  'products',
  async () => {
    const res = await $api.get('/shop/products/')
    return res.data
  }
)
</script>

<template>
  <div>
    <h1>Products</h1>

    <div v-if="pending">Loading...</div>
    <div v-else-if="error">Error loading products</div>

    <div v-else>
      <div v-for="product in products" :key="product.id">
        <h3>{{ product.name }}</h3>
        <p>{{ product.price }} $</p>
      </div>
    </div>
  </div>
</template>