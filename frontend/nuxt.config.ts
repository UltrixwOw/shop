// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devServer: {
    host: '127.0.0.1',
    port: 3000 // опционально
  },
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  runtimeConfig: {
    API_BASE_URL: 'https://meloni-backend.onrender.com/api',
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000/api'
    }
  },
  modules: ['@pinia/nuxt', '@vueuse/nuxt', '@nuxt/ui', '@nuxt/image', '@nuxtjs/i18n'],
  pinia: {
    storesDirs: ['./app/stores/**'],   // важно для Nuxt 4
  },
  vite: {
    optimizeDeps: {
      include: [
        '@vue/devtools-core',
        '@vue/devtools-kit',
        '@vueuse/core',
        'axios',
      ]
    }
  },
  routeRules: {
    '/backend/**': {
      proxy: 'https://meloni-backend.onrender.com/api/**'
    }
  },
  components: [
    {
      path: '~/components', // путь к компонентам
      pathPrefix: false,
    }
  ],
  css: ['~/assets/css/main.css'],
  colorMode: {
    preference: 'system',
    fallback: 'dark',
    classSuffix: ''
  },
  i18n: {
    locales: [
      { code: 'ru', name: 'Русский', file: 'ru.json', iso: 'ru-RU' },
      { code: 'en', name: 'English', file: 'en.json', iso: 'en-US' },
      { code: 'de', name: 'Deutsche', file: 'de.json', iso: 'de-DE' }
    ],
    defaultLocale: 'de',
    langDir: 'locales',
    strategy: 'prefix_except_default',
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'i18n_redirected',
      redirectOn: 'root'
    },
    vueI18n: 'i18n.config.ts',
  },
})