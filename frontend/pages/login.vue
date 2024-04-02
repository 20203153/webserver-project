<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useAuthStore } from '~/stores/auth'

const user = ref({
  username: '',
  password: ''
})

const router = useRouter()

const authStore = useAuthStore()

const login = async() => {
  await authStore.authUser(user.value)

  if (authStore.authenticated) {
    await router.push('/')
  }
}
</script>

<template>
<div class="container my-3">
  <form @submit.prevent="login">
    <div class="mb-3">
      <label for="username">사용자ID</label>
      <input type="text" class="form-control" v-model="user.username"/>
    </div>
    <div class="mb-3">
      <label for="password">비밀번호</label>
      <input type="password" class="form-control" v-model="user.password"/>
    </div>
    <button type="submit" class="btn btn-primary">로그인</button>
  </form>
</div>
</template>

<style scoped>

</style>