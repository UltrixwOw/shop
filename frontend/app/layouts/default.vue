<script setup>
</script>

<template>
  <div>
    <AppHeader />
    
    <main class="container">
      <slot />
    </main>

    <AppFooter />
  </div>
</template>

<script>
import AppHeader from '~/components/layout/AppHeader.vue'
import AppFooter from '~/components/layout/AppFooter.vue'
</script>