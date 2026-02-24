<template>
  <div v-if="isOpen" class="modal">
    <!-- LOGIN STEP 1 -->
    <div v-if="mode === 'login' && step === 1">
      <h2>Вход</h2>

      <input v-model="email" type="email" placeholder="Email" />

      <button @click="checkUser">Далее</button>

      <p v-if="error" class="error">{{ error }}</p>

      <p>
        Нет аккаунта?
        <button @click="switchToRegister">Регистрация</button>
      </p>
    </div>

    <!-- LOGIN STEP 2 -->
    <div v-if="mode === 'login' && step === 2">
      <h2>Введите пароль</h2>

      <input v-model="password" type="password" placeholder="Пароль" />

      <button @click="login">Войти</button>

      <p v-if="error" class="error">{{ error }}</p>
    </div>

    <!-- REGISTER -->
    <div v-if="mode === 'register'">
      <h2>Регистрация</h2>

      <input v-model="email" type="email" placeholder="Email" />
      <input v-model="password" type="password" placeholder="Пароль" />
      <input v-model="confirmPassword" type="password" placeholder="Подтвердите пароль" />

      <button @click="register">Зарегистрироваться</button>

      <p v-if="error" class="error">{{ error }}</p>

      <p>
        Уже есть аккаунт?
        <button @click="switchToLogin">Вход</button>
      </p>
    </div>

    <!-- VERIFY -->
    <div v-if="mode === 'verify'">
      <h2>Подтвердите email</h2>
      <p>Мы отправили ссылку на вашу почту.</p>

      <button @click="switchToLogin">Перейти ко входу</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useNuxtApp } from "#app";
import { useAuthStore } from "~/stores/auth";

const { $api } = useNuxtApp();
const auth = useAuthStore();

// 🔐 Управление
const isOpen = ref(true);
const mode = ref<"login" | "register" | "verify">("login");
const step = ref(1);

// Данные
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const error = ref("");

// --------------------
// Переключения
// --------------------

const switchToRegister = () => {
  reset();
  mode.value = "register";
};

const switchToLogin = () => {
  reset();
  mode.value = "login";
  step.value = 1;
};

const reset = () => {
  email.value = "";
  password.value = "";
  confirmPassword.value = "";
  error.value = "";
};

// --------------------
// Проверка пользователя
// --------------------

const checkUser = async () => {
  error.value = "";

  try {
    await $api.post("/users/check-email/", { email: email.value });
    step.value = 2;
  } catch {
    error.value = "Такой пользователь не найден. Зарегистрируйтесь.";
  }
};

// --------------------
// Логин
// --------------------

const login = async () => {
  error.value = "";

  try {
    await auth.login(email.value, password.value);
    isOpen.value = false;
  } catch {
    error.value = "Неверный email или пароль";
  }
};

// --------------------
// Регистрация
// --------------------

const register = async () => {
  error.value = "";

  if (password.value !== confirmPassword.value) {
    error.value = "Пароли не совпадают";
    return;
  }

  try {
    await $api.post("/users/register/", {
      email: email.value,
      password: password.value,
    });

    step.value = "verify";
  } catch (e: any) {
    if (e.response?.data?.error === "User already registered") {
      errorMessage.value = "Пользователь уже зарегистрирован";
    }
  }
};
</script>

<style scoped>
.modal {
  padding: 20px;
  background: white;
  width: 400px;
}

.error {
  color: red;
}
</style>
