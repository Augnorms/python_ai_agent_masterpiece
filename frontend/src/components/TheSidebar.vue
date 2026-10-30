<template>
  <aside class="sidebar">
    <!-- Brand Logo -->
    <div class="sidebar-brand">
      <div class="brand-icon-box">
        <svg class="brand-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="12" cy="12" r="3" fill="#00e5ff" stroke="none" />
          <circle cx="5" cy="8" r="2" fill="#00e5ff" stroke="none" />
          <circle cx="19" cy="8" r="2" fill="#00e5ff" stroke="none" />
          <circle cx="7" cy="19" r="2" fill="#00e5ff" stroke="none" />
          <circle cx="17" cy="19" r="2" fill="#00e5ff" stroke="none" />
          <path d="M12 12L5 8M12 12L19 8M12 12L7 19M12 12L17 19" stroke="#00e5ff" stroke-width="1.8" />
        </svg>
      </div>
      <div class="brand-text">
        <span class="brand-title">SwarmFlow</span>
        <span class="brand-subtitle">AI ORCHESTRATOR</span>
      </div>
    </div>

    <!-- Navigation -->
    <div class="nav-section">
      <div class="nav-label">NAVIGATION</div>
      <nav class="nav-links">
        <router-link to="/knowledge" class="nav-item" active-class="active">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <ellipse cx="12" cy="5" rx="9" ry="3" />
            <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" />
            <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
          </svg>
          <span class="nav-text">Knowledge & RAG</span>
        </router-link>

        <router-link to="/orchestrator" class="nav-item" active-class="active">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <polygon points="12 2 2 7 12 12 22 7 12 2" />
            <polyline points="2 17 12 22 22 17" />
            <polyline points="2 12 12 17 22 12" />
          </svg>
          <span class="nav-text">Agent Orchestrator</span>
        </router-link>
      </nav>
    </div>

    <!-- Spacer -->
    <div class="sidebar-spacer"></div>

    <!-- Settings Route (Close to Environment Card) -->
    <div class="sidebar-bottom-nav">
      <router-link to="/settings" class="nav-item" active-class="active">
        <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
          <circle cx="12" cy="12" r="3" />
          <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
        </svg>
        <span class="nav-text">Settings</span>
      </router-link>
    </div>

    <!-- Environment Footer Widget -->
    <div class="environment-widget">
      <div class="env-header">
        <span class="env-label">ENVIRONMENT</span>
        <span class="status-indicator">
          <span class="status-dot"></span>
          Online
        </span>
      </div>
      <div class="env-details">
        <span class="version-tag">v1.0.0-mvp</span>
        <span class="badge-stable">STABLE</span>
      </div>
    </div>
  </aside>
</template>

<script setup>
</script>

<style scoped>
.sidebar {
  width: 240px;
  min-width: 240px;
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  padding: 20px 16px;
  user-select: none;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 24px;
  border-bottom: 1px solid rgba(23, 36, 60, 0.7);
}

.brand-icon-box {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: rgba(0, 229, 255, 0.1);
  border: 1px solid rgba(0, 229, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 14px rgba(0, 229, 255, 0.2);
}

.brand-icon {
  width: 22px;
  height: 22px;
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-title {
  font-weight: 700;
  font-size: 15px;
  letter-spacing: 0.3px;
  color: #fff;
}

.brand-subtitle {
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 1.2px;
  color: var(--primary-cyan);
}

.nav-section {
  margin-top: 24px;
}

.nav-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1px;
  color: var(--text-dim);
  padding: 0 8px 12px 8px;
}

.nav-links {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.nav-icon {
  width: 17px;
  height: 17px;
  color: var(--text-dim);
  transition: color 0.2s ease;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.03);
  color: var(--text-main);
}

.nav-item:hover .nav-icon {
  color: var(--primary-cyan);
}

.nav-item.active {
  background: rgba(0, 229, 255, 0.07);
  border: 1px solid rgba(0, 229, 255, 0.35);
  color: var(--primary-cyan);
  font-weight: 600;
  box-shadow: 0 0 15px rgba(0, 229, 255, 0.08);
}

.nav-item.active .nav-icon {
  color: var(--primary-cyan);
}

.sidebar-spacer {
  flex: 1;
}

.sidebar-bottom-nav {
  margin-bottom: 12px;
}

.environment-widget {
  background: rgba(13, 21, 39, 0.8);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.env-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.env-label {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.8px;
  color: var(--text-dim);
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 600;
  color: var(--status-green);
}

.status-dot {
  width: 6px;
  height: 6px;
  background-color: var(--status-green);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--status-green);
  animation: pulse-dot 2s infinite ease-in-out;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.85); }
}

.env-details {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.version-tag {
  font-size: 11px;
  font-family: var(--font-mono);
  color: var(--text-muted);
}

.badge-stable {
  background: rgba(16, 185, 129, 0.12);
  color: #34d399;
  font-size: 9px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid rgba(16, 185, 129, 0.25);
  letter-spacing: 0.5px;
}
</style>
