<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>用户注册</h2>
        </div>
      </template>
      <el-form :model="form" label-width="0px" @submit.prevent="onSubmit">
        <el-form-item>
          <el-input v-model="form.username" placeholder="用户名" prefix-icon="User" size="large" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.email" placeholder="邮箱" prefix-icon="Message" size="large" />
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
          <el-input
            v-model="form.confirm"
            type="password"
            placeholder="确认密码"
            prefix-icon="Lock"
            show-password
            size="large"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit" :loading="loading" style="width: 100%" size="large">
            注册
          </el-button>
        </el-form-item>
        <el-form-item>
          <div style="text-align:center; width: 100%">
            <el-link type="primary" @click="$router.push('/login')">已有账号？去登录</el-link>
          </div>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
  </template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { User, Lock, Message } from '@element-plus/icons-vue'

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirm: ''
})
const loading = ref(false)

async function onSubmit() {
  if (!form.username || !form.email || !form.password || !form.confirm) {
    ElMessage.warning('请完整填写信息')
    return
  }
  if (form.password !== form.confirm) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }
  loading.value = true
  try {
    await axios.post('/api/auth/register', {
      username: form.username,
      email: form.email,
      password: form.password,
      role: 'reader'
    })
    ElMessage.success('注册成功，请登录')
    location.href = '/login'
  } catch (error) {
    ElMessage.error('注册失败，请检查输入信息')
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
