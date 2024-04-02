<script setup lang="ts">
import axios from 'axios'
import {useAuthStore} from "~/stores/auth";

const user = useAuthStore()

interface IQuestions {
  id: number,
  subject: string,
  created_at: string,
  updated_at: string,
  topic: Array<string>,
  owner: string,
  owner_id: number,
  hit: number
}

interface IQuestionResponse {
  count: number,
  next: string,
  previous: string,
  results: Array<IQuestions>
}

const runtimeConfig = useRuntimeConfig()

const data = ref<IQuestionResponse>({
  count: 0,
  next: '',
  previous: '',
  results: []
})

try {
  const response = await axios.get(`${runtimeConfig.public.BASE_URL}/pybo`)
  data.value = response.data
} catch (e) {
  console.log(e)
}

</script>

<template>
  <div class="container my-3">
    <BTableSimple>
      <BThead head-variant="dark">
        <BTr>
          <BTh>번호</BTh>
          <BTh style="width: 50%">제목</BTh>
          <BTh>글쓴이</BTh>
          <BTh>작성 일자</BTh>
          <BTh>조회수</BTh>
        </BTr>
      </BThead>
      <BTbody>
        <BTr v-for="question in data.results">
          <BTh>{{ question.id }}</BTh>
          <BTh><nuxt-link v-bind:to="`/question/${question.id}`">{{ question.subject }}</nuxt-link></BTh>
          <BTh>{{ question.owner }}</BTh>
          <!-- https://gurtn.tistory.com/65 -->
          <BTh>{{ new Date(question.created_at).toISOString().replace('T', ' ').slice(0, -5) }}</BTh>
          <BTh>{{ question.hit }}</BTh>
        </BTr>
      </BTbody>
    </BTableSimple>

    <nuxt-link to="/question/create" class="btn btn-primary" v-if="user.authenticated">
        질문 등록하기
    </nuxt-link>
  </div>
</template>

<style scoped>

</style>