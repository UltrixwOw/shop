<template>
  <div>
    <NuxtRouteAnnouncer />
    <NuxtWelcome />
    <pre>{{ products }}</pre>
  </div>
</template>

<script setup>
// useAsyncData или useFetch автоматически выполняются на сервере
const config = useRuntimeConfig();

// Лучший способ для Nuxt - useFetch
const { data: products, error } = await useFetch(`${config.public.apiBase}/shop/products/`, {
  // Опции запроса
  server: true, // выполнять на сервере (по умолчанию true)
  lazy: false, // ждать завершения
});
</script>