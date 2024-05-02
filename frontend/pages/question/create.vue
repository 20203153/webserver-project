<script setup lang="ts">
import axios from "axios";
import { useAuthStore } from "~/stores/auth";

useSeoMeta({
  title: `Pybo :: 질문쓰기`,
  ogTitle: `Pybo :: 질문쓰기`,
  ogType: 'website',
  ogSiteName: 'Pybo',
  ogDescription: 'Pybo의 Nuxt.js 구현체입니다.',
  ogImage: '/favicon.png',
})

const question = ref({
  subject: '',
  content: '',
  topic: ['토픽1']
})

const runtimeConfig = useRuntimeConfig()
const router = useRouter()
const route = useRoute()
const user = useAuthStore()

const question_create = async () => {
  if(question.value.subject == '' || question.value.content == '') return

  try {
    const response = await axios.post(`${runtimeConfig.public.BASE_URL}/pybo/question/`, question.value, {
      headers: {
        'Authorization': `Bearer ${user.token}`
      }
    })
    await router.push('/1')
  } catch(e) {
    console.log(e)
  }

}
</script>

<template>
<div class="container">
  <h5 class="my-3 border-bottom pb-2">질문 등록</h5>
  <form class="post-form my-3" @submit.prevent="question_create">
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