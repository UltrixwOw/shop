<script setup lang="ts">
import { useProductPreviewModalStore } from '~/stores/productPreviewModal'

const modal = useProductPreviewModalStore()
</script>

<template>
  <UModal
    v-model:open="modal.isOpen"
    :title="modal.product?.name"
    :description="modal.product?.description"
    :close="{
      icon: 'i-heroicons-x-mark-20-solid',
      color: 'neutral',
      variant: 'ghost'
    }"
    class="max-w-2xl"
  >
    <template #body>
      <div v-if="modal.product" class="space-y-4">

        <img
          v-if="modal.product.images?.length"
          :src="modal.product.images[0].image"
          class="w-full rounded-lg object-cover"
        />

        <p class="text-lg font-semibold text-primary">
          ${{ modal.product.price }}
        </p>

        <AppAddToCartButton :productId="modal.product.id" />

      </div>
    </template>
  </UModal>
</template>