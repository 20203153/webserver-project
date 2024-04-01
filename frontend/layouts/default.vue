<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
const authStore = useAuthStore()
</script>

<template>
  <BNavbar toggleable="lg" variant="primary" v-b-color-mode="'dark'">
    <BNavbarBrand href="/">Pybo</BNavbarBrand>
    <BNavbarToggle target="nav-collapse"/>
    <BCollapse id="nav-collapse" is-nav>
      <BNavbarNav>
        <BNavItem href="#">Link</BNavItem>
      </BNavbarNav>
      <BNavbarNav class="ms-auto mb-2 mb-lg-0">
        <BNavItem href="/login" v-if="!authStore.authenticated">Login</BNavItem>
        <BNavItem href="/logout" v-else>Logout</BNavItem>
      </BNavbarNav>
    </BCollapse>
  </BNavbar>

  <slot/>
</template>

<style scoped>

</style>