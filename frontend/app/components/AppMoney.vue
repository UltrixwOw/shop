<script setup lang="ts">
const props = defineProps<{
  value: number | string
}>()

const { format } = useMoney()
</script>

<template>
  <span class="tabular-nums text-primary font-bold text-xl">
    {{ format(props.value) }}
  </span>
</template>