<template>
  <div>
    <h1>图书馆借阅系统</h1>
    <input v-model="q" placeholder="搜索书名或作者" />
    <button @click="search">搜索</button>
    <ul>
      <li v-for="b in books" :key="b.id">{{ b.title }} - {{ b.author }}</li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const q = ref('')
const books = ref<any[]>([])

async function search() {
  const { data } = await axios.get('/api/books', { params: { q: q.value } })
  books.value = data.items
}
</script>

