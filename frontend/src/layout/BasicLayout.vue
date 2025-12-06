<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <div class="header-content">
          <div class="logo">
            <el-icon :size="30" color="#409EFF"><Reading /></el-icon>
            <span class="title">图书馆借阅系统</span>
          </div>
          <div class="menu">
            <el-menu
              mode="horizontal"
              :router="true"
              :default-active="$route.path"
            >
              <el-menu-item index="/">首页</el-menu-item>
              <el-sub-menu index="/me">
                <template #title>我的图书馆</template>
                <el-menu-item index="/me/loans">我的借阅</el-menu-item>
                <el-menu-item index="/me/reservations">我的预约</el-menu-item>
                <el-menu-item index="/me/fines">我的罚金</el-menu-item>
              </el-sub-menu>
              <el-menu-item v-if="authStore.user?.role === 'admin'" index="/admin">后台管理</el-menu-item>
            </el-menu>
          </div>
          <div class="user-actions">
            <template v-if="authStore.user">
              <span class="username">{{ authStore.user.full_name || authStore.user.username }}</span>
              <el-button type="danger" link @click="handleLogout">退出</el-button>
            </template>
            <template v-else>
              <el-button type="primary" link @click="$router.push('/login')">登录</el-button>
              <el-button type="success" link @click="$router.push('/register')">注册</el-button>
            </template>
          </div>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
      <el-footer>
        <p>© 2024 图书馆借阅系统 - 软件工程实验</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
}
</script>

<style scoped>
.common-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.el-container {
  height: 100%;
}

.el-header {
  background-color: #fff;
  border-bottom: 1px solid #dcdfe6;
  padding: 0 20px;
  height: 60px;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.title {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}

.menu {
  flex: 1;
  margin: 0 40px;
}

.el-menu {
  border-bottom: none;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.username {
  font-size: 14px;
  color: #606266;
}

.el-main {
  background-color: #f5f7fa;
  padding: 20px;
}

.el-footer {
  text-align: center;
  color: #909399;
  font-size: 12px;
  padding: 20px;
  background-color: #fff;
  border-top: 1px solid #ebeef5;
}
</style>
