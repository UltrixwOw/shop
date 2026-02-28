<script setup lang="ts">
// Метаданные страницы
definePageMeta({
  title: 'О нас'
})

// Команда компании (можно заменить на реальные данные из API)
const teamMembers = ref([
  {
    name: 'Анна Смирнова',
    role: 'Основатель & CEO',
    bio: 'Более 10 лет в e-commerce, создаёт уникальные shopping-экспериенсы',
    avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=400&fit=crop',
    social: {
      linkedin: '#',
      twitter: '#'
    }
  },
  {
    name: 'Михаил Волков',
    role: 'Art Director',
    bio: 'Отвечает за визуальный стиль и пользовательский опыт бренда',
    avatar: 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&h=400&fit=crop',
    social: {
      linkedin: '#',
      instagram: '#'
    }
  },
  {
    name: 'Екатерина Павлова',
    role: 'Head of Product',
    bio: 'Разрабатывает стратегию развития ассортимента',
    avatar: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=400&h=400&fit=crop',
    social: {
      linkedin: '#',
      twitter: '#'
    }
  },
  {
    name: 'Дмитрий Соколов',
    role: 'Технический директор',
    bio: 'Обеспечивает бесперебойную работу платформы',
    avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop',
    social: {
      github: '#',
      linkedin: '#'
    }
  }
])

// Статистика компании
const stats = ref([
  { value: '5K+', label: 'Довольных клиентов', icon: 'i-heroicons-users' },
  { value: '10K+', label: 'Товаров в каталоге', icon: 'i-heroicons-cube' },
  { value: '15+', label: 'Стран доставки', icon: 'i-heroicons-globe-alt' },
  { value: '24/7', label: 'Поддержка', icon: 'i-heroicons-chat-bubble-left-right' }
])

// Ценности компании
const values = ref([
  {
    title: 'Качество',
    description: 'Мы тщательно отбираем каждый товар, чтобы вы получали только лучшее.',
    icon: 'i-heroicons-star'
  },
  {
    title: 'Доверие',
    description: 'Прозрачность на всех этапах — от заказа до доставки.',
    icon: 'i-heroicons-hand-raised'
  },
  {
    title: 'Инновации',
    description: 'Постоянно внедряем новые технологии для вашего удобства.',
    icon: 'i-heroicons-rocket-launch'
  },
  {
    title: 'Забота',
    description: 'Мы ценим каждого клиента и всегда готовы помочь.',
    icon: 'i-heroicons-heart'
  }
])
</script>

