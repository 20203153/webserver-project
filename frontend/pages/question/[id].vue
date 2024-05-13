<script setup lang="ts">
import axios from 'axios'
import {useAuthStore} from "~/stores/auth";
import dayjs from "dayjs";
import type {Ref} from "vue";

interface IAnswers {
  id: number,
  subject: string,
  content: string,
  created_at: string,
  updated_at: string,
  owner: string,
  owner_id: number,
}

interface IQuestions {
  id: number,
  subject: string,
  content: string,
  created_at: string,
  updated_at: string,
  topic: Array<string>,
  owner: string,
  owner_id: number,
  hit: number
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
  answer: []
})

const answer_modify_id: Ref<number> = ref(0)
const answer = ref({
  content: '',
  question: 0
})
const M_answer = ref({
  content: '',
  question: 0,
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

const answer_modify_ready = async(id: number) => {
  const answers = data.value.answer.filter((d) => d.id === id)[0]
  if(answers.owner_id != user.userInfo.id) return

  M_answer.value.content = answers.content
  answer_modify_id.value = id
}

const answer_modify = async() => {
  console.log(M_answer.value.content)
  const response = await $fetch(`${BASE_URL}/pybo/answer/${route.params.id}/${answer_modify_id.value}/`, {
    method: 'PUT',
    body: M_answer.value,
    headers: {
      'Authorization': `Bearer ${user.token}`
    }
  })

  router.go(0)
}

const answer_delete = async(id: number) => {
  const response = await $fetch(`${BASE_URL}/pybo/answer/${route.params.id}/${id}/`, {
    method: 'DELETE',
    body: M_answer.value,
    headers: {
      'Authorization': `Bearer ${user.token}`
    }
  })

  router.go(0)
}

const question_delete = async() => {
  await user.getUserMeta()
  console.log(user.userInfo.id, data.value.owner_id)
  if(user.userInfo.id != data.value.owner_id) return;
  try {
    const response = await $fetch(`${BASE_URL}/pybo/${route.params.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${user.token}`
      }
    })
    await router.push('/')
  } catch(e) {
    console.log(e)
  }
}

try {
  const response = await axios.get(`${BASE_URL}/pybo/${route.params.id}`)
  data.value = response.data
  answer.value.question = data.value.id
  M_answer.value.question = data.value.id
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
        <div class="card-text" style="white-space: pre-line;">{{ data.content }}</div>
        <div class="d-flex justify-content-end">
          <div class="badge badge-light p-2 text-left mx-3" v-if="(new Date(data.created_at)).getTime() < (new Date(data.updated_at).getTime())">
            <div class="mb-2 text-black">modified at</div>
            <div class="text-black">{{ dayjs(data.updated_at).format('YYYY-MM-DD HH:mm:ss') }}</div>
          </div>
          <div class="badge badge-light p-2 text-left">
            <div class="mb-2 text-black">{{ data.owner }}</div>
            <div class="text-black">{{ dayjs(data.created_at).format('YYYY-MM-DD HH:mm:ss') }}</div>
          </div>
          <div class="my-3">
            <NuxtLink :href="`/question/modify_${data.id}`" class="btn btn-sm btn-outline-secondary" :disabled="user.userInfo.id != data.owner_id">수정</NuxtLink>
            <button class="btn btn-sm btn-danger" :disabled="user.userInfo.id != data.owner_id" @click="question_delete">삭제</button>
          </div>
        </div>
      </div>
    </div>
    <div class="mt-3" v-if="data.answer.length > 0">
      <div class="card my-3" v-for="answer in data.answer">
        <a v-bind:name="`comment_${answer.id}`"></a>
        <div class="card-body" v-if="answer_modify_id != answer.id">
          <div class="card-text" style="white-space: pre-line;">{{ answer.content }}</div>
          <span>
            - {{ answer.owner }}, {{ dayjs(answer.created_at).format('YYYY-MM-DD HH:mm:ss') }}
            <span v-if="(new Date(answer.created_at)).getTime() < (new Date(answer.updated_at).getTime())">
              수정: {{ dayjs(answer.updated_at).format('YYYY-MM-DD HH:mm:ss') }}
            </span>

            <button class="btn btn-sm btn-outline-secondary" :disabled="user.userInfo.id != answer.owner_id" type="button" @click="answer_modify_ready(answer.id)">수정</button>
            <button href="#" class="btn btn-sm btn-danger" :disabled="user.userInfo.id != answer.owner_id" type="button" @click="answer_delete(answer.id)">삭제</button>
          </span>
        </div>
        <form class="my-3" @submit.prevent="answer_modify" v-else>
          <div class="form-group">
            <textarea name="content" id="content" class="form-control" rows="10" v-model="M_answer.content" :disabled="!user.authenticated"></textarea>
            <input type="submit" value="답변 수정" class="btn btn-primary mt-2" :disabled="!user.authenticated || M_answer.content == ''">
          </div>
        </form>
      </div>
    </div>
    <form class="my-3" @submit.prevent="answer_create">
      <div class="form-group">
        <textarea name="content" id="content" class="form-control" rows="10" v-model="answer.content" v-bind:disabled="!user.authenticated"></textarea>
        <input type="submit" value="답변 등록" class="btn btn-primary mt-2" v-bind:disabled="!user.authenticated || answer.content == ''">
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