<template>
  <div class="book-detail-container" v-if="book">
    <el-page-header @back="$router.back()" title="返回">
      <template #content>
        <span class="text-large font-600 mr-3"> 图书详情 </span>
      </template>
    </el-page-header>

    <el-card class="book-info-card">
      <div class="book-layout">
        <div class="book-cover">
           <el-image
             v-if="book.cover_url"
             :src="book.cover_url"
             fit="cover"
             style="width: 100%; height: 100%; border-radius: 4px;"
           >
             <template #error>
               <div class="image-error">
                 <el-icon :size="100" color="#909399"><Notebook /></el-icon>
               </div>
             </template>
           </el-image>
           <template v-else>
             <el-icon :size="100" color="#909399"><Notebook /></el-icon>
           </template>
        </div>
        <div class="book-meta">
          <h1>{{ book.title }}</h1>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="作者">{{ book.author }}</el-descriptions-item>
            <el-descriptions-item label="ISBN">{{ book.isbn }}</el-descriptions-item>
            <el-descriptions-item label="出版社">{{ book.publisher || '未知' }}</el-descriptions-item>
            <el-descriptions-item label="简介">{{ book.summary || '暂无简介' }}</el-descriptions-item>
          </el-descriptions>
        </div>
      </div>
    </el-card>

    <el-card class="copies-card" header="馆藏副本状态">
      <el-table :data="copies" stripe style="width: 100%">
        <el-table-column prop="barcode" label="条码号" width="180" />
        <el-table-column prop="location" label="馆藏位置" />
        <el-table-column prop="status" label="状态">
           <template #default="scope">
             <el-tag :type="getStatusType(scope.row.status)">
               {{ getStatusText(scope.row.status) }}
             </el-tag>
           </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button
              size="small"
              type="primary"
              :disabled="scope.row.status !== 'available'"
              @click="borrow(scope.row.id)"
            >
              借阅
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Notebook } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const book = ref<any>(null)
const copies = ref<any[]>([])

function getStatusType(status: string) {
  const map: Record<string, string> = {
    available: 'success',
    borrowed: 'warning',
    maintenance: 'info',
    lost: 'danger'
  }
  return map[status] || 'info'
}

function getStatusText(status: string) {
  const map: Record<string, string> = {
    available: '在馆',
    borrowed: '已借出',
    maintenance: '维护中',
    lost: '遗失'
  }
  return map[status] || status
}

onMounted(async () => {
  const id = route.params.id
  try {
    const { data } = await api.get(`/books/${id}`)
    book.value = data
    const { data: cds } = await api.get(`/copies/by-book/${id}`)
    copies.value = cds
  } catch (e) {
    ElMessage.error('加载图书详情失败')
  }
})

async function borrow(copyId: number) {
  try {
    await api.post('/loans', null, { params: { copy_id: copyId } })
    ElMessage.success('借阅成功')
    // Refresh copies
    const { data: cds } = await api.get(`/copies/by-book/${route.params.id}`)
    copies.value = cds
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '借阅失败')
  }
}
</script>

<style scoped>
.book-detail-container {
  max-width: 1000px;
  margin: 0 auto;
}

.book-info-card {
  margin-top: 20px;
}

.book-layout {
  display: flex;
  gap: 30px;
}

.book-cover {
  width: 200px;
  height: 280px;
  background-color: #f5f7fa;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 4px;
  flex-shrink: 0;
}

.image-error {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.book-meta {
  flex: 1;
}

.copies-card {
  margin-top: 20px;
}
</style>
