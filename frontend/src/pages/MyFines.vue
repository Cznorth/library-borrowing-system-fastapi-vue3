<template>
  <div class="page-container">
    <el-card header="我的罚金">
      <el-table :data="fines" stripe>
        <el-table-column label="金额" prop="amount">
          <template #default="scope">
            ¥{{ scope.row.amount }}
          </template>
        </el-table-column>
        <el-table-column label="原因" prop="reason" />
        <el-table-column label="状态" prop="status">
           <template #default="scope">
             <el-tag :type="scope.row.status === 'paid' ? 'success' : 'danger'">
               {{ scope.row.status === 'paid' ? '已支付' : '未支付' }}
             </el-tag>
           </template>
        </el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button
              size="small"
              type="primary"
              @click="pay(scope.row.id)"
              :disabled="scope.row.status === 'paid'"
            >
              缴纳
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

const fines = ref<any[]>([])

async function load() {
  try {
    const { data } = await api.get('/fines/me')
    fines.value = data
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)

async function pay(id: number) {
  try {
    await api.post(`/fines/${id}/pay`)
    ElMessage.success('缴纳成功')
    await load()
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '缴纳失败')
  }
}
</script>

<style scoped>
.page-container {
  max-width: 1000px;
  margin: 0 auto;
}
</style>
