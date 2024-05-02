<script lang="ts">
useSeoMeta({
  title: `Pybo :: 회원가입`,
  ogTitle: `Pybo :: 회원가입`,
  ogType: 'website',
  ogSiteName: 'Pybo',
  ogDescription: 'Pybo의 Nuxt.js 구현체입니다.',
  ogImage: '/favicon.png',
})

export default {
  data() {
    return {
      form: {
        id: "",
        password: "",
        password2: "",
        email: ""
      }
    }
  },
  methods: {
    async signup() {
      console.log(this.form.id)
    }
  }
}
</script>

<template>
<div class="container my-3">
  <form @submit.prevent="signup">
    <div class="mb-3">
      <label for="username">사용자ID</label>
      <input type="text" class="form-control" v-model="form.id"/>
    </div>
    <div class="mb-3">
      <label for="password">비밀번호</label>
      <input type="password" class="form-control" v-model="form.password"/>
    </div>
    <div class="mb-3">
      <label for="password2">비밀번호 확인</label>
      <input type="password2" class="form-control" v-model="form.password2"/>
    </div>
    <div class="mb-3">
      <label for="email">이메일</label>
      <input type="text" class="form-control" v-model="form.email"/>
    </div>
    <button type="submit" class="btn btn-primary">생성하기</button>
  </form>
</div>
</template>

<style scoped>

</style>