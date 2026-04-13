<script setup lang="ts">
// Метаданные страницы
definePageMeta({
  title: 'about_us'
})

const { t } = useI18n()
const localePath = useLocalePath();

// Ссылки для PageHero
const heroLinks = computed(() => [
  {
    label: t('our_products'),
    to: localePath('/products'),
    icon: 'i-heroicons-shopping-bag',
    color: 'primary' as const,
    size: 'lg' as const
  },
  {
    label: t('contact_us'),
    to: '#contact',
    color: 'neutral' as const,
    variant: 'subtle' as const,
    trailingIcon: 'i-heroicons-arrow-right',
    size: 'lg' as const
  }
])

// Команда компании
const teamMembers = ref([
  {
    name: 'Анна Смирнова',
    role: 'founder_ceo',
    description: 'founder_desc',
    avatar: {
      src: 'https://picsum.photos/id/64/400/400',
      alt: 'Анна Смирнова'
    }
  },
  {
    name: 'Михаил Волков',
    role: 'art_director',
    description: 'art_director_desc',
    avatar: {
      src: 'https://picsum.photos/id/1005/400/400',
      alt: 'Михаил Волков'
    }
  },
  {
    name: 'Екатерина Павлова',
    role: 'head_of_product',
    description: 'head_of_product_desc',
    avatar: {
      src: 'https://picsum.photos/id/1027/400/400',
      alt: 'Екатерина Павлова'
    }
  },
  {
    name: 'Дмитрий Соколов',
    role: 'cto',
    description: 'cto_desc',
    avatar: {
      src: 'https://picsum.photos/id/1043/400/400',
      alt: 'Дмитрий Соколов'
    }
  }
])

// Статистика компании
const stats = computed(() => [
  { 
    label: t('happy_customers'), 
    value: '5K+', 
    icon: 'i-heroicons-users' 
  },
  { 
    label: t('products_count'), 
    value: '10K+', 
    icon: 'i-heroicons-cube' 
  },
  { 
    label: t('countries'), 
    value: '15+', 
    icon: 'i-heroicons-globe-alt' 
  },
  { 
    label: t('support'), 
    value: '24/7', 
    icon: 'i-heroicons-chat-bubble-left-right' 
  }
])

// Ценности компании
const values = computed(() => [
  {
    title: t('quality'),
    description: t('quality_desc'),
    icon: 'i-heroicons-star'
  },
  {
    title: t('trust'),
    description: t('trust_desc'),
    icon: 'i-heroicons-hand-raised'
  },
  {
    title: t('innovation'),
    description: t('innovation_desc'),
    icon: 'i-heroicons-rocket-launch'
  },
  {
    title: t('care'),
    description: t('care_desc'),
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
</script>

<template>
  <main>
    <!-- PageHero компонент -->
    <UPageHero
      orientation="horizontal"
      :headline="$t('shop_welcome')"
      :title="$t('shop_subtitle')"
      :description="$t('brand_history')"
      :links="heroLinks"
    >
      <!-- Изображение для правой части -->
      <img
        src="https://picsum.photos/id/42/800/600"
        :alt="$t('about_us')"
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
      :title="$t('our_story')"
      :description="$t('story_text')"
      :headline="$t('about')"
      icon="i-heroicons-clock"
    >
      <!-- Галерея изображений в правой части -->
      <div class="grid grid-cols-2 gap-4">
        <div class="space-y-4">
          <img
            src="https://picsum.photos/id/26/400/300"
            alt="Warehouse"
            class="rounded-2xl w-full h-48 object-cover ring ring-default"
          />
          <img
            src="https://picsum.photos/id/27/400/300"
            alt="Packaging"
            class="rounded-2xl w-full h-40 object-cover ring ring-default"
          />
        </div>
        <div class="space-y-4 mt-8">
          <img
            src="https://picsum.photos/id/28/400/300"
            alt="Team"
            class="rounded-2xl w-full h-40 object-cover ring ring-default"
          />
          <img
            src="https://picsum.photos/id/29/400/300"
            alt="Store"
            class="rounded-2xl w-full h-48 object-cover ring ring-default"
          />
        </div>
      </div>
    </UPageSection>

    <!-- PageSection - Статистика -->
    <UPageSection
      :title="$t('stats_title')"
      :description="$t('stats_text')"
      headline="STATISTICS"
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
      :title="$t('our_values')"
      :description="$t('values_subtitle')"
      :headline="$t('values')"
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

    <!-- PageSection - Команда -->
    <UPageSection
      :title="$t('dream_team')"
      :description="$t('team_desc')"
      :headline="$t('who_we_are')"
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
          <p class="text-sm text-primary mb-2">{{ t(member.role) }}</p>
          <p class="text-xs text-muted mb-4">{{ t(member.description) }}</p>
        </UCard>
      </UPageGrid>
    </UPageSection>

    <!-- PageSection - Контакты -->
    <UPageSection
      id="contact"
      :title="$t('contact_title')"
      :description="$t('contact_desc')"
      :headline="$t('contacts')"
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