<script setup lang="ts">
definePageMeta({
  middleware: 'guest'
})
import { useAuthStore } from '~/stores/auth'

const auth = useAuthStore()
</script>

<template>
  <div class="container">
    <h1>Мой профиль</h1>

    <div v-if="auth.user">
      <p><strong>ID:</strong> {{ auth.user.id }}</p>
      <p><strong>Email:</strong> {{ auth.user.email }}</p>
      <p><strong>Роль:</strong> {{ auth.user.role }}</p>
    </div>
  </div>
</template>