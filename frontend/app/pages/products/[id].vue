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
  <UContainer>
    <div v-if="error" class="py-8">
      <h2 class="text-2xl font-semibold text-gray-900">Product not found</h2>
    </div>

    <div v-else-if="product" class="py-8 space-y-8">
      <!-- Заголовок товара -->
      <h1 class="text-3xl font-bold text-gray-900">{{ product.name }}</h1>

      <!-- Галерея изображений -->
      <div v-if="product.images?.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <img
          v-for="(img, index) in product.images"
          :key="index"
          :src="img.image"
          :alt="product.name"
          class="w-full max-w-md rounded-lg shadow-md object-cover"
        />
      </div>

      <!-- Описание -->
      <p class="text-gray-600 leading-relaxed">{{ product.description }}</p>

      <!-- Цена -->
      <h3 class="text-2xl font-bold text-primary">${{ product.price }}</h3>

      <!-- Кнопка добавления в корзину -->
      <AppAddToCartButton :productId="product.id" />

      <!-- Отзывы -->
      <AppProductReviews :productId="product.id" />
    </div>
  </UContainer>
</template>