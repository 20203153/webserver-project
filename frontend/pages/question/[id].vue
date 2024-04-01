<script setup lang="ts">
import axios from 'axios'

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
const route = useRoute()

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

try {
  const response = await axios.get(`${runtimeConfig.public.BASE_URL}/pybo/${route.params.id}`)
  data.value = response.data
} catch (e) {
  console.log(e)
}
</script>

<script lang="ts">
export default {
  data() {
    return {
      form: {
        content: ""
      }
    }
  },
  methods: {
    async answer_create() {
      console.log(this.form.content)
    }
  }
}
</script>

<template>
<div class="container my-3">
  <h2 class="border-bottom py-2">{{ data.subject }}</h2>
  <div class="col-11">
    <div class="card">
      <div class="card-body">
        <div class="card-text" style="white-space: pre-line;">{{ data.content }}</div>
        <div class="d-flex justify-content-end">
          <div class="badge badge-light p-2 text-left mx-3" v-if="(new Date(data.created_at)).getTime() < (new Date(data.updated_at).getTime())">
            <div class="mb-2 text-black">modified at</div>
            <div class="text-black">{{ new Date(data.updated_at).toISOString().replace('T', ' ').slice(0, -5) }}</div>
          </div>
          <div class="badge badge-light p-2 text-left">
            <div class="mb-2 text-black">{{ data.owner }}</div>
            <div class="text-black">{{ new Date(data.updated_at).toISOString().replace('T', ' ').slice(0, -5) }}</div>
          </div>
          <div class="my-3">
            <a v-bind:href="`/question/edit/${route.params.id}`" class="btn btn-sm btn-outline-secondary">수정</a>
            <a v-bind:href="`/question/delete/${route.params.id}`" class="btn btn-sm btn-danger">삭제</a>
          </div>
        </div>
      </div>
    </div>
    <div class="mt-3" v-if="data.answer.length > 0">
      <div class="card my-3" v-for="answer in data.answer">
        <a v-bind:name="`comment_${answer.id}`"></a>
        <div class="card-body">
          <div class="card-text" style="white-space: pre-line;">{{ answer.content }}</div>
          <span>
            - {{ answer.owner }}, {{ new Date(answer.created_at).toISOString().replace('T', ' ').slice(0, -5)}}
            <span v-if="(new Date(answer.created_at)).getTime() < (new Date(answer.updated_at).getTime())">수정: {{ new Date(answer.updated_at).toISOString().replace('T', ' ').slice(0, -5) }} </span>

            <a href="#" class="btn btn-sm btn-outline-secondary">수정</a>
            <a href="#" class="btn btn-sm btn-danger">삭제</a>
          </span>
        </div>
      </div>
    </div>
    <form class="my-3" @submit.prevent="answer_create">
      <div class="form-group">
        <textarea name="content" id="content" class="form-control" rows="10" v-model="form.content"></textarea>
        <input type="submit" value="답변 등록" class="btn btn-primary mt-2">
      </div>
    </form>
  </div>
</div>
</template>

<style scoped>

</style>