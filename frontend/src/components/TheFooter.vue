<template>
  <footer class="app-footer">
    <div class="footer-left">
      <span class="cluster-info">
        <span class="muted-label">Cluster Shards:</span> 
        <strong class="highlight-info">4 active namespaces</strong>
      </span>
      <span class="footer-divider">•</span>
      <span class="storage-info">
        <span class="muted-label">Total Storage:</span> 
        <strong class="highlight-info">14.8 GB</strong>
      </span>
    </div>

    <div class="footer-right">
      <div class="connection-status">
        <span class="conn-dot"></span>
        <span class="conn-text">FastAPI Stream Connected</span>
      </div>
      <span class="footer-divider">•</span>
      <span class="telemetry-info">p95: 28ms</span>
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped>
.app-footer {
  height: 34px;
  background: var(--bg-sidebar);
  border-top: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  font-size: 11px;
  color: var(--text-muted);
  user-select: none;
}

.footer-left, .footer-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.muted-label {
  color: var(--text-dim);
}

.highlight-info {
  color: var(--text-main);
  font-weight: 500;
}

.footer-divider {
  color: var(--text-dim);
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 6px;
}

.conn-dot {
  width: 5px;
  height: 5px;
  background: var(--status-green);
  border-radius: 50%;
  box-shadow: 0 0 6px var(--status-green);
}

.conn-text {
  color: #a7f3d0;
  font-weight: 500;
}

.telemetry-info {
  font-family: var(--font-mono);
  color: var(--text-dim);
}
</style>
