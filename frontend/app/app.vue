<script setup lang="ts">
console.log('SSR?', process.server)
</script>

<template>
  <UApp>
      <NuxtLayout>
        <NuxtPage />
      </NuxtLayout>

    <AppAuthModal />
    <AppProductPreviewModal />
    <AppImageLightbox />
    <AppCartModal />
  </UApp>
</template>
