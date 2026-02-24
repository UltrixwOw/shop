<script setup>
const route = useRoute()
const api = useApi()

const product = await api(`/shop/products/${route.params.id}/`)
</script>

<template>
  <div>
    <h1>{{ product.name }}</h1>
    <p>{{ product.description }}</p>
    <button @click="addToCart">Add to cart</button>
  </div>
</template>