<!-- components/AppAuthModal.vue -->
<script setup lang="ts">
import { ref, computed } from "vue"
import { useNuxtApp } from "#app"
import { useAuthStore } from "~/stores/auth"
import { useAuthModalStore } from "~/stores/authModal"

const { $api } = useNuxtApp()
const auth = useAuthStore()
const modal = useAuthModalStore()

const mode = ref<"login" | "register" | "verify">("login")

const email = ref("")
const password = ref("")
const confirmPassword = ref("")
const error = ref("")
const loading = ref(false)

const reset = () => {
  email.value = ""
  password.value = ""
  confirmPassword.value = ""
  error.value = ""
}

const switchToRegister = () => {
  reset()
  mode.value = "register"
}

const switchToLogin = () => {
  reset()
  mode.value = "login"
}

const login = async () => {
  error.value = ""
  loading.value = true

  try {
    await auth.login(email.value, password.value)
    modal.close()
    reset()
  } catch (e: any) {
    error.value = e.response?.data?.detail || "Ошибка входа"
  } finally {
    loading.value = false
  }
}

const register = async () => {
  error.value = ""

  if (password.value !== confirmPassword.value) {
    error.value = "Пароли не совпадают"
    return
  }

  loading.value = true

  try {
    const res = await $api.post("/users/register/", {
      email: email.value,
      password: password.value,
    })

    if (res.data?.message === "Check your email") {
      reset()
      mode.value = "verify"
    }
  } catch (e: any) {
    error.value = e.response?.data?.error || "Ошибка регистрации"
  } finally {
    loading.value = false
  }
}

// Вычисляемое свойство для заголовка
const modalTitle = computed(() => {
  switch (mode.value) {
    case 'login': return 'Вход'
    case 'register': return 'Регистрация'
    case 'verify': return 'Проверьте почту'
  }
})

// ✅ Добавляем описание для каждого режима (для screen reader'ов)
const modalDescription = computed(() => {
  switch (mode.value) {
    case 'login': return 'Форма входа с email и паролем'
    case 'register': return 'Форма регистрации нового аккаунта'
    case 'verify': return 'Подтверждение email адреса'
  }
})
</script>

<template>
  <UModal
    v-model:open="modal.isOpen"
    :title="modalTitle"
    :description="modalDescription"  
    :close="{
      icon: 'i-heroicons-x-mark-20-solid',
      color: 'neutral',
      variant: 'ghost'
    }"
    class="max-w-md"
  >
    <template #body>
      <!-- ЛОГИН -->
      <div v-if="mode === 'login'" class="space-y-4">
        <UFormField label="Email">
          <UInput v-model="email" type="email" class="w-full" />
        </UFormField>

        <UFormField label="Пароль">
          <UInput v-model="password" type="password" class="w-full" />
        </UFormField>

        <UAlert
          v-if="error"
          color="error"
          variant="soft"
          :title="error"
        />
      </div>

      <!-- РЕГИСТРАЦИЯ -->
      <div v-else-if="mode === 'register'" class="space-y-4">
        <UFormField label="Email">
          <UInput v-model="email" type="email" class="w-full" />
        </UFormField>

        <UFormField label="Пароль">
          <UInput v-model="password" type="password" class="w-full" />
        </UFormField>

        <UFormField label="Подтвердите пароль">
          <UInput v-model="confirmPassword" type="password" class="w-full" />
        </UFormField>

        <UAlert
          v-if="error"
          color="error"
          variant="soft"
          :title="error"
        />
      </div>

      <!-- ПОДТВЕРЖДЕНИЕ -->
      <div v-else-if="mode === 'verify'" class="space-y-4">
        <UAlert color="primary" variant="soft">
          Мы отправили письмо для подтверждения email.
        </UAlert>
      </div>
    </template>

    <!-- ФУТЕР с кнопками действий -->
    <template #footer="{ close }">
      <div class="flex flex-col gap-4 w-full">
        <!-- Кнопки для логина/регистрации -->
        <template v-if="mode === 'login'">
          <UButton
            class="w-full"
            :loading="loading"
            @click="login"
          >
            Войти
          </UButton>
          
          <div class="text-sm text-center">
            Нет аккаунта?
            <UButton variant="link" @click="switchToRegister">
              Регистрация
            </UButton>
          </div>
        </template>

        <template v-else-if="mode === 'register'">
          <UButton
            class="w-full"
            :loading="loading"
            @click="register"
          >
            Зарегистрироваться
          </UButton>
          
          <div class="text-sm text-center">
            Уже есть аккаунт?
            <UButton variant="link" @click="switchToLogin">
              Вход
            </UButton>
          </div>
        </template>

        <template v-else-if="mode === 'verify'">
          <UButton
            class="w-full"
            @click="switchToLogin"
          >
            Перейти ко входу
          </UButton>
        </template>
      </div>
    </template>
  </UModal>
</template>