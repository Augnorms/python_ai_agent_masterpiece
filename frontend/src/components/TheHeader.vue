<template>
  <header class="app-header">
    <div class="header-left">
      <!-- Swarm Status Pill -->
      <div class="status-pill">
        <span class="active-dot" :class="{ 'inactive-dot': status !== 'active' }"></span>
        <span class="status-text">{{ status === 'active' ? 'Swarm Active' : status }}</span>
        <span class="divider">•</span>
        <span class="region-text">{{ region }}</span>
      </div>

      <!-- Supervisor Model Badge -->
      <div class="model-badge">
        <svg class="model-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10" />
          <path d="M12 16v-4M12 8h.01" />
        </svg>
        <span class="model-name">{{ model }}</span>
        <span class="role-tag">Supervisor</span>
      </div>
    </div>

    <div class="header-right">
      <!-- Theme Toggle (Dark / Light Mode) -->
      <button 
        class="header-icon-btn theme-toggle-btn" 
        :title="isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
        @click="toggleTheme"
        aria-label="Toggle Theme"
      >
        <!-- Sun Icon (shown in dark mode) -->
        <svg v-if="isDark" class="theme-icon sun-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="5" />
          <line x1="12" y1="1" x2="12" y2="3" />
          <line x1="12" y1="21" x2="12" y2="23" />
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
          <line x1="1" y1="12" x2="3" y2="12" />
          <line x1="21" y1="12" x2="23" y2="12" />
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
        </svg>

        <!-- Moon Icon (shown in light mode) -->
        <svg v-else class="theme-icon moon-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
        </svg>
      </button>

      <!-- Terminal / Logs Button -->
      <button class="header-icon-btn" title="View Server & Agent Logs">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
          <polyline points="4 17 10 11 4 5" />
          <line x1="12" y1="19" x2="20" y2="19" />
        </svg>
      </button>

      <!-- Notifications -->
      <button class="header-icon-btn" title="System Notifications">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
          <path d="M13.73 21a2 2 0 0 1-3.46 0" />
        </svg>
        <span class="notification-indicator"></span>
      </button>

      <!-- User Avatar -->
      <div class="user-profile">
        <div class="user-avatar">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isDark = ref(true)
const status = ref('active')
const region = ref('Ghana-Accra')
const model = ref('openai/gpt-oss-20b')

const fetchStatus = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/status')
    if (res.ok) {
      const data = await res.json()
      if (data.status) status.value = data.status
      if (data.region) region.value = data.region
      if (data.model) model.value = data.model
    }
  } catch (err) {
    console.warn('Could not fetch status from backend:', err)
  }
}

const toggleTheme = () => {
  isDark.value = !isDark.value
  const theme = isDark.value ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme') || 'dark'
  isDark.value = savedTheme === 'dark'
  document.documentElement.setAttribute('data-theme', savedTheme)
  fetchStatus()
})
</script>

<style scoped>
.app-header {
  height: 56px;
  background: var(--bg-header);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  user-select: none;
  transition: background-color 0.25s ease, border-color 0.25s ease;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.status-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(13, 21, 39, 0.9);
  border: 1px solid rgba(23, 36, 60, 0.9);
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 11px;
}

.active-dot {
  width: 6px;
  height: 6px;
  background: var(--status-green);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--status-green);
}

.inactive-dot {
  background: var(--text-dim);
  box-shadow: none;
}

.status-text {
  color: var(--text-main);
  font-weight: 500;
}

.divider {
  color: var(--text-dim);
}

.region-text {
  color: var(--text-muted);
}

.model-badge {
  display: flex;
  align-items: center;
  gap: 7px;
  background: rgba(157, 114, 255, 0.12);
  border: 1px solid rgba(157, 114, 255, 0.35);
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 11px;
}

.model-icon {
  width: 14px;
  height: 14px;
  color: #a855f7;
  flex-shrink: 0;
}

.model-name {
  color: #c084fc;
  font-family: var(--font-mono);
  font-weight: 600;
  letter-spacing: 0.2px;
}

.role-tag {
  background: rgba(157, 114, 255, 0.25);
  color: #ffffff;
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 4px;
  font-weight: 700;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon-btn {
  background: transparent;
  border: 1px solid rgba(23, 36, 60, 0.8);
  border-radius: 8px;
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
}

.header-icon-btn svg {
  width: 17px;
  height: 17px;
}

.header-icon-btn:hover {
  background: rgba(255, 255, 255, 0.04);
  color: var(--primary-cyan);
  border-color: rgba(0, 229, 255, 0.3);
}

.theme-toggle-btn {
  transition: all 0.25s ease;
}

.theme-icon {
  width: 17px;
  height: 17px;
  transition: transform 0.3s ease, color 0.3s ease;
}

.theme-toggle-btn:hover .sun-icon {
  transform: rotate(45deg);
  color: #f59e0b;
}

.theme-toggle-btn:hover .moon-icon {
  transform: rotate(-15deg);
  color: #6366f1;
}

.notification-indicator {
  position: absolute;
  top: 7px;
  right: 7px;
  width: 5px;
  height: 5px;
  background: var(--primary-cyan);
  border-radius: 50%;
  box-shadow: 0 0 6px var(--primary-cyan);
}

.user-profile {
  margin-left: 4px;
  cursor: pointer;
}

.user-avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: rgba(0, 229, 255, 0.15);
  border: 1.5px solid var(--primary-cyan);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-cyan);
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.25);
  transition: transform 0.2s ease;
}

.user-avatar svg {
  width: 18px;
  height: 18px;
}

.user-avatar:hover {
  transform: scale(1.05);
}
</style>
