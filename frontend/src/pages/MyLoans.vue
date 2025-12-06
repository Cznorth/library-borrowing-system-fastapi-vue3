<template>
  <div>
    <h2>我的借阅</h2>
    <ul>
      <li v-for="l in loans" :key="l.id">
        借阅副本 {{ l.copy_id }} 到期 {{ new Date(l.due_date).toLocaleDateString() }}
        <button @click="renew(l.id)">续借</button>
        <button @click="ret(l.id)">归还</button>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import api from '../services/api'

const loans = ref<any[]>([])

async function load() {
  const { data } = await api.get('/loans/me')
  loans.value = data
}

onMounted(load)

async function renew(id: number) {
  await api.post(`/loans/${id}/renew`)
  await load()
}

async function ret(id: number) {
  await api.post(`/loans/${id}/return`)
  await load()
}
</script>

