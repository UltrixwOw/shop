<script setup lang="ts">
import { useProductsStore } from '~/stores/products'
import { useProductPreviewModalStore } from '~/stores/productPreviewModal'

const productsStore = useProductsStore()
const previewModal = useProductPreviewModalStore()

const { data: products, pending } = await useAsyncData(
  'products',
  () => productsStore.fetchProducts()
)

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

    <!-- Skeleton -->
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

    <!-- Products -->
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

        <!-- Image -->
        <div class="aspect-square overflow-hidden rounded-md mb-4">
          
          <NuxtImg
            v-if="product.images?.length"
            :src="product.images[0].image"
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

        <p class="text-primary font-bold text-xl mb-2">
          ${{ product.price }}
        </p>

        <AppAddToCartButton
          :productId="product.id"
          :disabled="product.stock === 0"
          class="relative z-10"
          @click.stop
        />

      </UCard>
    </div>

  </div>
</template>