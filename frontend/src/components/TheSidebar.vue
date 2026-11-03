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

    <!-- Section 1: Process Schematics -->
    <div class="nav-section">
      <div class="nav-label">PROCESS SCHEMATICS</div>
      <nav class="nav-links">
        <router-link to="/overview" class="nav-item" active-class="active">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <circle cx="12" cy="12" r="8.5" />
            <circle cx="12" cy="12" r="2.5" fill="currentColor" stroke="none" />
            <path d="M12 3.5v3M12 17.5v3M4 12h3M17 12h3" />
          </svg>
          <span class="nav-text">Overview & Predictive Models</span>
        </router-link>
      </nav>
    </div>

    <!-- Section 2: Telemetry & Supervision -->
    <div class="nav-section">
      <div class="nav-label">TELEMETRY & SUPERVISION</div>
      <nav class="nav-links">
        <router-link to="/modbus" class="nav-item" active-class="active">
          <!-- PLC Modbus Chip Icon matching media_1793640139533_f007cf37.png -->
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <rect x="3" y="4" width="15" height="16" rx="2" stroke="currentColor" stroke-width="1.8" />
            <rect x="6" y="7" width="3" height="4" fill="currentColor" opacity="0.85" />
            <rect x="11" y="7" width="3" height="4" fill="currentColor" opacity="0.85" />
            <rect x="6" y="13" width="3" height="4" fill="currentColor" opacity="0.85" />
            <rect x="11" y="13" width="3" height="4" fill="currentColor" opacity="0.85" />
            <line x1="18" y1="8" x2="21" y2="8" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            <line x1="18" y1="12" x2="21" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            <line x1="18" y1="16" x2="21" y2="16" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
          </svg>
          <span class="nav-text">Modbus TCP Telemetry (PLC)</span>
        </router-link>

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
  width: 250px;
  min-width: 250px;
  background: var(--bg-sidebar, #070d1a);
  border-right: 1px solid var(--border-color, #142442);
  display: flex;
  flex-direction: column;
  padding: 16px 14px;
  user-select: none;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 18px;
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
  width: 20px;
  height: 20px;
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
  color: var(--primary-cyan, #00e5ff);
}

.nav-section {
  margin-top: 20px;
}

.nav-label {
  font-size: 9.5px;
  font-weight: 800;
  letter-spacing: 0.8px;
  color: var(--text-dim, #64748b);
  padding: 0 8px 8px 8px;
}

.nav-links {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 12px;
  border-radius: 6px;
  color: var(--text-muted, #94a3b8);
  font-size: 12.5px;
  font-weight: 600;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  text-decoration: none;
}

.nav-icon {
  width: 17px;
  height: 17px;
  flex-shrink: 0;
  color: var(--text-dim, #64748b);
  transition: color 0.2s ease;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.04);
  color: var(--text-main, #f1f5f9);
}

.nav-item:hover .nav-icon {
  color: var(--primary-cyan, #00e5ff);
}

/* Active Tab: Matches media_1793640139533_f007cf37.png with vibrant cyan pill and dark text */
.nav-item.active {
  background: #00c2e8;
  border: 1px solid #00c2e8;
  color: #04101e;
  font-weight: 800;
  box-shadow: 0 0 16px rgba(0, 194, 232, 0.35);
}

.nav-item.active .nav-icon {
  color: #04101e;
  stroke: #04101e;
}

.sidebar-spacer {
  flex: 1;
}

.sidebar-bottom-nav {
  margin-bottom: 12px;
}

.environment-widget {
  background: rgba(13, 21, 39, 0.8);
  border: 1px solid var(--border-color, #17243c);
  border-radius: 8px;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
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
  color: var(--text-dim, #64748b);
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 600;
  color: var(--status-green, #10b981);
}

.status-dot {
  width: 6px;
  height: 6px;
  background-color: var(--status-green, #10b981);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--status-green, #10b981);
  animation: pulse-dot 2s infinite ease-in-out;
}

.env-details {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.version-tag {
  font-size: 10px;
  color: var(--text-muted, #94a3b8);
  font-family: var(--font-mono, monospace);
}

.badge-stable {
  font-size: 9px;
  font-weight: 700;
  color: var(--status-green, #10b981);
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
  padding: 1px 6px;
  border-radius: 4px;
}

@keyframes pulse-dot {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.3); opacity: 0.7; }
}

</style>
