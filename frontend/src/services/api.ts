import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers = config.headers || {}
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
})

export default api

export const importBooksByIsbn = async (isbn: string) => {
  const { data } = await api.post('/books/import/by_isbn', { isbn })
  return data
}

export const importBooksByKeyword = async (keyword: string, limit = 20) => {
  const { data } = await api.post('/books/import/by_keyword', { keyword, limit })
  return data
}

export const bulkImportBooks = async (file?: File, items?: any[]) => {
  if (file) {
    const form = new FormData()
    form.append('file', file)
    const { data } = await api.post('/books/bulk', form, { headers: { 'Content-Type': 'multipart/form-data' } })
    return data
  }
  const { data } = await api.post('/books/bulk', items || [])
  return data
}

