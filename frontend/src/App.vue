<template>
  <div class="app-shell">
    <!-- Left Sidebar -->
    <TheSidebar />

    <!-- Right Workspace Area -->
    <div class="app-workspace">
      <!-- Top Header -->
      <TheHeader />

      <!-- Main Dynamic Content (Vue Router) -->
      <main class="app-main-content">
        <router-view />
      </main>

      <!-- Bottom Status Footer -->
      <TheFooter />
    </div>
  </div>
</template>

<script setup>
import TheSidebar from './components/TheSidebar.vue'
import TheHeader from './components/TheHeader.vue'
import TheFooter from './components/TheFooter.vue'
</script>

<style scoped>
.app-shell {
  display: flex;
  width: 100vw;
  height: 100vh;
  background-color: var(--bg-app);
  overflow: hidden;
}

.app-workspace {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  height: 100%;
  overflow: hidden;
}

.app-main-content {
  flex: 1;
  min-height: 0;
  overflow: hidden;
  position: relative;
}
</style>