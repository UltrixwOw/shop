<script setup lang="ts">
import { useProductsStore } from "~/stores/products";
import { useProductPreviewModalStore } from "~/stores/productPreviewModal";

const productsStore = useProductsStore();
const previewModal = useProductPreviewModalStore();

const loading = ref(true);
const error = ref<string | null>(null);

// =============================
// LOAD PRODUCTS
// =============================

onMounted(async () => {
  try {
    await productsStore.fetchProducts();
  } catch (err) {
    error.value = "Failed to load products";
    console.error(err);
  } finally {
    loading.value = false;
  }
});

// SSR
if (import.meta.server) {
  await productsStore.fetchProducts();
}

// =============================
// OPEN PREVIEW
// =============================

const openPreview = async (product: any) => {
  await previewModal.open(product.id, product);
};
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 py-10">
    <h1 class="text-3xl font-bold mb-8">
      {{ $t("products") }}
    </h1>

    <!-- LOADING -->
    <div v-if="loading" class="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
      <USkeleton v-for="n in 6" :key="n" class="h-96 rounded-lg" />
    </div>

    <!-- ERROR -->
    <div v-else-if="error" class="text-red-500 text-center py-10">
      {{ error }}
    </div>

    <!-- EMPTY -->
    <div v-else-if="!productsStore.items.length" class="text-gray-500 text-center py-10">
      <UIcon
        name="i-heroicons-shopping-bag"
        class="w-16 h-16 mx-auto mb-4 text-gray-300"
      />

      <p class="text-lg">No products available.</p>
    </div>

    <!-- PRODUCTS -->
    <div v-else class="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
      <UCard
        v-for="product in productsStore.items"
        :key="product.id"
        class="relative flex flex-col justify-between cursor-pointer hover:shadow-lg transition"
        :ui="{
          body: 'p-2 md:p-4',
          base: 'overflow-hidden h-full',
        }"
        @click="openPreview(product)"
      >
        <!-- WISHLIST -->
        <div class="absolute top-2 right-2 z-20" @click.stop>
          <AppAddToWishlistButton :productId="product.id" />
        </div>

        <!-- IMAGE -->
        <div class="aspect-square overflow-hidden rounded-md mb-4">
          <img
            v-if="product.images?.length"
            :src="product.images[0].thumbnail || product.images[0].image"
            :alt="product.name"
            loading="lazy"
            class="w-full h-full object-cover hover:scale-105 transition"
          />

          <NuxtImg
            v-else
            src="/images/productPreview.png"
            alt="Product placeholder"
            loading="lazy"
            class="w-full h-full object-cover hover:scale-105 transition"
          />
        </div>

        <!-- TITLE -->
        <h3 class="text-lg font-semibold mb-2">
          {{ product.name }}
        </h3>

        <!-- RATING -->
        <div>
          <AppRatingView
            :rating="Number(product.average_rating || 0)"
            :count="product.reviews_count || 0"
          />
        </div>

        <!-- FOOTER -->
        <div class="flex justify-between items-center mt-4">
          <AppMoney
            class="tabular-nums text-primary font-bold text-xl"
            :value="product.price"
          />

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
