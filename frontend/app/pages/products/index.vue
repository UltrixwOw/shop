<script setup lang="ts">
import { useProductsStore } from "~/stores/products";
import { useProductPreviewModalStore } from "~/stores/productPreviewModal";

const productsStore = useProductsStore();
const previewModal = useProductPreviewModalStore();

// Состояния загрузки как в wishlist
const loading = ref(true)
const error = ref<string | null>(null)

// Загружаем данные
onMounted(async () => {
  try {
    await productsStore.fetchProducts()
  } catch (err) {
    error.value = 'Failed to load products'
    console.error(err)
  } finally {
    loading.value = false
  }
})

// Для SSR - загружаем данные на сервере
if (import.meta.server) {
  await productsStore.fetchProducts()
}

const openPreview = (product: any) => {
  previewModal.open(product);
};
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 py-10">
    <h1 class="text-3xl font-bold mb-8">{{ $t("products") }}</h1>

    <!-- Состояние загрузки - как в wishlist -->
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <USkeleton v-for="n in 3" :key="n" class="h-96 rounded-lg" />
    </div>

    <!-- Ошибка - как в wishlist -->
    <div v-else-if="error" class="text-red-500 text-center py-10">
      {{ error }}
    </div>

    <!-- Пустой список - как в wishlist -->
    <div
      v-else-if="!productsStore.items.length"
      class="text-gray-500 text-center py-10"
    >
      <UIcon name="i-heroicons-shopping-bag" class="w-16 h-16 mx-auto mb-4 text-gray-300" />
      <p class="text-lg">No products available.</p>
    </div>

    <!-- Products - как в wishlist -->
    <div
      v-else
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
    >
      <UCard
        v-for="product in productsStore.items"
        :key="product.id"
        class="relative flex flex-col justify-between cursor-pointer hover:shadow-lg transition"
        @click="openPreview(product)"
      >
        <!-- Wishlist -->
        <div class="absolute top-2 right-2 z-20" @click.stop>
          <AppAddToWishlistButton :productId="product.id" />
        </div>

        <!-- Image -->
        <div class="aspect-square overflow-hidden rounded-md mb-4">
          <NuxtImg
            v-if="product.images?.length"
            :src="product.images[0].image"
            :srcset="[]"
            :alt="product.name"
            loading="lazy"
            format="webp"
            quality="80"
            sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
            class="w-full h-full object-cover hover:scale-105 transition"
          />

          <NuxtImg
            v-else
            src="/images/productPreview.png"
            :srcset="[]"
            alt="Product placeholder"
            loading="lazy"
            format="webp"
            quality="80"
            class="w-full h-full object-cover hover:scale-105 transition"
          />
        </div>

        <h3 class="text-lg font-semibold mb-2">
          {{ product.name }}
        </h3>

        <div>
          <AppRatingView
            :rating="Number(product.average_rating || 0)"
            :count="product.reviews_count || 0"
          />
        </div>

        <div class="flex justify-between items-center mt-4">
          <AppMoney class="tabular-nums text-primary font-bold text-xl" :value="product.price" />

          <AppAddToCartButton
            :productId="product.id"
            :disabled="product.stock === 0"
            class="relative z-10 w-max"
            @click.stop
          />
        </div>
      </UCard>
    </div>
  </div>
</template>