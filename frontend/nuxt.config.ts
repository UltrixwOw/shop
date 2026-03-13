// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devServer: {
    host: '127.0.0.1',
    port: 8000 // опционально
  },
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000/api'
    }
  },
  modules: ['@pinia/nuxt', '@nuxt/ui', '@nuxt/image'],
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
})