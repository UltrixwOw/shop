<script setup lang="ts">
import { useImgModalStore } from "~/stores/imgModal";

const imgModal = useImgModalStore();
const carousel = useTemplateRef("carousel");

function onSelect(index: number) {
  imgModal.activeIndex = index;
}

function select(index: number) {
  imgModal.activeIndex = index;
  carousel.value?.emblaApi?.scrollTo(index);
}
</script>

<template>
  <UModal
    v-model:open="imgModal.isOpen"
    :title="imgModal.title"
    :description="imgModal.description"
    fullscreen
    :ui="{
      header: 'absolute top-0 left-0 w-full z-10 border-none',
      body: 'overflow-hidden',
    }"
  >
    <template #body>
      <div class="flex flex-col justify-center h-full">
        <!-- Fullscreen Carousel -->
        <UCarousel
          ref="carousel"
          v-slot="{ item }"
          :items="imgModal.images"
          class="w-full"
          :start-index="imgModal.activeIndex"
          @select="onSelect"
        >
          <div class="flex items-center justify-center h-screen">
            <NuxtImg
              :src="item.image"
              width="1000"
              height="600"
              sizes="100vw"
              format="webp"
              quality="95"
              class="max-h-screen object-contain"
              loading="eager"
            />
          </div>
        </UCarousel>

        <!-- Thumbnails -->
        <div class="absolute bottom-6 left-0 right-0 flex justify-center gap-2">
          <div
            v-for="(item, index) in imgModal.images"
            :key="index"
            class="size-16 cursor-pointer opacity-60 transition"
            :class="{ 'opacity-100': imgModal.activeIndex === index }"
            @click="select(index)"
          >
            <NuxtImg
              :src="item.image"
              width="200"
              format="webp"
              quality="80"
              class="w-full h-full object-cover rounded"
              loading="lazy"
            />
          </div>
        </div>
      </div>
    </template>
  </UModal>
</template>