<template>
  <UContainer class="py-12">
    <!-- Хлебные крошки -->
    <UBreadcrumb
      :items="[
        { label: 'Главная', to: '/' },
        { label: 'О нас', to: '/about' }
      ]"
      class="mb-8"
    />

    <!-- Герой-секция с параллакс эффектом -->
    <div class="relative rounded-3xl overflow-hidden mb-16 h-[400px] md:h-[500px]">
      <img
        src="https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1600&h=900&fit=crop"
        alt="О нас"
        class="absolute inset-0 w-full h-full object-cover"
      />
      <div class="absolute inset-0 bg-gradient-to-r from-primary-900/90 to-primary-800/80" />
      
      <div class="absolute inset-0 flex items-center">
        <div class="px-8 md:px-12 text-white max-w-3xl">
          <UBadge color="white" variant="soft" size="lg" class="mb-4">
            Добро пожаловать в Meloni
          </UBadge>
          
          <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold mb-4">
            Мы создаём<br />лучший шопинг-опыт
          </h1>
          
          <p class="text-xl text-white/80">
            История бренда, который начался с мечты сделать онлайн-покупки проще, 
            приятнее и доступнее для каждого.
          </p>
        </div>
      </div>
    </div>

    <!-- Наша история -->
    <div class="grid lg:grid-cols-2 gap-12 items-center mb-20">
      <div>
        <h2 class="text-3xl font-bold mb-4">Наша история</h2>
        <div class="space-y-4 text-gray-600 dark:text-gray-400">
          <p>
            Meloni родился в 2020 году из простой идеи: сделать онлайн-шопинг 
            таким же приятным, как прогулка по любимому бутику. Мы заметили, 
            что многие платформы забывают о человеческом подходе, превращая 
            покупки в бездушный процесс.
          </p>
          <p>
            За четыре года мы выросли из небольшого стартапа в международную 
            платформу, но не потеряли главного — внимания к каждому клиенту. 
            Сегодня Meloni — это сообщество людей, объединённых любовью к 
            качественным вещам и отличному сервису.
          </p>
          <p>
            Мы гордимся тем, что 80% наших клиентов возвращаются снова, а 
            многие становятся нашими друзьями. И это только начало!
          </p>
        </div>
      </div>
      
      <div class="grid grid-cols-2 gap-4">
        <div class="space-y-4">
          <img
            src="https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=400&h=300&fit=crop"
            alt="Склад"
            class="rounded-2xl h-48 w-full object-cover"
          />
          <img
            src="https://images.unsplash.com/photo-1534723452862-4c874018d66d?w=400&h=300&fit=crop"
            alt="Упаковка"
            class="rounded-2xl h-40 w-full object-cover"
          />
        </div>
        <div class="space-y-4 mt-8">
          <img
            src="https://images.unsplash.com/photo-1603252110971-4a48c3677be8?w=400&h=300&fit=crop"
            alt="Команда"
            class="rounded-2xl h-40 w-full object-cover"
          />
          <img
            src="https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?w=400&h=300&fit=crop"
            alt="Магазин"
            class="rounded-2xl h-48 w-full object-cover"
          />
        </div>
      </div>
    </div>

    <!-- Статистика -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-6 mb-20">
      <UCard
        v-for="stat in stats"
        :key="stat.label"
        class="text-center hover:shadow-lg transition-shadow"
      >
        <UIcon :name="stat.icon" class="w-8 h-8 text-primary-600 mx-auto mb-2" />
        <p class="text-3xl font-bold text-primary-600">{{ stat.value }}</p>
        <p class="text-sm text-gray-600 dark:text-gray-400">{{ stat.label }}</p>
      </UCard>
    </div>

    <!-- Наши ценности -->
    <div class="mb-20">
      <h2 class="text-3xl font-bold text-center mb-12">Наши ценности</h2>
      
      <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        <UCard
          v-for="value in values"
          :key="value.title"
          class="text-center hover:scale-105 transition-transform"
        >
          <template #header>
            <div class="flex justify-center">
              <div class="p-3 bg-primary-100 dark:bg-primary-900 rounded-full">
                <UIcon :name="value.icon" class="w-6 h-6 text-primary-600 dark:text-primary-400" />
              </div>
            </div>
          </template>
          
          <h3 class="text-lg font-semibold mb-2">{{ value.title }}</h3>
          <p class="text-sm text-gray-600 dark:text-gray-400">{{ value.description }}</p>
        </UCard>
      </div>
    </div>

    <!-- Команда -->
    <div class="mb-20">
      <div class="text-center mb-12">
        <h2 class="text-3xl font-bold mb-4">Команда мечты</h2>
        <p class="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          За каждым успешным заказом стоят талантливые люди, которые делают Meloni особенным
        </p>
      </div>

      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <UCard
          v-for="member in teamMembers"
          :key="member.name"
          class="text-center"
        >
          <UAvatar
            :src="member.avatar"
            :alt="member.name"
            size="xl"
            class="mx-auto mb-4"
          />
          
          <h3 class="font-semibold text-lg">{{ member.name }}</h3>
          <p class="text-sm text-primary-600 mb-2">{{ member.role }}</p>
          <p class="text-xs text-gray-500 mb-4">{{ member.bio }}</p>
          
          <div class="flex justify-center gap-2">
            <UButton
              v-for="(url, platform) in member.social"
              :key="platform"
              :to="url"
              color="neutral"
              variant="ghost"
              size="xs"
              :icon="`i-heroicons-${platform}`"
              target="_blank"
            />
          </div>
        </UCard>
      </div>
    </div>

    <!-- Контакты и карта -->
    <div class="grid lg:grid-cols-2 gap-8">
      <UCard>
        <template #header>
          <h3 class="text-xl font-semibold">Свяжитесь с нами</h3>
        </template>

        <div class="space-y-4">
          <div class="flex items-center gap-3">
            <UIcon name="i-heroicons-map-pin" class="w-5 h-5 text-primary-600" />
            <span>ул. Тверская, 15, Москва, 123456</span>
          </div>
          
          <div class="flex items-center gap-3">
            <UIcon name="i-heroicons-phone" class="w-5 h-5 text-primary-600" />
            <a href="tel:+74951234567" class="hover:text-primary-600">+7 (495) 123-45-67</a>
          </div>
          
          <div class="flex items-center gap-3">
            <UIcon name="i-heroicons-envelope" class="w-5 h-5 text-primary-600" />
            <a href="mailto:hello@meloni.com" class="hover:text-primary-600">hello@meloni.com</a>
          </div>
          
          <div class="flex items-center gap-3">
            <UIcon name="i-heroicons-clock" class="w-5 h-5 text-primary-600" />
            <span>Пн-Пт: 9:00 - 20:00, Сб-Вс: 10:00 - 18:00</span>
          </div>

          <USeparator class="my-4" />

          <div class="flex gap-2">
            <UButton
              v-for="social in ['instagram', 'telegram', 'youtube', 'facebook']"
              :key="social"
              :icon="`i-heroicons-${social}`"
              color="neutral"
              variant="soft"
              to="#"
              target="_blank"
            />
          </div>
        </div>
      </UCard>

      <UCard>
        <iframe
          src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2245.287548782147!2d37.6036!3d55.7623!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNTXCsDQ1JzQ0LjMiTiAzN8KwMzYnMTIuOSJF!5e0!3m2!1sru!2sru!4v1620000000000!5m2!1sru!2sru"
          width="100%"
          height="300"
          style="border:0;"
          allowfullscreen=""
          loading="lazy"
          class="rounded-lg"
        />
      </UCard>
    </div>
  </UContainer>
</template>

<style scoped>
/* Плавное появление элементов */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>