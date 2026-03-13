<script setup lang="ts">
const props = defineProps<{
  value: number | string
}>()

const { format } = useMoney()
</script>

<template>
  <span>
    {{ format(props.value) }}
  </span>
</template>