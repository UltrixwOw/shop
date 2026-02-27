<!-- components/AppLoginButton.vue -->
<script setup lang="ts">
import type { DropdownMenuItem } from '@nuxt/ui'
import { useAuthStore } from "~/stores/auth"
import { useAuthModalStore } from "~/stores/authModal"

const auth = useAuthStore()
const modal = useAuthModalStore()

// Создаем реактивные элементы меню
const dropdownItems = ref<DropdownMenuItem[][]>([
  // Первая группа - информация о пользователе
  [
    {
      label: auth.user?.email || 'Profile',
      icon: 'i-heroicons-user-circle',
      to: '/me',
      type: 'link'
    }
  ],
  // Вторая группа - выход (с красным цветом для опасного действия)
  [
    {
      label: 'Logout',
      icon: 'i-heroicons-arrow-right-on-rectangle',
      color: 'error',
      onSelect: () => auth.logout()
    }
  ]
])

// Обновляем items при изменении пользователя
watch(() => auth.user, () => {
  if (dropdownItems.value[0]?.[0]) {
    dropdownItems.value[0][0].label = auth.user?.email || 'Profile'
  }
}, { immediate: true })
</script>

<template>
  <div>
    <!-- Кнопка входа для неавторизованных -->
    <UButton
      v-if="!auth.isAuthenticated"
      @click="modal.open()"
    >
      Login
    </UButton>

    <!-- DropdownMenu для авторизованных -->
    <UDropdownMenu
      v-else
      :items="dropdownItems"
      :content="{
        align: 'end',
        side: 'bottom'
      }"
    >
      <UButton
        icon="i-heroicons-user-circle"
        variant="ghost"
        :badge="auth.user?.email?.charAt(0).toUpperCase()"
      />
    </UDropdownMenu>
  </div>
</template>