<template>
  <BasicLayout v-if="!$route.path.includes('/login')">
    <!-- BasicLayout will render router-view inside its el-main -->
  </BasicLayout>
  <router-view v-else />
</template>

<script setup lang="ts">
import BasicLayout from './layout/BasicLayout.vue'
</script>

<style>
body {
  margin: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}
</style>
