<!-- components/AppHeader.vue -->
<script setup lang="ts">
import { useAuthStore } from "~/stores/auth";
import { useAuthModalStore } from "~/stores/authModal";

const auth = useAuthStore();
const modal = useAuthModalStore();

const localePath = useLocalePath()

const mobileNavItems = [
  { label: 'Products', to: '/products' },
  { label: 'About us', to: '/about' },
];
</script>

<template>
  <UHeader>
    <template #left>
      <NuxtLink :to="localePath('/')">
        <div class="appLogo-box">
          <AppLogo />
          <h1 class="title-meloni text-2xl font-bold italic tracking-tight" color="pink-300">
            Meloni
          </h1>
        </div>
      </NuxtLink>
    </template>
    <!-- LEFT -->


    <!-- CENTER (опционально) -->
    <div class="menu-box">
      <AppLink to="/products" variant="ghost">{{ $t('products') }}</AppLink>
      <AppLink to="/about" variant="ghost">{{ $t('about_us') }}</AppLink>
    </div>

    <!-- RIGHT -->
    <template #right>
      <div class="flex items-center gap-1">
        <AppWishlistButton />
        
        <AppCartButton />

        <AppLoginButton />

        <UIcon
          v-if="auth.loading"
          name="i-heroicons-arrow-path-20-solid"
          class="animate-spin ml-2"
        />
      </div>
    </template>

    <template #body>
      <div class="flex flex-col gap-4 py-4">
        <!-- Ваши кнопки/ссылки для мобильной версии -->
        <AppLink
          v-for="item in mobileNavItems"
          :key="item.to"
          :to="item.to"
          class="px-4 py-2 text-lg hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg"
          active-class="text-primary font-medium"
        >
          {{ item.label }}
        </AppLink>
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