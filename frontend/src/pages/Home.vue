<template>
  <div class="home-container">
    <div class="search-bar">
      <el-input
        v-model="q"
        placeholder="搜索书名或作者"
        class="search-input"
        size="large"
        @keyup.enter="search(true)"
      >
        <template #append>
          <el-button :icon="Search" @click="search(true)" />
        </template>
      </el-input>
    </div>

    <el-empty v-if="!books.length && searched" description="未找到相关图书" />

    <el-row :gutter="20" v-else>
      <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="b in books" :key="b.id">
        <el-card class="book-card" shadow="hover" @click="$router.push(`/books/${b.id}`)">
          <div class="book-cover">
            <el-image
              v-if="b.cover_url"
              :src="b.cover_url"
              fit="cover"
              style="width: 100%; height: 100%; border-radius: 4px;"
            >
              <template #error>
                <div class="image-error">
                  <el-icon :size="60" color="#909399"><Notebook /></el-icon>
                </div>
              </template>
            </el-image>
            <template v-else>
              <el-icon :size="60" color="#909399"><Notebook /></el-icon>
            </template>
          </div>
          <div class="book-info">
            <h3 class="book-title" :title="b.title">{{ b.title }}</h3>
            <p class="book-author">{{ b.author }}</p>
            <p class="book-isbn">ISBN: {{ b.isbn }}</p>
            <div class="book-status">
              <el-tag :type="b.available_copies > 0 ? 'success' : 'danger'">
                {{ b.available_copies > 0 ? '可借阅' : '暂无库存' }}
              </el-tag>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <div class="pagination-wrapper" v-if="total > 0">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[8, 12, 16, 24]"
        layout="total, sizes, prev, pager, next, jumper"
        @current-change="onPageChange"
        @size-change="onSizeChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { Search, Notebook } from '@element-plus/icons-vue'

const q = ref('')
const books = ref<any[]>([])
const searched = ref(false)
const currentPage = ref(1)
const pageSize = ref(12)
const total = ref(0)

async function search(reset = false) {
  if (reset) {
    currentPage.value = 1
  }
  try {
    const { data } = await axios.get('/api/books', { params: { q: q.value || undefined, page: currentPage.value, page_size: pageSize.value } })
    books.value = Array.isArray(data) ? data : (data.items || [])
    total.value = Array.isArray(data) ? data.length : (data.total || 0)
    searched.value = true
  } catch (e) {
    console.error(e)
  }
}

function onPageChange(p: number) {
  currentPage.value = p
  search()
}

function onSizeChange(s: number) {
  pageSize.value = s
  currentPage.value = 1
  search()
}

onMounted(() => {
  search(true)
})
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
}

.search-bar {
  margin-bottom: 30px;
  display: flex;
  justify-content: center;
}

.search-input {
  max-width: 600px;
  width: 100%;
}

.book-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.2s;
}

.book-card:hover {
  transform: translateY(-5px);
}

.book-cover {
  height: 150px;
  background-color: #f5f7fa;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 4px;
  margin-bottom: 15px;
}

.image-error {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.book-title {
  font-size: 16px;
  font-weight: bold;
  margin: 0 0 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.book-author {
  color: #606266;
  font-size: 14px;
  margin: 0 0 5px;
}

.book-isbn {
  color: #909399;
  font-size: 12px;
  margin: 0 0 10px;
}

.book-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination-wrapper {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}
</style>
