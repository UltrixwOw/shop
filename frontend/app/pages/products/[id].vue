<script setup>
const route = useRoute()
const { $api } = useNuxtApp()

const id = computed(() => route.params.id)

const { data: product, error } = await useAsyncData(
  `product-${id.value}`,
  async () => {
    const res = await $api.get(`/shop/products/${id.value}/`)
    return res.data
  }
)
</script>

<template>
  <div v-if="error">
    <h2>Product not found</h2>
  </div>

  <div v-else-if="product">
    <h1>{{ product.name }}</h1>

    <div v-if="product.images?.length">
      <img
        v-for="img in product.images"
        :key="img.image"
        :src="img.image"
        style="max-width: 300px;"
      />
    </div>

    <p>{{ product.description }}</p>

    <h3>${{ product.price }}</h3>

    <AppAddToCartButton :productId="product.id" />
  </div>
</template>