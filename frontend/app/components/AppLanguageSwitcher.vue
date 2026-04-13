<script setup lang="ts">
const { locales, locale, setLocale } = useI18n();

const items = computed(() =>
  locales.value.map((l) => {
    const code = typeof l === "string" ? l : l.code;
    return code;
  })
);
</script>

<template>
  <USelectMenu :model-value="locale" :items="items" @update:model-value="setLocale" />
</template>
