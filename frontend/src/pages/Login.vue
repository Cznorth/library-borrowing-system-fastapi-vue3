<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>图书馆借阅系统</h2>
        </div>
      </template>
      <el-form :model="form" label-width="0px" @submit.prevent="onSubmit">
        <el-form-item>
          <el-input v-model="form.username" placeholder="用户名" prefix-icon="User" size="large" />
        </el-form-item>
        <el-form-item>
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            show-password
            size="large"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit" :loading="loading" style="width: 100%" size="large">
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'

const form = reactive({
  username: '',
  password: ''
})
const loading = ref(false)

async function onSubmit() {
  if (!form.username || !form.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  loading.value = true
  try {
    const { data } = await axios.post('/api/auth/login', {
      username: form.username,
      password: form.password
    })
    localStorage.setItem('token', data.access_token)
    ElMessage.success('登录成功')
    location.href = '/'
  } catch (error) {
    ElMessage.error('登录失败，请检查用户名或密码')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f2f5;
  background-image: url('https://images.unsplash.com/photo-1481627834876-b7833e8f5570?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
  background-size: cover;
}

.login-card {
  width: 400px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
}

.card-header {
  text-align: center;
  color: #303133;
}
</style>
