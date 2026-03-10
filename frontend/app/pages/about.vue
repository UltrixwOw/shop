<script setup lang="ts">
// Метаданные страницы
definePageMeta({
  title: 'О нас'
})

// Ссылки для PageHero
const heroLinks = ref([
  {
    label: 'Наши товары',
    to: '/products',
    icon: 'i-heroicons-shopping-bag',
    color: 'primary' as const,
    size: 'lg' as const
  },
  {
    label: 'Связаться с нами',
    to: '#contact',
    color: 'neutral' as const,
    variant: 'subtle' as const,
    trailingIcon: 'i-heroicons-arrow-right',
    size: 'lg' as const
  }
])

// Команда компании с надежными изображениями
const teamMembers = ref([
  {
    name: 'Анна Смирнова',
    role: 'Основатель & CEO',
    description: 'Более 10 лет в e-commerce, создаёт уникальные shopping-экспериенсы',
    // Используем picsum для надежности
    avatar: {
      src: 'https://picsum.photos/id/64/400/400', // мужчина в очках
      alt: 'Анна Смирнова'
    }
  },
  {
    name: 'Михаил Волков',
    role: 'Art Director',
    description: 'Отвечает за визуальный стиль и пользовательский опыт бренда',
    avatar: {
      src: 'https://picsum.photos/id/1005/400/400', // мужчина с бородой
      alt: 'Михаил Волков'
    }
  },
  {
    name: 'Екатерина Павлова',
    role: 'Head of Product',
    description: 'Разрабатывает стратегию развития ассортимента',
    avatar: {
      src: 'https://picsum.photos/id/1027/400/400', // девушка в очках
      alt: 'Екатерина Павлова'
    }
  },
  {
    name: 'Дмитрий Соколов',
    role: 'Технический директор',
    description: 'Обеспечивает бесперебойную работу платформы',
    avatar: {
      src: 'https://picsum.photos/id/1043/400/400', // мужчина в шапке
      alt: 'Дмитрий Соколов'
    }
  }
])

