<template>
  <div class="home-container">
    <div class="search-bar">
      <el-input
        v-model="q"
        placeholder="搜索书名或作者"
        class="search-input"
        size="large"
        @keyup.enter="search"
      >
        <template #append>
          <el-button :icon="Search" @click="search" />
        </template>
      </el-input>
    </div>

    <el-empty v-if="!books.length && searched" description="未找到相关图书" />
    
    <el-row :gutter="20" v-else>
      <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="b in books" :key="b.id">
        <el-card class="book-card" shadow="hover" @click="$router.push(`/books/${b.id}`)">
          <div class="book-cover">
            <el-icon :size="60" color="#909399"><Notebook /></el-icon>
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { Search, Notebook } from '@element-plus/icons-vue'

const q = ref('')
const books = ref<any[]>([])
const searched = ref(false)

async function search() {
  try {
    const { data } = await axios.get('/api/books', { params: { q: q.value } })
    // Check if data is array or object with items
    books.value = Array.isArray(data) ? data : (data.items || [])
    searched.value = true
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  search()
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
</style>
