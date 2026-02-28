<!-- components/AppHeader.vue -->
<script setup lang="ts">
import { useAuthStore } from "~/stores/auth";
import { useAuthModalStore } from "~/stores/authModal";

const auth = useAuthStore();
const modal = useAuthModalStore();
</script>

<template>
  <UHeader>
    <template #title>
    <div class="appLogo-box">
      <AppLogo />
      <h1 class="text-2xl font-bold italic tracking-tight" color="pink-300">
        Meloni
      </h1>
    </div>
      
    </template>
    <!-- LEFT -->


    <!-- CENTER (опционально) -->
    <div class="menu-box">
      <ULink to="/products" variant="ghost"> Products </ULink>
      <ULink to="/about" variant="ghost"> About us </ULink>
    </div>

    <!-- RIGHT -->
    <template #right>
      <div class="flex items-center gap-1">
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

<style scoped>
  .appLogo-box {
    display: flex;
    align-items: center;
  }
  .appLogo-box h1 {
    margin-left: 8px;
  }
  .menu-box a {
    margin: 0 8px;
  }
</style>