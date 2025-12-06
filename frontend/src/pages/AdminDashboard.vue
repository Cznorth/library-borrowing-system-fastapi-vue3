<template>
  <div class="admin-container">
    <h2>管理员仪表盘</h2>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card shadow="hover" @click="$router.push('/admin/books')" class="admin-card">
          <div class="card-content">
            <el-icon :size="40" color="#409EFF"><Reading /></el-icon>
            <h3>图书管理</h3>
            <p>添加、编辑、删除图书及副本</p>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" @click="$router.push('/admin/users')" class="admin-card">
          <div class="card-content">
             <el-icon :size="40" color="#67C23A"><User /></el-icon>
            <h3>用户管理</h3>
            <p>查看用户列表、权限管理</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { Reading, User } from '@element-plus/icons-vue'
</script>

<style scoped>
.admin-container {
  max-width: 1000px;
  margin: 0 auto;
}

.admin-card {
  cursor: pointer;
  text-align: center;
  height: 100%;
  transition: transform 0.2s;
}

.admin-card:hover {
  transform: translateY(-5px);
}

.card-content {
  padding: 20px;
}

h3 {
  margin: 10px 0;
}

p {
  color: #909399;
  font-size: 14px;
}
</style>
