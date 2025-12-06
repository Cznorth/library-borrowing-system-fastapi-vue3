<template>
  <div class="page-container">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <div class="left">
            <span class="title">图书管理</span>
          </div>
          <div class="right">
            <el-button type="primary" @click="showAddDialog = true">新增图书</el-button>
            <el-button type="success" @click="showImportDialog = true">批量导入</el-button>
          </div>
        </div>
      </template>

      <!-- Search Toolbar -->
      <div class="toolbar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索书名、作者、ISBN..."
          clearable
          @clear="handleSearch"
          @keyup.enter="handleSearch"
          style="width: 300px"
        >
          <template #append>
            <el-button @click="handleSearch">
              <el-icon><Search /></el-icon>
            </el-button>
          </template>
        </el-input>
      </div>

      <!-- Table -->
      <el-table :data="books" v-loading="loading" stripe style="width: 100%; margin-top: 20px">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column label="封面" width="80">
          <template #default="scope">
            <el-image 
              v-if="scope.row.cover_url" 
              :src="scope.row.cover_url" 
              :preview-src-list="[scope.row.cover_url]"
              fit="cover" 
              style="width: 40px; height: 60px" 
            />
            <div v-else class="no-cover">无封面</div>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="书名" min-width="150" show-overflow-tooltip />
        <el-table-column prop="author" label="作者" width="120" show-overflow-tooltip />
        <el-table-column prop="isbn" label="ISBN" width="140" />
        <el-table-column prop="publisher" label="出版社" width="120" show-overflow-tooltip />
        <el-table-column prop="category" label="分类" width="100" />
        <el-table-column label="库存" width="100">
          <template #default="scope">
             <el-tag type="info">{{ scope.row.available_copies }} 本可用</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button size="small" type="danger" @click="remove(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- Add Book Dialog -->
    <el-dialog v-model="showAddDialog" title="新增图书" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="书名" required>
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="作者" required>
          <el-input v-model="form.author" />
        </el-form-item>
        <el-form-item label="ISBN">
          <el-input v-model="form.isbn" />
        </el-form-item>
        <el-form-item label="出版社">
          <el-input v-model="form.publisher" />
        </el-form-item>
        <el-form-item label="年份">
          <el-input-number v-model="form.year" :min="1000" :max="new Date().getFullYear()" />
        </el-form-item>
        <el-form-item label="分类">
          <el-input v-model="form.category" />
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="form.summary" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddDialog = false">取消</el-button>
          <el-button type="primary" @click="create">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Import Dialog -->
    <el-dialog v-model="showImportDialog" title="批量导入图书" width="600px">
      <el-tabs v-model="importTab">
        <el-tab-pane label="关键字导入" name="keyword">
          <el-form label-width="100px">
            <el-form-item label="关键字">
              <el-input v-model="importKeyword" placeholder="如：计算机科学" />
            </el-form-item>
            <el-form-item label="数量限制">
              <el-input-number v-model="importLimit" :min="1" :max="50" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="importByKeyword" :loading="importLoading">开始导入</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="ISBN 导入" name="isbn">
          <el-form label-width="100px">
            <el-form-item label="ISBN">
              <el-input v-model="importIsbn" placeholder="输入 ISBN" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="importByIsbn" :loading="importLoading">导入</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="文件导入" name="file">
          <div class="upload-container">
             <input type="file" ref="fileInput" @change="onFileChange" accept=".csv,.json" style="display: none" />
             <el-button @click="$refs.fileInput.click()">选择文件</el-button>
             <span v-if="importFile" style="margin-left: 10px">{{ importFile.name }}</span>
             <div style="margin-top: 20px">
               <el-button type="primary" @click="handleImportFile" :disabled="!importFile" :loading="importLoading">上传并导入</el-button>
             </div>
             <p class="hint">支持 .json 或 .csv 格式</p>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import api, { importBooksByKeyword, importBooksByIsbn, bulkImportBooks } from '../services/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'

// Data
const books = ref<any[]>([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const searchQuery = ref('')

// Dialogs
const showAddDialog = ref(false)
const showImportDialog = ref(false)
const importTab = ref('keyword')
const importLoading = ref(false)

// Forms
const form = reactive({
  title: '',
  author: '',
  isbn: '',
  publisher: '',
  year: new Date().getFullYear(),
  category: '',
  summary: ''
})

const importKeyword = ref('')
const importLimit = ref(10)
const importIsbn = ref('')
const importFile = ref<File | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)

async function load() {
  loading.value = true
  try {
    const params: any = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    if (searchQuery.value) {
      params.q = searchQuery.value
    }
    const { data } = await api.get('/books', { params })
    books.value = data.items
    total.value = data.total
  } catch (e) {
    console.error(e)
    ElMessage.error('加载图书列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(load)

function handleSearch() {
  currentPage.value = 1
  load()
}

function handleSizeChange(val: number) {
  pageSize.value = val
  load()
}

function handleCurrentChange(val: number) {
  currentPage.value = val
  load()
}

async function create() {
  if (!form.title || !form.author) {
    ElMessage.warning('请填写书名和作者')
    return
  }
  try {
    await api.post('/books', form)
    ElMessage.success('创建成功')
    showAddDialog.value = false
    // Reset form
    Object.assign(form, {
      title: '',
      author: '',
      isbn: '',
      publisher: '',
      year: new Date().getFullYear(),
      category: '',
      summary: ''
    })
    load()
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '创建失败')
  }
}

async function remove(id: number) {
  try {
    await ElMessageBox.confirm('确定要删除这本书吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await api.delete(`/books/${id}`)
    ElMessage.success('删除成功')
    load()
  } catch (e) {
    // Cancelled or error
  }
}

// Import functions
async function importByKeyword() {
  if (!importKeyword.value) return
  importLoading.value = true
  try {
    await importBooksByKeyword(importKeyword.value, importLimit.value)
    ElMessage.success('导入任务已提交')
    showImportDialog.value = false
    load()
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '导入失败')
  } finally {
    importLoading.value = false
  }
}

async function importByIsbn() {
  if (!importIsbn.value) return
  importLoading.value = true
  try {
    await importBooksByIsbn(importIsbn.value)
    ElMessage.success('导入成功')
    importIsbn.value = ''
    load() // Refresh
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '导入失败')
  } finally {
    importLoading.value = false
  }
}

function onFileChange(e: Event) {
  const t = e.target as HTMLInputElement
  importFile.value = t.files && t.files[0] ? t.files[0] : null
}

async function handleImportFile() {
  if (!importFile.value) return
  importLoading.value = true
  try {
    await bulkImportBooks(importFile.value)
    ElMessage.success('批量导入成功')
    importFile.value = null
    showImportDialog.value = false
    load()
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '导入失败')
  } finally {
    importLoading.value = false
  }
}
</script>

<style scoped>
.page-container {
  max-width: 1200px;
  margin: 20px auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 18px;
  font-weight: bold;
}

.toolbar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.no-cover {
  width: 40px;
  height: 60px;
  background-color: #f0f2f5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  color: #909399;
  text-align: center;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.upload-container {
  text-align: center;
  padding: 20px;
  border: 1px dashed #dcdfe6;
  border-radius: 4px;
}

.hint {
  font-size: 12px;
  color: #909399;
  margin-top: 10px;
}
</style>
