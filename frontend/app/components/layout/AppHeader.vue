<script setup>
// Явный импорт для надежности (хотя auto-import должен работать)
import { useAuthStore } from '~/stores/auth'

const auth = useAuthStore()
</script>

<template>
  <header class="header">
    <NuxtLink to="/">Shop</NuxtLink>

    <nav>
      <NuxtLink to="/products">Products</NuxtLink>
      <NuxtLink to="/cart">Cart</NuxtLink>
      <NuxtLink to="/me">Me</NuxtLink>
      
      <AppLoginButton />
    </nav>
    
    <!-- Индикатор загрузки (опционально) -->
    <span v-if="auth.loading" class="loading">...</span>
  </header>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

nav {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.loading {
  color: #6c757d;
  margin-left: 1rem;
}

button {
  background: none;
  border: 1px solid #dc3545;
  color: #dc3545;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background: #dc3545;
  color: white;
}
</style>