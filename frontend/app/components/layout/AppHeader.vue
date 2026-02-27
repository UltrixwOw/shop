<!-- components/AppHeader.vue -->
<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
import { useAuthModalStore } from '~/stores/authModal'

const auth = useAuthStore()
const modal = useAuthModalStore()
</script>

<template>
  <UHeader>
    <!-- LEFT -->
    <template #left>
      <NuxtLink to="/" class="text-xl font-bold">
        Shop
      </NuxtLink>
    </template>

    <!-- CENTER (опционально) -->
    <template #center>
      <!-- Можно добавить навигацию -->
    </template>

    <!-- RIGHT -->
    <template #right>
      <div class="flex items-center gap-1">
        <UButton to="/products" variant="ghost">
          Products
        </UButton>

        <AppCartButton />

        <AppLoginButton />

        <UIcon 
          v-if="auth.loading" 
          name="i-heroicons-arrow-path-20-solid" 
          class="animate-spin ml-2" 
        />
      </div>
    </template>
  </UHeader>
</template>