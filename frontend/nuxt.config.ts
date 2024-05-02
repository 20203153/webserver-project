// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  build: {
    transpile: ['Dayjs'],
  },
  modules: [
    '@pinia/nuxt',
    '@bootstrap-vue-next/nuxt'
  ],
  imports: {
    dirs: ['./stores']
  },
  pinia: {
    // @ts-ignore
    autoImports: ['defineStore', 'acceptHMRUpdate']
  },
  css: ['bootstrap/dist/css/bootstrap.min.css'],
  runtimeConfig: {
    public: {
      BASE_URL: process.env.BASE_URL || 'http://localhost:8000'
    }
  }
})
