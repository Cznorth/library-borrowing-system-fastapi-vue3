<template>
  <div>
    <h2>图书管理</h2>
    <div style="margin-bottom: 12px;">
      <input v-model="keyword" placeholder="关键字导入（如：计算机）" />
      <input v-model.number="limit" type="number" min="1" max="50" placeholder="数量" />
      <button @click="importByKeyword">按关键字导入</button>
    </div>
    <div style="margin-bottom: 12px;">
      <input v-model="isbnInput" placeholder="ISBN 导入（单个）" />
      <button @click="importByIsbn">按 ISBN 导入</button>
    </div>
    <div style="margin-bottom: 12px;">
      <input type="file" @change="onFile" accept=".csv,.json" />
      <button @click="importFile" :disabled="!file">上传文件批量导入</button>
    </div>
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
import api, { importBooksByKeyword, importBooksByIsbn, bulkImportBooks } from '../services/api'

const books = ref<any[]>([])
const form = ref<any>({ title: '', author: '', isbn: '' })
const keyword = ref('')
const limit = ref(10)
const isbnInput = ref('')
const file = ref<File | null>(null)

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

async function importByKeyword() {
  if (!keyword.value) return
  await importBooksByKeyword(keyword.value, limit.value)
  await load()
}

async function importByIsbn() {
  if (!isbnInput.value) return
  await importBooksByIsbn(isbnInput.value)
  isbnInput.value = ''
  await load()
}

function onFile(e: Event) {
  const t = e.target as HTMLInputElement
  file.value = t.files && t.files[0] ? t.files[0] : null
}

async function importFile() {
  if (!file.value) return
  await bulkImportBooks(file.value)
  file.value = null
  await load()
}
</script>

