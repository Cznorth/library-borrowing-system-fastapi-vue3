import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  optimizeDeps: {
    entries: ['index.html']
  },
  server: {
    port: 5173,
    allowedHosts: true,
    proxy: {
      '/api': process.env.VITE_API_PROXY_TARGET || 'http://localhost:8000'
    }
  }
})

