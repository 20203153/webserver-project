<script setup lang="ts">

</script>

<template>
  <BNavbar toggleable="lg" variant="primary" v-b-color-mode="'dark'">
    <BNavbarBrand href="#">Pybo</BNavbarBrand>
    <BNavbarToggle target="nav-collapse"/>
    <BCollapse id="nav-collapse" is-nav>
      <BNavbarNav>
        <BNavItem href="#">Link</BNavItem>
      </BNavbarNav>
      <BNavbarNav class="ms-auto mb-2 mb-lg-0">
        <BNavItem href="/login">Login</BNavItem>
      </BNavbarNav>
    </BCollapse>
  </BNavbar>

  <slot/>
</template>

<style scoped>

</style>