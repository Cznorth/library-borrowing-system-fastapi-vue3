<template>
  <div class="page-container">
    <el-card header="我的借阅">
      <el-table :data="loans" stripe>
        <el-table-column label="副本条码" prop="copy.barcode">
           <template #default="scope">
             {{ scope.row.copy?.barcode || scope.row.copy_id }}
           </template>
        </el-table-column>
        <el-table-column label="借阅日期" prop="borrow_date">
          <template #default="scope">
            {{ new Date(scope.row.borrow_date).toLocaleDateString() }}
          </template>
        </el-table-column>
        <el-table-column label="应还日期" prop="due_date">
          <template #default="scope">
            {{ new Date(scope.row.due_date).toLocaleDateString() }}
          </template>
        </el-table-column>
        <el-table-column label="状态" prop="status">
          <template #default="scope">
             <el-tag :type="scope.row.return_date ? 'success' : (new Date(scope.row.due_date) < new Date() ? 'danger' : 'primary')">
               {{ scope.row.return_date ? '已归还' : (new Date(scope.row.due_date) < new Date() ? '已逾期' : '借阅中') }}
             </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button
              size="small"
              type="primary"
              @click="renew(scope.row.id)"
              :disabled="!!scope.row.return_date"
            >
              续借
            </el-button>
            <el-button
              size="small"
              type="success"
              @click="ret(scope.row.id)"
              :disabled="!!scope.row.return_date"
            >
              归还
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

const loans = ref<any[]>([])

async function load() {
  try {
    const { data } = await api.get('/loans/me')
    loans.value = data
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)

async function renew(id: number) {
  try {
    await api.post(`/loans/${id}/renew`)
    ElMessage.success('续借成功')
    await load()
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '续借失败')
  }
}

async function ret(id: number) {
  try {
    await api.post(`/loans/${id}/return`)
    ElMessage.success('归还成功')
    await load()
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '归还失败')
  }
}
</script>

<style scoped>
.page-container {
  max-width: 1000px;
  margin: 0 auto;
}
</style>
