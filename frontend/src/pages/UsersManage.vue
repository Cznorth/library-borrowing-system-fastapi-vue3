<template>
  <div>
    <h2>用户管理</h2>
    <ul>
      <li v-for="u in users" :key="u.id">
        {{ u.username }} - {{ u.role }}
        <button @click="del(u.id)">删除</button>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import api from '../services/api'

const users = ref<any[]>([])

async function load() {
  const { data } = await api.get('/admin/users')
  users.value = data.items
}

onMounted(load)

async function del(id: number) {
  await api.delete(`/admin/users/${id}`)
  await load()
}
</script>

