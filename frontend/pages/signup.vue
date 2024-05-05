<script setup lang="ts">
import type {Ref} from "vue";

const config = useRuntimeConfig()
const BASE_URL = config.public.backendUrl

useSeoMeta({
  title: `Pybo :: 회원가입`,
  ogTitle: `Pybo :: 회원가입`,
  ogType: 'website',
  ogSiteName: 'Pybo',
  ogDescription: 'Pybo의 Nuxt.js 구현체입니다.',
  ogImage: '/favicon.png',
})

const form = ref({
  id: "",
  password: "",
  password2: "",
  email: "",
  nickname: ""
})
const error: Ref<{[key: string]: string[]} | undefined> = ref()
const errorFields: {[key: string]: string} = {
  username: '사용자ID',
  email: '이메일',
  password: '비밀번호',
  password2: '비밀번호 확인',
  nickname: '닉네임'
}

const signupRequest = async () => {
  try {
    const result = await $fetch(`${BASE_URL}/users/register/`, {
      method: 'POST',
      body: {
        username: form.value.id,
        email: form.value.email,
        password: form.value.password,
        password2: form.value.password2,
        nickname: form.value.nickname
      }
    })
  } catch(e) {
    console.log(e)
    if(e?.response._data) {
      error.value = e?.response._data
    }
  }
}
</script>

<template>
  <div class="container my-3">
    <div class="alert alert-warning" v-for="(datas, key) in error">
      <h4 class="laert-heading">{{ errorFields[(key as string)] }} 필드의 문제!</h4>
      <p v-for="data in datas">{{ data }}</p>
    </div>
    <form @submit.prevent="signupRequest">
      <div class="mb-3">
        <label for="username">사용자ID</label>
        <input type="text" class="form-control" maxlength="20" v-model="form.id"/>
      </div>
      <div class="mb-3">
        <label for="password">비밀번호</label>
        <input type="password" class="form-control" maxlength="255" v-model="form.password"/>
      </div>
      <div class="mb-3">
        <label for="password2">비밀번호 확인</label>
        <input type="password" class="form-control" maxlength="255" v-model="form.password2"/>
      </div>
      <div class="mb-3">
        <label for="email">이메일</label>
        <input type="email" class="form-control" maxlength="255" v-model="form.email"/>
      </div>
      <div class="mb-3">
        <label for="nickname">닉네임</label>
        <input type="text" class="form-control"maxlength="20" v-model="form.nickname"/>
      </div>
      <button type="submit" class="btn btn-primary">생성하기</button>
    </form>
  </div>
</template>

<style scoped>

</style>