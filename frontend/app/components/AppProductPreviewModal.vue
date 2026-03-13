<script setup lang="ts">
import { useProductPreviewModalStore } from "~/stores/productPreviewModal";
import { useImgModalStore } from "~/stores/imgModal";
import { computed } from "vue";

const modal = useProductPreviewModalStore();
const imgModal = useImgModalStore();

// Вычисляемый массив для карусели
const carouselItems = computed(() => {
  if (modal.product?.images?.length) {
    return modal.product.images;
  }
  // Возвращаем массив объектов для совместимости
  return [{ image: "/images/productPreview.png", isPlaceholder: true }];
});

function openLightbox(index: number) {
  // Не открываем лайтбокс для плейсхолдера
  if (carouselItems.value[index]?.isPlaceholder) return;

  imgModal.open(
    modal.product.images,
    index,
    modal.product.name,
    modal.product.description
  );
}
</script>

<template>
  <UModal
    v-model:open="modal.isOpen"
    :title="modal.product?.name"
    :description="modal.product?.description"
    :close-on-escape="true"
    :dismissible="true"
    :ui="{ content: 'focus:outline-none' }"
    class="max-w-4xl"
  >
    <template #body>
      <div v-if="modal.product" class="space-y-6">
        <!-- Единая карусель -->
        <UCarousel :items="carouselItems" :ui="{ item: 'basis-1/3' }" class="w-full">
          <template #default="{ item, index }">
            <div
              class="aspect-square overflow-hidden rounded-lg"
              :class="{ 'cursor-pointer': !item.isPlaceholder }"
              @click="!item.isPlaceholder ? openLightbox(index) : null"
            >
              <NuxtImg
                :src="item.image"
                :alt="modal.product.name"
                format="webp"
                quality="80"
                class="w-full h-full object-cover"
                loading="lazy"
              />
            </div>
          </template>
        </UCarousel>
        <div>
          <AppProductReviews :productId="modal.product.id" />
        </div>

        <USeparator />

        <div class="flex justify-between">
          <AppMoney class="tabular-nums text-primary font-bold text-xl" :value="modal.product.price" />

          <AppAddToCartButton :productId="modal.product.id" class="relative z-10 w-max" />
        </div>
      </div>
    </template>
  </UModal>
</template>
