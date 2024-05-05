<script setup lang="ts">
import axios from 'axios'
import dayjs from 'dayjs'
import {useAuthStore} from "~/stores/auth";
import type {Ref} from "vue";
import {runtime} from "std-env";

const route = useRoute()
const user = useAuthStore()

const currentPage = ref(parseInt(route.params.id as string))
const currentTopic: Ref<string[]> = ref([])
const pageList: Ref<number[]> = ref([])

const runtimeConfig = useRuntimeConfig()
const BASE_URL = runtimeConfig.public.backendUrl

useSeoMeta({
  title: `Pybo :: 질문 - ${currentPage.value}페이지`,
  ogTitle: `Pybo :: 질문 - ${currentPage.value}페이지`,
  ogType: 'website',
  ogSiteName: 'Pybo',
  ogDescription: 'Pybo의 Nuxt.js 구현체입니다.',
  ogImage: '/favicon.png',
})

interface IQuestions {
  id: number,
  subject: string,
  created_at: string,
  updated_at: string,
  topic: Array<string>,
  owner: string,
  owner_id: number,
  hit: number,
  answers: number
}

interface IQuestionResponse {
  count: number,
  next: string,
  previous: string,
  results: Array<IQuestions>
}

const data = ref<IQuestionResponse>({
  count: 0,
  next: '',
  previous: '',
  results: []
})

const calculatePageList = (currentPage: number, totalPage: number, pageRange: number = 5): number[] => {
  const maxPage = Math.min(totalPage, currentPage + pageRange);
  const minPage = Math.max(1, currentPage - pageRange);

  const pageList: number[] = [];
  for (let i = minPage; i <= maxPage; i++) {
    pageList.push(i);
  }

  return pageList;
}

const getPage = async() => {
  const response = await axios.get(`${BASE_URL}/pybo/?page=${currentPage.value}${currentTopic.value.length > 0 ? `&topic=${currentTopic.value.join(',')}` : ''}`)
  data.value = response.data

  pageList.value = calculatePageList(currentPage.value, Math.ceil(data.value.count / 10))
}

try {
  getPage()
} catch (e) {
  console.log(e)
}

</script>

<template>
  <div class="container my-3">
    <div style="margin-bottom: 2em;">
      <label for="tags">토픽</label>
      <b-form-tags input-id="tags" v-model="currentTopic" separator=" ,;" no-add-on-enter placeholder="공백, 콤마, 세미콜론으로 토픽을 추가하세요." @input="getPage()">
        <b-form-tag v-for="topic in currentTopic" :key="topic" :title="topic" @remove="currentTopic = currentTopic.filter((v) => v != topic); getPage()"></b-form-tag>
      </b-form-tags>
    </div>
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
          <BTh>
            <nuxt-link v-bind:to="`/question/${question.id}`">{{ question.subject }}</nuxt-link>
            <span class="text-danger small mx-2" v-if="question.answers > 0">{{ question.answers }}</span>
            <span class="small mx-2" v-for="topic in question.topic" @click="currentTopic.push(topic); getPage()" style="cursor: pointer">#{{ topic }}</span>
          </BTh>
          <BTh>{{ question.owner }}</BTh>
          <BTh>{{ dayjs(question.created_at).format('YYYY-MM-DD HH:mm:ss') }}</BTh>
          <BTh>{{ question.hit }}</BTh>
        </BTr>
      </BTbody>
    </BTableSimple>

    <!-- 페이징처리 시작 -->
    <ul class="pagination justify-content-center">
        <!-- 이전페이지 -->
        <li class="page-item" v-if="currentPage - 1 > 0">
            <NuxtLink class="page-link" :to="`/${currentPage - 1}`">이전</NuxtLink>
        </li>
        <li class="page-item disabled" v-else>
            <a class="page-link" tabindex="-1" aria-disabled="true" href="#">이전</a>
        </li>
        <!-- 페이지리스트 -->
        <li class="page-item" :class="{ 'active': currentPage === idx }" v-for="idx in pageList" :key="idx">
          <NuxtLink class="page-link" :to="`/${idx}`">{{ idx }}</NuxtLink>
        </li>
        <!-- 다음페이지 -->
        <li class="page-item" v-if="currentPage < Math.ceil(data.count / 10)">
            <NuxtLink class="page-link" :to="`/${currentPage + 1}`">다음</NuxtLink>
        </li>
        <li class="page-item disabled" v-else>
            <a class="page-link" tabindex="-1" aria-disabled="true" href="#">다음</a>
        </li>
    </ul>
    <!-- 페이징처리 끝 -->

    <nuxt-link to="/question/create" class="btn btn-primary" v-if="user.authenticated">
        질문 등록하기
    </nuxt-link>
  </div>
</template>

<style scoped>

</style>