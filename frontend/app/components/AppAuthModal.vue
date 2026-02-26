<template>
  <div v-if="modal.isOpen" class="modal">

    <!-- LOGIN -->
    <div v-if="mode === 'login'">
      <h2>Вход</h2>

      <input v-model="email" type="email" placeholder="Email" />
      <input v-model="password" type="password" placeholder="Пароль" />

      <button :disabled="loading" @click="login">
        <span v-if="loading">Загрузка...</span>
        <span v-else>Войти</span>
      </button>

      <p v-if="error" class="error">{{ error }}</p>

      <p>
        Нет аккаунта?
        <button @click="switchToRegister">Регистрация</button>
      </p>
    </div>

    <!-- REGISTER -->
    <div v-if="mode === 'register'">
      <h2>Регистрация</h2>

      <input v-model="email" type="email" placeholder="Email" />
      <input v-model="password" type="password" placeholder="Пароль" />
      <input v-model="confirmPassword" type="password" placeholder="Подтвердите пароль" />

      <button :disabled="loading" @click="register">
        <span v-if="loading">Загрузка...</span>
        <span v-else>Зарегистрироваться</span>
      </button>

      <p v-if="error" class="error">{{ error }}</p>

      <p>
        Уже есть аккаунт?
        <button @click="switchToLogin">Вход</button>
      </p>
    </div>

    <!-- VERIFY -->
    <div v-if="mode === 'verify'">
      <h2>Проверьте почту</h2>
      <p>Мы отправили письмо для подтверждения email.</p>

      <button @click="switchToLogin">Перейти ко входу</button>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
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
    modal.close()   // 🔥 авто-закрытие
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
</script>

<style scoped>
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 30px;
  background: white;
  width: 400px;
  box-shadow: 0 10px 30px rgba(0,0,0,.2);
  border-radius: 10px;
}

button {
  margin-top: 10px;
  width: 100%;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>