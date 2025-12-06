import { test, expect } from '@playwright/test'

const screenshotsDir = '../docs/screenshots'

test('capture key pages screenshots', async ({ page }) => {
  // 登录页
  await page.goto('/login')
  await page.waitForLoadState('networkidle')
  await page.screenshot({ path: `${screenshotsDir}/login.png`, fullPage: true })

  // 管理员登录
  await page.locator('input[placeholder="用户名"]').fill('admin')
  await page.locator('input[placeholder="密码"]').fill('Admin@12345')
  await page.getByRole('button', { name: '登录' }).click()
  await page.waitForURL('/')

  // 首页
  await page.waitForLoadState('networkidle')
  await page.screenshot({ path: `${screenshotsDir}/home.png`, fullPage: true })

  // 管理员首页
  await page.goto('/admin')
  await page.waitForLoadState('networkidle')
  await page.screenshot({ path: `${screenshotsDir}/admin.png`, fullPage: true })

  // 我的借阅
  await page.goto('/me/loans')
  await page.waitForLoadState('networkidle')
  await page.screenshot({ path: `${screenshotsDir}/my_loans.png`, fullPage: true })

  // 我的预约
  await page.goto('/me/reservations')
  await page.waitForLoadState('networkidle')
  await page.screenshot({ path: `${screenshotsDir}/my_reservations.png`, fullPage: true })

  // 我的罚金
  await page.goto('/me/fines')
  await page.waitForLoadState('networkidle')
  await page.screenshot({ path: `${screenshotsDir}/my_fines.png`, fullPage: true })
})

