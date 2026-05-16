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

function next() {
  carousel.value?.emblaApi?.scrollNext();
}

function prev() {
  carousel.value?.emblaApi?.scrollPrev();
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
      body: 'overflow-hidden p-0',
    }"
    class="z-99"
  >
    <template #body>
      <div class="relative flex flex-col justify-center h-full">
        <!-- FULLSCREEN CAROUSEL -->
        <UCarousel
          ref="carousel"
          v-slot="{ item }"
          :items="imgModal.images"
          class="w-full"
          :start-index="imgModal.activeIndex"
          @select="onSelect"
        >
          <div class="flex items-center justify-center h-screen">
            <!-- FULL IMAGE -->
            <img
              :src="item.image"
              :alt="imgModal.title"
              loading="eager"
              class="max-h-full max-w-full object-contain"
            />
          </div>
        </UCarousel>

        <!-- PREV -->
        <UButton
          v-if="imgModal.images.length > 1"
          color="neutral"
          class="w-10 h-10 items-center justify-center absolute left-2 top-1/2 -translate-y-1/2 !bg-black/50 !hover:bg-black/70 text-white rounded-full p-2 z-10 hidden lg:flex"
          @click="prev"
          :disabled="imgModal.activeIndex === 0"
          icon="heroicons:chevron-left"
        />

        <!-- NEXT -->
        <UButton
          v-if="imgModal.images.length > 1"
          color="neutral"
          class="w-10 h-10 items-center justify-center absolute right-2 top-1/2 -translate-y-1/2 !bg-black/50 !hover:bg-black/70 text-white rounded-full p-2 z-10 hidden lg:flex"
          @click="next"
          :disabled="imgModal.activeIndex === imgModal.images.length - 1"
          icon="heroicons:chevron-right"
        />

        <!-- THUMBNAILS -->
        <div
          class="absolute bottom-2 left-0 right-0 flex justify-center gap-2"
        >
          <div
            v-for="(item, index) in imgModal.images"
            :key="index"
            class="size-16 cursor-pointer opacity-60 transition"
            :class="{ 'opacity-100': imgModal.activeIndex === index }"
            @click="select(index)"
          >
            <!-- THUMB -->
            <img
              :src="item.thumbnail || item.image"
              :alt="imgModal.title"
              loading="lazy"
              class="w-full h-full object-cover rounded"
            />
          </div>
        </div>
      </div>
    </template>
  </UModal>
</template>