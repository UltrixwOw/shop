<script setup>
</script>

<template>
  <div>
    <AppHeader />
    
    <UMain>
      <slot />
    </UMain>

    <AppFooter />
  </div>
</template>

<script>
import AppHeader from '~/components/layout/AppHeader.vue'
import AppFooter from '~/components/layout/AppFooter.vue'
</script>