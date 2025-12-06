<template>
  <div class="login">
    <h1>登录</h1>
    <form @submit.prevent="onSubmit">
      <input v-model="username" placeholder="用户名" />
      <input v-model="password" type="password" placeholder="密码" />
      <button type="submit">登录</button>
    </form>
  </div>
  
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const username = ref('')
const password = ref('')

async function onSubmit() {
  const { data } = await axios.post('/api/auth/login', { username: username.value, password: password.value })
  localStorage.setItem('token', data.access_token)
  location.href = '/'
}
</script>

