<script setup lang="ts">
// Простая приветственная логика в зависимости от времени суток
const getGreeting = () => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Доброе утро'
  if (hour < 18) return 'Добрый день'
  return 'Добрый вечер'
}

const greeting = ref(getGreeting())
// Пример: можно добавить анимацию или обновление приветствия
</script>

<template>
  <UContainer class="min-h-screen py-16">
    <!-- Герой-секция с градиентом -->
    <div class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-primary-900 via-primary-700 to-primary-500 dark:from-primary-950 dark:via-primary-900 dark:to-primary-700 mb-16">
      <!-- Декоративные элементы фона -->
      <div class="absolute inset-0 bg-grid-white/10 [mask-image:linear-gradient(0deg,transparent,black)]" />
      <div class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent" />
      
      <!-- Контент -->
      <div class="relative px-8 py-20 md:px-12 md:py-28 lg:px-16 text-center lg:text-left">
        <div class="max-w-4xl mx-auto lg:mx-0">
          <!-- Приветствие -->
          <UBadge
            size="lg"
            color="white"
            variant="soft"
            class="mb-6 backdrop-blur-sm bg-white/10 text-white border-white/20"
          >
            {{ greeting }}
          </UBadge>
          
          <!-- Заголовок -->
          <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-6">
            Добро пожаловать в
            <span class="block text-5xl md:text-6xl lg:text-7xl mt-2 text-transparent bg-clip-text bg-gradient-to-r from-yellow-200 to-pink-200">
              Meloni
            </span>
          </h1>
          
          <!-- Описание -->
          <p class="text-xl text-white/80 mb-8 max-w-2xl mx-auto lg:mx-0">
            Откройте для себя уникальные товары и наслаждайтесь удобным шопингом с доставкой по всему миру.
          </p>
          
          <!-- Кнопки действий -->
          <div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
            <UButton
              to="/products"
              size="xl"
              color="white"
              variant="solid"
              class="shadow-lg hover:shadow-xl transition-all duration-300"
            >
              Начать покупки
            </UButton>
            <UButton
              to="/about"
              size="xl"
              color="white"
              variant="outline"
              class="border-white/30 text-white hover:bg-white/10"
            >
              Узнать больше
            </UButton>
          </div>
        </div>
      </div>
      
      <!-- Иллюстрация / Декоративное изображение -->
      <div class="absolute -bottom-16 -right-16 lg:bottom-0 lg:right-0 w-64 h-64 lg:w-96 lg:h-96 opacity-20 lg:opacity-30">
        <div class="absolute inset-0 bg-white rounded-full blur-3xl" />
      </div>
    </div>

    <!-- Секция с преимуществами -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
      <UCard class="text-center hover:shadow-lg transition-shadow">
        <template #header>
          <div class="flex justify-center">
            <div class="p-3 bg-primary-100 dark:bg-primary-900 rounded-full">
              <UIcon name="i-heroicons-truck" class="w-8 h-8 text-primary-600 dark:text-primary-400" />
            </div>
          </div>
        </template>
        
        <h3 class="text-xl font-semibold mb-2">Быстрая доставка</h3>
        <p class="text-gray-600 dark:text-gray-400">
          Доставляем заказы по всему миру в кратчайшие сроки
        </p>
      </UCard>

      <UCard class="text-center hover:shadow-lg transition-shadow">
        <template #header>
          <div class="flex justify-center">
            <div class="p-3 bg-primary-100 dark:bg-primary-900 rounded-full">
              <UIcon name="i-heroicons-shield-check" class="w-8 h-8 text-primary-600 dark:text-primary-400" />
            </div>
          </div>
        </template>
        
        <h3 class="text-xl font-semibold mb-2">Безопасная оплата</h3>
        <p class="text-gray-600 dark:text-gray-400">
          Ваши платежные данные надежно защищены
        </p>
      </UCard>

      <UCard class="text-center hover:shadow-lg transition-shadow">
        <template #header>
          <div class="flex justify-center">
            <div class="p-3 bg-primary-100 dark:bg-primary-900 rounded-full">
              <UIcon name="i-heroicons-chat-bubble-left-right" class="w-8 h-8 text-primary-600 dark:text-primary-400" />
            </div>
          </div>
        </template>
        
        <h3 class="text-xl font-semibold mb-2">Поддержка 24/7</h3>
        <p class="text-gray-600 dark:text-gray-400">
          Всегда готовы помочь с любым вопросом
        </p>
      </UCard>
    </div>

    <!-- Секция "Популярные категории" (опционально) -->
    <div class="text-center">
      <h2 class="text-3xl font-bold mb-8">Популярные категории</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <UButton
          v-for="i in 4"
          :key="i"
          to="/products"
          color="neutral"
          variant="soft"
          class="py-8 text-lg"
        >
          Категория {{ i }}
        </UButton>
      </div>
    </div>
  </UContainer>
</template>

<style scoped>
.bg-grid-white\/10 {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32' width='32' height='32' fill='none' stroke='rgb(255 255 255 / 0.1)'%3e%3cpath d='M0 .5H31.5V32'/%3e%3c/svg%3e");
}
</style>