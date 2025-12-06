<template>
  <div>
    <h2>图书管理</h2>
    <form @submit.prevent="create">
      <input v-model="form.title" placeholder="书名" />
      <input v-model="form.author" placeholder="作者" />
      <input v-model="form.isbn" placeholder="ISBN" />
      <button type="submit">新增</button>
    </form>
    <ul>
      <li v-for="b in books" :key="b.id">{{ b.title }}
        <button @click="remove(b.id)">删除</button>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../services/api'

const books = ref<any[]>([])
const form = ref<any>({ title: '', author: '', isbn: '' })

async function load() {
  const { data } = await api.get('/books')
  books.value = data.items
}

onMounted(load)

async function create() {
  await api.post('/books', form.value)
  form.value = { title: '', author: '', isbn: '' }
  await load()
}

async function remove(id: number) {
  await api.delete(`/books/${id}`)
  await load()
}
</script>

