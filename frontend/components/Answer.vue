<script setup lang="ts">
import dayjs from "dayjs";
import {useAuthStore} from "~/stores/auth";
import type { IAnswers } from "~/pages/question/[id].vue";

const props = defineProps<{ answer: IAnswers, questionId: number }>()
const answer = props.answer

const runtimeConfig = useRuntimeConfig()
const router = useRouter()
const route = useRoute()
const user = useAuthStore()
const BASE_URL = runtimeConfig.public.backendUrl

const answerModify = ref(false)
const M_answer = ref({
  content: answer.content,
  question: props.questionId,
})

const answer_modify_ready = async(id: number) => {
  if (answer.owner_id != user.userInfo.id) return
  answerModify.value = true
}


const answer_modify = async() => {
  console.log(M_answer.value.content)
  const response = await $fetch(`${BASE_URL}/pybo/answer/${route.params.id}/${answer.id}/`, {
    method: 'PUT',
    body: M_answer.value,
    headers: {
      'Authorization': `Bearer ${user.token}`
    }
  })

  router.go(0)
}

const answer_delete = async(id: number) => {
  const response = await $fetch(`${BASE_URL}/pybo/answer/${route.params.id}/${answer.id}/`, {
    method: 'DELETE',
    body: M_answer.value,
    headers: {
      'Authorization': `Bearer ${user.token}`
    }
  })

  router.go(0)
}

const answer_vote = async() => {
  await user.getUserMeta()

  if(user.userInfo.id == answer.owner_id) return;
  try {
    await $fetch(`${BASE_URL}/pybo/vote/answer/${answer.id}/`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${user.token}`
      }
    })
    router.go(0)
  } catch (e) {
    console.log(e)
  }
}
</script>

<template>
  <div class="card my-3">
    <a v-bind:id="`comment_${answer.id}`"></a>
    <div class="card-body" v-if="!answerModify">
      <div class="card-text" style="white-space: pre-line;">{{ answer.content }}</div>
      <span>
        - {{ answer.owner }}, {{ dayjs(answer.created_at).format('YYYY-MM-DD HH:mm:ss') }}
        <span v-if="(new Date(answer.created_at)).getTime() < (new Date(answer.updated_at).getTime())">
          수정: {{ dayjs(answer.updated_at).format('YYYY-MM-DD HH:mm:ss') }} &nbsp;
        </span>
      </span>
      <div class="d-flex justify-content-end">
        <div class="my-3" v-if="user.userInfo.id != answer.owner_id">
          <button class="recommend btn btn-sm btn-outline-secondary" type="button" @click="answer_vote" :disabled="!user.authenticated"> 추천 &nbsp;
            <span class="badge rounded-pill bg-success">{{answer.vote}}</span>
          </button>
        </div>
        <div class="my-3" v-else>
          <button class="btn btn-sm btn-outline-secondary" :disabled="user.userInfo.id != answer.owner_id" type="button" @click="answer_modify_ready(answer.id)">수정</button>
          <button href="#" class="btn btn-sm btn-danger" :disabled="user.userInfo.id != answer.owner_id" type="button" @click="answer_delete(answer.id)">삭제</button>
        </div>
      </div>
    </div>
    <form class="my-3" @submit.prevent="answer_modify" v-else style="padding-left: 10px; padding-right: 10px;">
      <div class="form-group">
        <textarea name="content" id="content" class="form-control" rows="10" v-model="M_answer.content" :disabled="!user.authenticated" />
        <input type="submit" value="답변 수정" class="btn btn-primary mt-2" :disabled="!user.authenticated || M_answer.content == ''">
      </div>
    </form>
  </div>
</template>

<style scoped>

</style>