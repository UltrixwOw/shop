<script setup lang="ts">
const props = defineProps<{
  rating: number;
  count: number;
}>();

const fullStars = computed(() => Math.floor(props.rating));
const emptyStars = computed(() => 5 - fullStars.value);
</script>

<template>
  <div class="flex items-center gap-2">
    <div class="flex text-yellow-500 text-lg">
      <span v-for="n in fullStars" :key="'f' + n">★</span>

      <span v-for="n in emptyStars" :key="'e' + n" class="text-gray-300"> ★ </span>
    </div>

    <!-- <div class="text-sm text-gray-500">
      <span class="flex items-center">
        {{ rating.toFixed(1) }} ({{ count }}
        <Icon name="i-heroicons-chat-bubble-bottom-center-text-solid" class="w-4 h-4" />
        )
      </span>
    </div> -->
  </div>
</template>
