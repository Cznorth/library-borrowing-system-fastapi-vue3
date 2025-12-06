<template>
  <div>
    <h2>我的罚金</h2>
    <ul>
      <li v-for="f in fines" :key="f.id">
        金额 {{ f.amount }} 状态 {{ f.status }}
        <button :disabled="f.status==='paid'" @click="pay(f.id)">缴纳</button>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import api from '../services/api'

const fines = ref<any[]>([])

async function load() {
  const { data } = await api.get('/fines/me')
  fines.value = data
}

onMounted(load)

async function pay(id: number) {
  await api.post(`/fines/${id}/pay`)
  await load()
}
</script>

