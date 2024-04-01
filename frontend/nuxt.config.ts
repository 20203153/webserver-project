// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    '@bootstrap-vue-next/nuxt'
  ],
  css: ['bootstrap/dist/css/bootstrap.min.css'],
  runtimeConfig: {
    public: {
      BASE_URL: process.env.BASE_URL || 'http://localhost:8000'
    }
  }
})
