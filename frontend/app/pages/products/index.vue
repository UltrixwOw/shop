<script setup lang="ts">
import { useProductPreviewModalStore } from '~/stores/productPreviewModal'

const previewModal = useProductPreviewModalStore()
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
  <div class="max-w-7xl mx-auto px-4 py-10">

    <!-- Заголовок -->
    <h1 class="text-3xl font-bold mb-8">
      Products
    </h1>

    <!-- Ошибка -->
    <div v-if="error">
      <UAlert
        color="error"
        variant="soft"
        title="Ошибка загрузки продуктов"
      />
    </div>

    <!-- Загрузка -->
    <div
      v-else-if="pending"
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
    >
      <USkeleton
        v-for="n in 6"
        :key="n"
        class="h-72 rounded-xl"
      />
    </div>

    <!-- Сетка продуктов -->
    <div
      v-else
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
    >
      <UCard
        v-for="product in products"
        :key="product.id"
        class="flex flex-col justify-between"
      >
        <!-- Картинка -->
        <div
          v-if="product.images?.length"
          class="aspect-square overflow-hidden rounded-lg mb-4"
        >
          <img
            :src="product.images[0].image"
            class="w-full h-full object-cover hover:scale-105 transition"
          />
        </div>

        <!-- Название -->
        <h3 class="text-lg font-semibold mb-2">
          {{ product.name }}
        </h3>

        <!-- Цена -->
        <p class="text-primary font-bold text-xl mb-4">
          ${{ product.price }}
        </p>

        <!-- Кнопки -->
        <div class="flex flex-col gap-2 mt-auto">

          <!-- Preview -->
          <UButton
            variant="soft"
            block
            @click="previewModal.open(product)"
          >
            Quick preview
          </UButton>

          <!-- Add to cart -->
          <AppAddToCartButton
            :productId="product.id"
          />

        </div>
      </UCard>
    </div>

  </div>
</template>