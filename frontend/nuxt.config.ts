// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  srcDir: 'app/',
  devServer: {
    host: '127.0.0.1',
    port: 3000 // опционально
  },
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  runtimeConfig: {
    public: {
      apiBase: 'http://127.0.0.1:8000/api' // Django API
    }
  },
  modules: ['@pinia/nuxt', '@nuxt/ui'],
  pinia: {
    storesDirs: ['./app/stores/**'],   // важно для Nuxt 4
  },
  components: [
    {
      path: '~/components', // путь к компонентам
      pathPrefix: false,
    }
  ],
  css: ['~/assets/css/main.css'],
  
})
