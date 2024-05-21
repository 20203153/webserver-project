<script setup lang="ts">
import {useAuthStore} from "~/stores/auth"
import dayjs from "dayjs"
import {MdEditor} from "md-editor-v3";

export interface IAnswers {
  id: number,
  subject: string,
  content: string,
  created_at: string,
  updated_at: string,
  owner: string,
  owner_id: number,
  vote: number,
}

export interface IQuestions {
  id: number,
  subject: string,
  content: string,
  created_at: string,
  updated_at: string,
  topic: Array<string>,
  owner: string,
  owner_id: number,
  hit: number,
  vote: number,
  answer: Array<IAnswers>,
}

const runtimeConfig = useRuntimeConfig()
const router = useRouter()
const route = useRoute()
const user = useAuthStore()
const BASE_URL = runtimeConfig.public.backendUrl

const isError = ref(false)
const data = ref<IQuestions>({
  id: 0,
  subject: '',
  content: '',
  created_at: '',
  updated_at: '',
  topic: [],
  owner: '',
  owner_id: 0,
  hit: 0,
  vote: 0,
  answer: []
})

const answer = ref({
  content: '',
  question: 0
})

const answer_create = async () => {
  console.log(answer.value.content)
  const response = await $fetch(`${BASE_URL}/pybo/answer/${route.params.id}/`, {
    method: 'POST',
    body: answer.value,
    headers: {
      'Authorization': `Bearer ${user.token}`
    }
  })

  router.go(0)
}

const question_delete = async() =>
{
  await user.getUserMeta()
  console.log(user.userInfo.id, data.value.owner_id)
  if(user.userInfo.id != data.value.owner_id) return;
  try {
    await $fetch(`${BASE_URL}/pybo/question/${route.params.id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${user.token}`
      }
    });
    await router.push('/')
  } catch(e) {
    console.log(e)
  }
}


const question_vote = async() => {
  await user.getUserMeta()

  if(user.userInfo.id == data.value.owner_id) return;
  try {
    data.value = await $fetch(`${BASE_URL}/pybo/vote/question/${route.params.id}/`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${user.token}`
      }
    })
  } catch (e) {
    console.log(e)
  }
}

try {
  await user.getUserMeta()

  data.value = await $fetch(`${BASE_URL}/pybo/${route.params.id}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${user.token}`
    }
  })
  answer.value.question = data.value.id

  useSeoMeta({
    title: `Pybo :: ${data.value.subject}`,
    ogTitle: `Pybo :: ${data.value.subject}`,
    ogType: 'website',
    ogSiteName: 'Pybo',
    ogDescription: 'Pybo의 Nuxt.js 구현체입니다.',
    ogImage: '/favicon.png',
  })
} catch (error) {
  console.log(error)
  isError.value = true
  router.push('/')
}
</script>

<template>
<div class="container my-3" v-if="!isError">
  <h2 class="border-bottom py-2">{{ data.subject }}</h2>
  <div class="col-11">
    <div class="card">
      <div class="card-body">
        <div class="card-text" style="white-space: pre-line;"
          v-html="$mdRenderer.render(data.content)"
        />
        <div class="d-flex justify-content-end">
          <div class="badge badge-light p-2 text-left mx-3" v-if="(new Date(data.created_at)).getTime() < (new Date(data.updated_at).getTime())">
            <div class="mb-2 text-black">modified at</div>
            <div class="text-black">{{ dayjs(data.updated_at).format('YYYY-MM-DD HH:mm:ss') }}</div>
          </div>
          <div class="badge badge-light p-2 text-left">
            <div class="mb-2 text-black">{{ data.owner }}</div>
            <div class="text-black">{{ dayjs(data.created_at).format('YYYY-MM-DD HH:mm:ss') }}</div>
          </div>
          <div class="my-3" v-if="user.userInfo.id != data.owner_id">
            <button class="recommend btn btn-sm btn-outline-secondary" type="button" @click="question_vote" :disabled="!user.authenticated"> 추천 &nbsp;
              <span class="badge rounded-pill bg-success">{{data.vote}}</span>
            </button>
          </div>
          <div class="my-3" v-else>
            <NuxtLink :href="`/question/modify_${data.id}`" class="btn btn-sm btn-outline-secondary" :disabled="user.userInfo.id != data.owner_id">수정</NuxtLink>
            <button class="btn btn-sm btn-danger" :disabled="user.userInfo.id != data.owner_id" @click="question_delete">삭제</button>
          </div>
        </div>
      </div>
    </div>
    <div class="mt-3" v-if="data.answer.length > 0">
      <Answer v-for="answer in data.answer" :answer="answer" :id="`answer_${data.id}`" :questionId="data.id" />
    </div>
    <form class="my-3" @submit.prevent="answer_create">
      <div class="form-group">
        <MdEditor language="en-US" v-model="answer.content" :disabled="!user.authenticated" />
        <input type="submit" value="답변 등록" class="btn btn-primary mt-2" :disabled="!user.authenticated || answer.content == ''">
      </div>
    </form>
  </div>

  <button class="btn btn-primary mt-2" @click="user.refresh(); user.getUserMeta()">refresh</button>
</div>
</template>

<style scoped>
  [disabled] {
    pointer-events: none;
  }
</style>