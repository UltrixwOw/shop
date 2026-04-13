<!-- components/AppAuthModal.vue -->
<script setup lang="ts">
import { ref, computed } from "vue"
import { useNuxtApp } from "#app"
import { useAuthStore } from "~/stores/auth"
import { useAuthModalStore } from "~/stores/authModal"

const { $api } = useNuxtApp()
const { t } = useI18n()
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
    error.value = e.response?.data?.detail || t('login_error')
  } finally {
    loading.value = false
  }
}

const register = async () => {
  error.value = ""

  if (password.value !== confirmPassword.value) {
    error.value = t('password_mismatch')
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
    error.value = e.response?.data?.error || t('register_error')
  } finally {
    loading.value = false
  }
}

// Вычисляемое свойство для заголовка
const modalTitle = computed(() => {
  switch (mode.value) {
    case 'login': return t('login_title')
    case 'register': return t('register_title')
    case 'verify': return t('verify_title')
  }
})

// Описание для каждого режима (для screen reader'ов)
const modalDescription = computed(() => {
  switch (mode.value) {
    case 'login': return t('login_subtitle')
    case 'register': return t('register_subtitle')
    case 'verify': return t('verify_subtitle')
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
    class="max-w-md z-50"
    :ui="{
      overlay: 'z-45',
    }"
  >
    <template #body>
      <!-- ЛОГИН -->
      <div v-if="mode === 'login'" class="space-y-4">
        <UFormField :label="$t('email')">
          <UInput v-model="email" type="email" class="w-full" />
        </UFormField>

        <UFormField :label="$t('password')">
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
        <UFormField :label="$t('email')">
          <UInput v-model="email" type="email" class="w-full" />
        </UFormField>

        <UFormField :label="$t('password')">
          <UInput v-model="password" type="password" class="w-full" />
        </UFormField>

        <UFormField :label="$t('confirm_password')">
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
          {{ $t('verification_sent') }}
        </UAlert>
      </div>
    </template>

    <!-- ФУТЕР с кнопками действий -->
    <template #footer="{ close }">
      <div class="flex flex-col gap-4 w-full">
        <!-- Кнопки для логина -->
        <template v-if="mode === 'login'">
          <UButton
            class="w-full"
            :loading="loading"
            @click="login"
          >
            {{ $t('sign_in') }}
          </UButton>
          
          <div class="text-sm text-center">
            {{ $t('no_account') }}
            <UButton variant="link" @click="switchToRegister">
              {{ $t('register') }}
            </UButton>
          </div>
        </template>

        <!-- Кнопки для регистрации -->
        <template v-else-if="mode === 'register'">
          <UButton
            class="w-full"
            :loading="loading"
            @click="register"
          >
            {{ $t('sign_up') }}
          </UButton>
          
          <div class="text-sm text-center">
            {{ $t('have_account') }}
            <UButton variant="link" @click="switchToLogin">
              {{ $t('sign_in') }}
            </UButton>
          </div>
        </template>

        <!-- Кнопки для верификации -->
        <template v-else-if="mode === 'verify'">
          <UButton
            class="w-full"
            @click="switchToLogin"
          >
            {{ $t('go_to_login') }}
          </UButton>
        </template>
      </div>
    </template>
  </UModal>
</template>