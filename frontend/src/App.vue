<template>
  <div class="app-shell" :class="{ 'is-login-mode': isLoginRoute }">
    <!-- Left Sidebar (hidden on login view) -->
    <TheSidebar v-if="!isLoginRoute" />

    <!-- Right Workspace Area -->
    <div class="app-workspace" :class="{ 'full-workspace': isLoginRoute }">
      <!-- Top Header (hidden on login view) -->
      <TheHeader v-if="!isLoginRoute" />

      <!-- Main Dynamic Content (Vue Router) -->
      <main class="app-main-content">
        <router-view />
      </main>

      <!-- Bottom Status Footer (hidden on login view) -->
      <TheFooter v-if="!isLoginRoute" />
    </div>

    <!-- Reusable Global SCADA System Dialog -->
    <AppDialog />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import TheSidebar from './components/TheSidebar.vue'
import TheHeader from './components/TheHeader.vue'
import TheFooter from './components/TheFooter.vue'
import AppDialog from './components/AppDialog.vue'

const route = useRoute()
const isLoginRoute = computed(() => route.path === '/login')
</script>

<style scoped>
.app-shell {
  display: flex;
  width: 100vw;
  height: 100vh;
  background-color: var(--bg-app);
  overflow: hidden;
}

.app-shell.is-login-mode {
  background: transparent;
}

.app-workspace {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  height: 100%;
  overflow: hidden;
}

.app-workspace.full-workspace {
  width: 100vw;
  height: 100vh;
}

.app-main-content {
  flex: 1;
  min-height: 0;
  overflow: hidden;
  position: relative;
}
</style>