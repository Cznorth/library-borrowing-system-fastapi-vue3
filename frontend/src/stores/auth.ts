import { defineStore } from 'pinia'
import api from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({ user: null as any }),
  actions: {
    async fetchMe() {
      try {
        const { data } = await api.get('/users/me')
        this.user = data
      } catch (e) {
        this.user = null
      }
    },
    logout() {
      localStorage.removeItem('token')
      this.user = null
      location.href = '/login'
    }
  }
})

