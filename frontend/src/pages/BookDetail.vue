<template>
  <div>
    <h2>{{ book?.title }}</h2>
    <p>作者：{{ book?.author }}</p>
    <button v-for="c in copies" :key="c.id" :disabled="c.status!=='available'" @click="borrow(c.id)">
      借阅副本 {{ c.barcode }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const book = ref<any>(null)
const copies = ref<any[]>([])

onMounted(async () => {
  const id = route.params.id
  const { data } = await api.get(`/books/${id}`)
  book.value = data
  const { data: cds } = await api.get(`/copies/by-book/${id}`)
  copies.value = cds
})

async function borrow(copyId: number) {
  await api.post('/loans', null, { params: { copy_id: copyId } })
  alert('借阅成功')
}
</script>

