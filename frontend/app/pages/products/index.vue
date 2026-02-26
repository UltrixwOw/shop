<script setup>
const { $api } = useNuxtApp();

const { data: products } = await useAsyncData("products", async () => {
  const res = await $api.get("/shop/products/");
  return res.data;
});
</script>

<template>
  <div class="products-grid">
    <div v-for="product in products" :key="product.id" class="product-card">
      <NuxtLink :to="`/products/${product.id}`">
        <div v-if="product.images?.length">
          <img :src="product.images[0].image" style="max-width: 300px" />
        </div>

        <h3>{{ product.name }}</h3>
        <p>${{ product.price }}</p>
      </NuxtLink>
      <AppAddToCartButton :productId="product.id" />
    </div>
  </div>
</template>

<style scoped>
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

.product-card {
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 8px;
  text-decoration: none;
  color: inherit;
  transition: 0.2s;
  overflow: hidden;
}

.product-card:hover {
  transform: translateY(-3px);
}
</style>
