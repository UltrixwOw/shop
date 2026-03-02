<script setup lang="ts">
import { useProductsStore } from '~/stores/products'
import { useProductPreviewModalStore } from '~/stores/productPreviewModal'

const productsStore = useProductsStore()
const previewModal = useProductPreviewModalStore()

// ✅ SSR-safe
const { data: products, pending } = await useAsyncData(
  'products',
  () => productsStore.fetchProducts()
)

// синхронизация store (если вдруг SSR)
if (products.value) {
  productsStore.items = products.value
}

const openPreview = (product: any) => {
  previewModal.open(product)
}
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 py-10">

    <h1 class="text-3xl font-bold mb-8">
      Products
    </h1>

    <div
      v-if="pending"
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
    >
      <USkeleton
        v-for="n in 6"
        :key="n"
        class="h-72 rounded-xl"
      />
    </div>

    <div
      v-else
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
    >
      <UCard
        v-for="product in productsStore.items"
        :key="product.id"
        class="flex flex-col justify-between cursor-pointer hover:shadow-lg transition"
        @click="openPreview(product)"
      >

        <div class="aspect-square overflow-hidden rounded-md mb-4">
          <img
            v-if="product.images?.length"
            :src="product.images[0].image"
            class="w-full h-full object-cover hover:scale-105 transition"
          />
          <div v-else class="w-full h-full">
          <img
            src="@/assets/images/productPreview.png"
            class="w-full h-full object-cover hover:scale-105 transition"
          />
          </div>
        </div>

        <h3 class="text-lg font-semibold mb-2">
          {{ product.name }}
        </h3>

        <p class="text-primary font-bold text-xl mb-2">
          ${{ product.price }}
        </p>

        <AppAddToCartButton
          :productId="product.id"
          :disabled="product.stock === 0"
          @click.stop
        />

      </UCard>
    </div>

  </div>
</template>