// Статистика компании
const stats = ref([
  { 
    label: 'Довольных клиентов', 
    value: '5K+', 
    icon: 'i-heroicons-users' 
  },
  { 
    label: 'Товаров в каталоге', 
    value: '10K+', 
    icon: 'i-heroicons-cube' 
  },
  { 
    label: 'Стран доставки', 
    value: '15+', 
    icon: 'i-heroicons-globe-alt' 
  },
  { 
    label: 'Поддержка', 
    value: '24/7', 
    icon: 'i-heroicons-chat-bubble-left-right' 
  }
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

// Социальные сети
const socialLinks = ref([
  { icon: 'i-heroicons-envelope', to: 'mailto:hello@meloni.com', label: 'Email' },
  { icon: 'i-simple-icons-instagram', to: 'https://instagram.com/meloni', label: 'Instagram' },
  { icon: 'i-simple-icons-telegram', to: 'https://t.me/meloni', label: 'Telegram' },
  { icon: 'i-simple-icons-youtube', to: 'https://youtube.com/@meloni', label: 'YouTube' },
  { icon: 'i-simple-icons-facebook', to: 'https://facebook.com/meloni', label: 'Facebook' }
])

// Альтернативный вариант с инициалами (если изображения не нужны)
const teamMembersWithInitials = ref([
  {
    name: 'Анна Смирнова',
    role: 'Основатель & CEO',
    description: 'Более 10 лет в e-commerce, создаёт уникальные shopping-экспериенсы',
    avatar: {
      text: 'АС', // инициалы
      alt: 'Анна Смирнова'
    }
  },
  {
    name: 'Михаил Волков',
    role: 'Art Director',
    description: 'Отвечает за визуальный стиль и пользовательский опыт бренда',
    avatar: {
      text: 'МВ',
      alt: 'Михаил Волков'
    }
  },
  {
    name: 'Екатерина Павлова',
    role: 'Head of Product',
    description: 'Разрабатывает стратегию развития ассортимента',
    avatar: {
      text: 'ЕП',
      alt: 'Екатерина Павлова'
    }
  },
  {
    name: 'Дмитрий Соколов',
    role: 'Технический директор',
    description: 'Обеспечивает бесперебойную работу платформы',
    avatar: {
      text: 'ДС',
      alt: 'Дмитрий Соколов'
    }
  }
])
</script>

<template>
  <main>
    <!-- PageHero компонент -->
    <UPageHero
      orientation="horizontal"
      headline="Добро пожаловать в онлайн-магазин Meloni"
      title="Мы создаём лучший шопинг-опыт"
      description="История бренда, который начался с мечты сделать онлайн-покупки проще, приятнее и доступнее для каждого."
      :links="heroLinks"
    >
      <!-- Изображение для правой части -->
      <img
        src="https://picsum.photos/id/42/800/600"
        alt="О нас"
        class="rounded-2xl shadow-2xl ring ring-default w-full h-auto"
        width="800"
        height="600"
        loading="lazy"
      />
    </UPageHero>

    <!-- PageSection - Наша история -->
    <UPageSection
      orientation="horizontal"
      reverse
      title="Наша история"
      description="Meloni родился в 2020 году из простой идеи: сделать онлайн-шопинг таким же приятным, как прогулка по любимому бутику. Мы заметили, что многие платформы забывают о человеческом подходе, превращая покупки в бездушный процесс."
      headline="О НАС"
      icon="i-heroicons-clock"
    >
      <!-- Галерея изображений в правой части -->
      <div class="grid grid-cols-2 gap-4">
        <div class="space-y-4">
          <img
            src="https://picsum.photos/id/26/400/300"
            alt="Склад"
            class="rounded-2xl w-full h-48 object-cover ring ring-default"
          />
          <img
            src="https://picsum.photos/id/27/400/300"
            alt="Упаковка"
            class="rounded-2xl w-full h-40 object-cover ring ring-default"
          />
        </div>
        <div class="space-y-4 mt-8">
          <img
            src="https://picsum.photos/id/28/400/300"
            alt="Команда"
            class="rounded-2xl w-full h-40 object-cover ring ring-default"
          />
          <img
            src="https://picsum.photos/id/29/400/300"
            alt="Магазин"
            class="rounded-2xl w-full h-48 object-cover ring ring-default"
          />
        </div>
      </div>
    </UPageSection>

    <!-- PageSection - Статистика -->
    <UPageSection
      title="Meloni в цифрах"
      description="Мы гордимся тем, что 80% наших клиентов возвращаются снова, а многие становятся нашими друзьями."
      headline="СТАТИСТИКА"
      icon="i-heroicons-chart-bar"
    >
      <!-- PageGrid для статистики -->
      <UPageGrid>
        <UCard
          v-for="stat in stats"
          :key="stat.label"
          class="text-center"
        >
          <UIcon :name="stat.icon" class="w-8 h-8 text-primary mx-auto mb-2" />
          <p class="text-3xl font-bold text-primary">{{ stat.value }}</p>
          <p class="text-sm text-muted">{{ stat.label }}</p>
        </UCard>
      </UPageGrid>
    </UPageSection>

    <!-- PageSection - Наши ценности -->
    <UPageSection
      title="Наши ценности"
      description="Четыре принципа, которые делают Meloni особенным"
      headline="ЦЕННОСТИ"
      icon="i-heroicons-heart"
    >
      <!-- PageGrid для ценностей -->
      <UPageGrid>
        <UCard
          v-for="value in values"
          :key="value.title"
          class="text-center"
        >
          <div class="flex justify-center mb-4">
            <div class="p-3 bg-primary/10 rounded-full">
              <UIcon :name="value.icon" class="flex w-6 h-6 text-primary" />
            </div>
          </div>
          <h3 class="text-lg font-semibold mb-2">{{ value.title }}</h3>
          <p class="text-sm text-muted">{{ value.description }}</p>
        </UCard>
      </UPageGrid>
    </UPageSection>

    <!-- PageSection - Команда с picsum изображениями -->
    <UPageSection
      title="Команда мечты"
      description="За каждым успешным заказом стоят талантливые люди, которые делают Meloni особенным"
      headline="КТО МЫ"
      icon="i-heroicons-users"
    >
      <!-- PageGrid для команды -->
      <UPageGrid>
        <UCard
          v-for="member in teamMembers"
          :key="member.name"
          class="text-center"
        >
          <UAvatar
            v-bind="member.avatar"
            size="xl"
            class="mx-auto mb-4"
          />
          
          <h3 class="font-semibold text-lg">{{ member.name }}</h3>
          <p class="text-sm text-primary mb-2">{{ member.role }}</p>
          <p class="text-xs text-muted mb-4">{{ member.description }}</p>
        </UCard>
      </UPageGrid>
    </UPageSection>

    <!-- Альтернативный вариант с инициалами (раскомментируйте если нужно) -->
    <!-- <UPageSection
      title="Команда мечты"
      description="За каждым успешным заказом стоят талантливые люди, которые делают Meloni особенным"
      headline="КТО МЫ"
      icon="i-heroicons-users"
    >
      <UPageGrid>
        <UCard
          v-for="member in teamMembersWithInitials"
          :key="member.name"
          class="text-center"
        >
          <UAvatar
            v-bind="member.avatar"
            size="xl"
            class="mx-auto mb-4"
          />
          
          <h3 class="font-semibold text-lg">{{ member.name }}</h3>
          <p class="text-sm text-primary mb-2">{{ member.role }}</p>
          <p class="text-xs text-muted mb-4">{{ member.description }}</p>
        </UCard>
      </UPageGrid>
    </UPageSection> -->

    <!-- PageSection - Контакты -->
    <UPageSection
      id="contact"
      title="Свяжитесь с нами"
      description="Мы всегда рады помочь и ответить на ваши вопросы"
      headline="КОНТАКТЫ"
      icon="i-heroicons-chat-bubble-left-right"
    >
      <div class="grid lg:grid-cols-2 gap-8">
        <!-- Контактная информация -->
        <UCard>
          <div class="space-y-4">
            <div class="flex items-center gap-3">
              <UIcon name="i-heroicons-map-pin" class="w-5 h-5 text-primary shrink-0" />
              <span class="text-muted">Alexanderplatz 1, 10178 Berlin, Германия</span>
            </div>
            
            <div class="flex items-center gap-3">
              <UIcon name="i-heroicons-phone" class="w-5 h-5 text-primary shrink-0" />
              <a href="tel:+49301234567" class="text-muted hover:text-primary transition-colors">
                +49 30 1234567
              </a>
            </div>
            
            <div class="flex items-center gap-3">
              <UIcon name="i-heroicons-envelope" class="w-5 h-5 text-primary shrink-0" />
              <a href="mailto:hello@meloni.com" class="text-muted hover:text-primary transition-colors">
                hello@meloni.com
              </a>
            </div>
            
            <div class="flex items-center gap-3">
              <UIcon name="i-heroicons-clock" class="w-5 h-5 text-primary shrink-0" />
              <span class="text-muted">Пн-Пт: 9:00 - 20:00, Сб-Вс: 10:00 - 18:00</span>
            </div>

            <USeparator class="my-4" />

            <!-- Социальные сети -->
            <div class="flex gap-2">
              <UButton
                v-for="social in socialLinks"
                :key="social.label"
                :icon="social.icon"
                :to="social.to"
                color="neutral"
                variant="soft"
                target="_blank"
                :aria-label="social.label"
              />
            </div>
          </div>
        </UCard>

        <!-- Карта -->
        <UCard class="p-0 overflow-hidden">
          <iframe
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2427.234567890123!2d13.4123!3d52.5200!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47a84e123456789%3A0x1234567890abcdef!2sAlexanderplatz%2C%2010178%20Berlin!5e0!3m2!1sru!2sde!4v1620000000000!5m2!1sru!2sde"
            width="100%"
            height="300"
            style="border:0;"
            allowfullscreen=""
            loading="lazy"
            class="w-full h-full min-h-[300px] rounded-md"
          />
        </UCard>
      </div>
    </UPageSection>
  </main>
</template>