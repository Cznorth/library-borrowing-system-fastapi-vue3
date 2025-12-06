<template>
  <div class="page-container">
    <el-card header="我的预约">
      <el-table :data="reservations" stripe>
        <el-table-column label="图书" prop="book.title">
           <template #default="scope">
             {{ scope.row.book?.title || '书目ID: ' + scope.row.book_id }}
           </template>
        </el-table-column>
        <el-table-column label="预约日期" prop="reservation_date">
           <template #default="scope">
            {{ new Date(scope.row.reservation_date).toLocaleDateString() }}
          </template>
        </el-table-column>
        <el-table-column label="状态" prop="status">
          <template #default="scope">
            <el-tag>{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button
              size="small"
              type="danger"
              @click="cancel(scope.row.id)"
              :disabled="scope.row.status !== 'active' && scope.row.status !== 'pending'"
            >
              取消
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import api from '../services/api'
import { ElMessage } from 'element-plus'

const reservations = ref<any[]>([])

async function load() {
  try {
    const { data } = await api.get('/reservations/me')
    reservations.value = data
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)

async function cancel(id: number) {
  try {
    await api.post(`/reservations/${id}/cancel`)
    ElMessage.success('取消成功')
    await load()
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '取消失败')
  }
}
</script>

<style scoped>
.page-container {
  max-width: 1000px;
  margin: 0 auto;
}
</style>
