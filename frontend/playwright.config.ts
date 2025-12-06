import { defineConfig } from '@playwright/test'

export default defineConfig({
  testMatch: ['tests/screenshots.spec.ts'],
  use: {
    baseURL: 'http://localhost:5173',
  }
})

