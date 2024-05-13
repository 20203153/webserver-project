<script setup lang="ts">
import axios from "axios";
import { useAuthStore } from "~/stores/auth";

const runtimeConfig = useRuntimeConfig()
const router = useRouter()
const route = useRoute()
const user = useAuthStore()

const BASE_URL = runtimeConfig.public.backendUrl

useSeoMeta({
  title: `Pybo :: 질문수정 :: ${route.params.id}`,
  ogTitle: `Pybo :: 질문수정 :: ${route.params.id}`,
  ogType: 'website',
  ogSiteName: 'Pybo',
  ogDescription: 'Pybo의 Nuxt.js 구현체입니다.',
  ogImage: '/favicon.png',
})

const question = ref({
  subject: '',
  content: '',
  topic: ['']
})

const get_question = async () => {
  const response = await axios.get(`${BASE_URL}/pybo/${route.params.id}`)
  question.value = response.data
}

const question_modify = async () => {
  if(question.value.subject == '' || question.value.content == '') return

  try {
    const response = await axios.put(`${runtimeConfig.public.backendUrl}/pybo/question/${route.params.id}/`, question.value, {
      headers: {
        'Authorization': `Bearer ${user.token}`
      }
    })
    await router.push('/1')
  } catch(e) {
    console.log(e)
  }
}

;(async() => {
  await get_question()
})()
</script>

<template>
<div class="container">
  <h5 class="my-3 border-bottom pb-2">질문 수정</h5>
  <form class="post-form my-3" @submit.prevent="question_modify">
    <div class="form-group">
      <label for="subject">제목</label>
      <input type="text" class="form-control" name="subject" id="subject" v-model="question.subject" />
    </div>
    <div>
      <label for="tags">토픽</label>
      <b-form-tags input-id="tags" v-model="question.topic" separator=" ,;" no-add-on-enter placeholder="공백, 콤마, 세미콜론으로 토픽을 추가하세요." />
    </div>
    <div class="form-group">
      <label for="content">내용</label>
      <textarea class="form-control" name="content" id="content" v-model="question.content" rows="10"/>
    </div>
    <div class="form-group">
      <button type="submit" class="btn btn-primary" v-bind:class="(question.subject != '' && question.content != '' ? '' : 'disabled')">저장하기</button>
    </div>
  </form>
</div>
</template>

<style scoped>

</style>