<template>
  <div class="page-container">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span class="title">
            <el-icon class="icon-header"><Reading /></el-icon>
            我的借阅
          </span>
          <el-tag type="info" effect="plain">共 {{ loans.length }} 本</el-tag>
        </div>
      </template>
      
      <el-table :data="loans" stripe style="width: 100%" v-loading="loading">
        <el-table-column label="图书信息" min-width="180">
           <template #default="scope">
             <div class="book-info">
                <span class="book-title">{{ scope.row.copy?.book?.title || '未知图书' }}</span>
                <span class="barcode">条码: {{ scope.row.copy?.barcode || scope.row.copy_id }}</span>
             </div>
           </template>
        </el-table-column>
        
        <el-table-column label="借阅日期" prop="loan_date" width="160">
          <template #default="scope">
            <div class="date-cell">
              <el-icon><Calendar /></el-icon>
              <span>{{ formatDate(scope.row.loan_date) }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="应还日期" prop="due_date" width="160">
          <template #default="scope">
            <div class="date-cell" :class="{ 'text-danger': isOverdue(scope.row) && !scope.row.return_date }">
              <el-icon><Timer /></el-icon>
              <span>{{ formatDate(scope.row.due_date) }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="状态" prop="status" width="100">
          <template #default="scope">
             <el-tag :type="getStatusType(scope.row)" effect="dark">
               {{ getStatusText(scope.row) }}
             </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="scope">
            <el-button-group>
              <el-button
                size="small"
                type="primary"
                @click="renew(scope.row.id)"
                :disabled="!!scope.row.return_date"
                :icon="Refresh"
              >
                续借
              </el-button>
              <el-button
                size="small"
                type="success"
                @click="ret(scope.row.id)"
                :disabled="!!scope.row.return_date"
                :icon="Check"
              >
                归还
              </el-button>
            </el-button-group>
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
import { Refresh, Check, Reading, Calendar, Timer } from '@element-plus/icons-vue'

const loans = ref<any[]>([])
const loading = ref(false)

async function load() {
  loading.value = true
  try {
    const { data } = await api.get('/loans/me')
    // Sort by loan_date desc
    loans.value = data.sort((a: any, b: any) => new Date(b.loan_date).getTime() - new Date(a.loan_date).getTime())
  } catch (e) {
    console.error(e)
    ElMessage.error('获取借阅记录失败')
  } finally {
    loading.value = false
  }
}

onMounted(load)

function formatDate(dateStr: string) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString()
}

function isOverdue(row: any) {
  return new Date(row.due_date) < new Date()
}

function getStatusType(row: any) {
  if (row.return_date) return 'success'
  if (isOverdue(row)) return 'danger'
  return 'primary'
}

function getStatusText(row: any) {
  if (row.return_date) return '已归还'
  if (isOverdue(row)) return '已逾期'
  return '借阅中'
}

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
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 18px;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 8px;
}

.icon-header {
  font-size: 20px;
  color: #409eff;
}

.book-info {
  display: flex;
  flex-direction: column;
}

.book-title {
  font-weight: bold;
  color: #303133;
}

.barcode {
  font-size: 12px;
  color: #909399;
}

.date-cell {
  display: flex;
  align-items: center;
  gap: 6px;
}

.text-danger {
  color: #f56c6c;
  font-weight: bold;
}
</style>
