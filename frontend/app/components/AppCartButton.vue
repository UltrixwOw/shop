<script setup lang="ts">
import { useCartModalStore } from "~/stores/cartModal";
import { useCartStore } from "~/stores/cart";

const modal = useCartModalStore();
const cart = useCartStore();

// Простое решение для гидратации
const mounted = ref(false);

onMounted(() => {
  mounted.value = true;
});
</script>

<template>
  <UChip
    :show="mounted && cart.items.length > 0"
    position="my-bottom-left"
    color="myPink"
  >
    <UButton icon="i-heroicons-shopping-bag" variant="ghost" @click="modal.open()" />
  </UChip>
</template>
