<!-- AppLink.vue -->
<script setup lang="ts">
const props = defineProps({
  to: [String, Object]
})

const localePath = useLocalePath()

const resolved = computed(() =>
  typeof props.to === 'string'
    ? localePath(props.to)
    : localePath(props.to)
)
</script>

<template>
  <ULink as="NuxtLink" :to="resolved">
    <slot />
  </ULink>
</template>