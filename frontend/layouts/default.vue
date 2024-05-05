<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

const auth = useAuthStore()
const route = useRoute()

const runtimeConfig = useRuntimeConfig()
const BASE_URL = runtimeConfig.public.backendUrl

watch(() => route.path, async () => {
  await auth.refresh()
})

;(async() => {
  await auth.getUserMeta()
})()
</script>

<template>
  <BNavbar toggleable="lg" variant="primary" v-b-color-mode="'dark'">
    <BNavbarBrand href="/">Pybo</BNavbarBrand>
    <BNavbarToggle target="nav-collapse"/>
    <BCollapse id="nav-collapse" is-nav>
      <BNavbarNav>
        <BNavItem href="/">질문</BNavItem>
      </BNavbarNav>
      <BNavbarNav class="ms-auto mb-2 mb-lg-0" v-if="auth.authenticated">
        <BNavItem>
          <img :src="`${BASE_URL}/media/${auth.userInfo.image ?? 'default.png'}`" style="width:25px;" alt=""> &nbsp;{{ auth.userInfo.nickname }}
        </BNavItem>
        <BNavItem href="/logout">로그아웃</BNavItem>
      </BNavbarNav>
      <BNavbarNav class="ms-auto mb-2 mb-lg-0" v-else>
        <BNavItem href="/signup">회원가입</BNavItem>
        <BNavItem href="/login">로그인</BNavItem>
      </BNavbarNav>
    </BCollapse>
  </BNavbar>

  <slot/>
</template>

<style scoped>

</style>