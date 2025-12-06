<template>
  <div>
    <h2>我的预约</h2>
    <ul>
      <li v-for="r in reservations" :key="r.id">
        书目 {{ r.book_id }} 状态 {{ r.status }}
        <button @click="cancel(r.id)">取消</button>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import api from '../services/api'

const reservations = ref<any[]>([])

async function load() {
  const { data } = await api.get('/reservations/me')
  reservations.value = data
}

onMounted(load)

async function cancel(id: number) {
  await api.post(`/reservations/${id}/cancel`)
  await load()
}
</script>

