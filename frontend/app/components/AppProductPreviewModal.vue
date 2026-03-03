<script setup lang="ts">
import { useProductPreviewModalStore } from "~/stores/productPreviewModal";

const modal = useProductPreviewModalStore();

const carousel = useTemplateRef("carousel");
const activeIndex = ref(0);

function onClickPrev() {
  activeIndex.value--;
}

function onClickNext() {
  activeIndex.value++;
}

function onSelect(index: number) {
  activeIndex.value = index;
}

function select(index: number) {
  activeIndex.value = index;
  carousel.value?.emblaApi?.scrollTo(index);
}
</script>

<template>
  <UModal
    v-model:open="modal.isOpen"
    :title="modal.product?.name"
    :description="modal.product?.description"
    :close="{
      icon: 'i-heroicons-x-mark-20-solid',
      color: 'neutral',
      variant: 'ghost',
    }"
    class="max-w-3xl"
  >
    <template #body>
      <div v-if="modal.product" >
        <!-- 🔥 Main Image Area (как в products.vue) -->
        <div class="aspect-square overflow-hidden rounded-lg">
          <UCarousel
            v-if="modal.product.images?.length"
            ref="carousel"
            v-slot="{ item }"
            arrows
            :items="modal.product.images"
            :prev="{ onClick: onClickPrev }"
            :next="{ onClick: onClickNext }"
            class="w-full "
            @select="onSelect"
          >
            <NuxtImg
              :src="item.image"
              :alt="modal.product.name"
              loading="lazy"
              format="webp"
              quality="90"
              sizes="100vw"
              class="w-full  object-cover rounded-lg"
            />
          </UCarousel>

          <!-- Fallback -->
          <NuxtImg
            v-else
            src="/images/productPreview.png"
            alt="Product placeholder"
            loading="lazy"
            format="webp"
            quality="80"
            class="w-full  object-cover rounded-lg"
          />
        </div>

        <!-- 🔥 Thumbnails -->
        <div v-if="modal.product.images?.length > 1" class="flex gap-2 justify-center">
          <div
            v-for="(item, index) in modal.product.images"
            :key="item.id || index"
            class="size-16 overflow-hidden rounded-md cursor-pointer transition-opacity"
            :class="
              activeIndex === index ? 'opacity-100' : 'opacity-40 hover:opacity-100'
            "
            @click="select(index)"
          >
            <NuxtImg
              :src="item.image"
              :alt="modal.product.name"
              loading="lazy"
              format="webp"
              quality="70"
              class="w-full h-full object-cover"
            />
          </div>
        </div>

      </div>
    </template>
    <template #footer>
    <div class="space-y-2 w-full">
      <p class="text-lg font-semibold text-primary">${{ modal.product.price }}</p>

      <AppAddToCartButton :productId="modal.product.id" />
    </div>
      
    </template>
  </UModal>
</template>
