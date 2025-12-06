import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import Home from '../pages/Home.vue'
import BookDetail from '../pages/BookDetail.vue'
import MyLoans from '../pages/MyLoans.vue'
import MyReservations from '../pages/MyReservations.vue'
import MyFines from '../pages/MyFines.vue'
import AdminDashboard from '../pages/AdminDashboard.vue'
import BooksManage from '../pages/BooksManage.vue'
import UsersManage from '../pages/UsersManage.vue'
import { useAuthStore } from '../stores/auth'

const routes: RouteRecordRaw[] = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/books/:id', component: BookDetail },
  { path: '/me/loans', component: MyLoans },
  { path: '/me/reservations', component: MyReservations },
  { path: '/me/fines', component: MyFines },
  { path: '/admin', component: AdminDashboard },
  { path: '/admin/books', component: BooksManage },
  { path: '/admin/users', component: UsersManage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from) => {
  const store = useAuthStore()
  if (!store.user) {
    await store.fetchMe()
  }
  if (to.path !== '/login' && to.path !== '/register' && !localStorage.getItem('token')) {
    return '/login'
  }
  // 简单的角色保护：访问 /admin 需要管理员角色
  if (to.path.startsWith('/admin') && store.user?.role !== 'admin') {
    return '/'
  }
})

export default router

