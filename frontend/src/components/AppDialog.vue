<template>
  <transition name="dialog-fade">
    <div
      v-if="isDialogOpen"
      class="dialog-overlay"
      @click.self="handleOverlayClick"
      role="presentation"
    >
      <div
        class="dialog-card"
        :class="[`dialog-${dialogOptions.type || 'info'}`, { 'is-light': isLight }]"
        role="dialog"
        aria-modal="true"
        :aria-labelledby="dialogTitleId"
      >
        <!-- Glow accent line on top of card -->
        <div class="card-accent-bar" :class="dialogOptions.type || 'info'"></div>

        <!-- Top Status Bar -->
        <div class="dialog-top-bar">
          <div class="dialog-status-pill">
            <span class="status-dot"></span>
            <span class="status-name">SCADA SYSTEM GATEWAY</span>
          </div>
          <span class="dialog-node-tag">PLANT NODE #04</span>
        </div>

        <!-- Close 'X' button -->
        <button
          type="button"
          class="dialog-close-btn"
          @click="handleCancel"
          aria-label="Close dialog"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>

        <!-- Body Content -->
        <div class="dialog-body">
          <!-- Icon Box -->
          <div class="dialog-icon-box" :class="dialogOptions.type || 'info'">
            <!-- Confirm / Logout / Warning: Lock & Shield or Warning Triangle -->
            <svg
              v-if="dialogOptions.type === 'confirm'"
              class="dialog-type-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>

            <!-- Warning Icon -->
            <svg
              v-else-if="dialogOptions.type === 'warning'"
              class="dialog-type-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
              <line x1="12" y1="9" x2="12" y2="13" />
              <line x1="12" y1="17" x2="12.01" y2="17" />
            </svg>

            <!-- Error Icon -->
            <svg
              v-else-if="dialogOptions.type === 'error'"
              class="dialog-type-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <circle cx="12" cy="12" r="10" />
              <line x1="15" y1="9" x2="9" y2="15" />
              <line x1="9" y1="9" x2="15" y2="15" />
            </svg>

            <!-- Success Icon -->
            <svg
              v-else-if="dialogOptions.type === 'success'"
              class="dialog-type-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <circle cx="12" cy="12" r="10" />
              <polyline points="16 9 10 15 7 12" />
            </svg>

            <!-- Info Icon (Default) -->
            <svg
              v-else
              class="dialog-type-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="16" x2="12" y2="12" />
              <line x1="12" y1="8" x2="12.01" y2="8" />
            </svg>
          </div>

          <div class="dialog-text-content">
            <h3 :id="dialogTitleId" class="dialog-title">
              {{ dialogOptions.title || 'System Notice' }}
            </h3>
            <p class="dialog-message">
              {{ dialogOptions.message }}
            </p>
          </div>
        </div>

        <!-- Footer Actions -->
        <div class="dialog-footer">
          <button
            v-if="dialogOptions.showCancel"
            type="button"
            class="btn-dialog-cancel"
            @click="handleCancel"
          >
            {{ dialogOptions.cancelText || 'Cancel' }}
          </button>

          <button
            type="button"
            class="btn-dialog-confirm"
            :class="dialogOptions.type || 'info'"
            @click="handleConfirm"
          >
            {{ dialogOptions.confirmText || 'Acknowledge' }}
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useDialog } from '../composables/useDialog'

const { isDialogOpen, dialogOptions, handleConfirm, handleCancel } = useDialog()

const isLight = ref(false)
const dialogTitleId = computed(() => 'scada-dialog-title-' + Math.random().toString(36).slice(2, 7))

const handleOverlayClick = () => {
  if (dialogOptions.value.showCancel) {
    handleCancel()
  } else {
    handleConfirm()
  }
}

const handleKeydown = (e) => {
  if (!isDialogOpen.value) return
  if (e.key === 'Escape') {
    handleCancel()
  } else if (e.key === 'Enter') {
    handleConfirm()
  }
}

const checkTheme = () => {
  const currentTheme = document.documentElement.getAttribute('data-theme')
  isLight.value = currentTheme === 'light'
}

onMounted(() => {
  checkTheme()
  window.addEventListener('keydown', handleKeydown)
  window.addEventListener('theme-changed', (e) => {
    isLight.value = e.detail?.theme === 'light'
  })
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
/* Overlay Backdrop */
.dialog-overlay {
  position: fixed;
  inset: 0;
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.25rem;
  background: rgba(4, 8, 16, 0.78);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
}

/* Animations */
.dialog-fade-enter-active,
.dialog-fade-leave-active {
  transition: opacity 0.2s ease;
}

.dialog-fade-enter-from,
.dialog-fade-leave-to {
  opacity: 0;
}

.dialog-fade-enter-active .dialog-card {
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.2s ease;
}

.dialog-fade-enter-from .dialog-card {
  transform: scale(0.95) translateY(-8px);
  opacity: 0;
}

/* Dialog Card */
.dialog-card {
  position: relative;
  width: 100%;
  max-width: 440px;
  background: #0d1424;
  border: 1px solid rgba(0, 229, 255, 0.25);
  border-radius: 14px;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.75), 0 0 35px rgba(0, 229, 255, 0.12);
  color: #e2e8f0;
  padding: 1.5rem 1.75rem 1.35rem;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  transition: all 0.2s ease;
}

/* Top Accent Glow Bar */
.card-accent-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: #00e5ff;
}

.card-accent-bar.confirm,
.card-accent-bar.warning {
  background: #f59e0b;
}

.card-accent-bar.error {
  background: #ef4444;
}

.card-accent-bar.success {
  background: #10b981;
}

/* Top Header Bar */
.dialog-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.15rem;
  padding-right: 1.5rem;
}

.dialog-status-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.2rem 0.65rem;
  background: rgba(0, 229, 255, 0.1);
  border: 1px solid rgba(0, 229, 255, 0.3);
  border-radius: 9999px;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: #00e5ff;
  box-shadow: 0 0 6px #00e5ff;
}

.status-name {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #00e5ff;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

.dialog-node-tag {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: #64748b;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

/* Close Button */
.dialog-close-btn {
  position: absolute;
  top: 0.9rem;
  right: 0.9rem;
  background: transparent;
  border: none;
  color: #64748b;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s ease;
}

.dialog-close-btn svg {
  width: 16px;
  height: 16px;
}

.dialog-close-btn:hover {
  color: #00e5ff;
  background: rgba(0, 229, 255, 0.1);
}

/* Body Content */
.dialog-body {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.35rem;
}

.dialog-icon-box {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 229, 255, 0.12);
  border: 1px solid rgba(0, 229, 255, 0.35);
  color: #00e5ff;
}

.dialog-icon-box.confirm,
.dialog-icon-box.warning {
  background: rgba(245, 158, 11, 0.12);
  border-color: rgba(245, 158, 11, 0.4);
  color: #f59e0b;
}

.dialog-icon-box.error {
  background: rgba(239, 68, 68, 0.12);
  border-color: rgba(239, 68, 68, 0.4);
  color: #ef4444;
}

.dialog-icon-box.success {
  background: rgba(16, 185, 129, 0.12);
  border-color: rgba(16, 185, 129, 0.4);
  color: #10b981;
}

.dialog-type-icon {
  width: 22px;
  height: 22px;
}

.dialog-text-content {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.dialog-title {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: #ffffff;
}

.dialog-message {
  margin: 0;
  font-size: 0.82rem;
  line-height: 1.45;
  color: #94a3b8;
}

/* Footer Actions */
.dialog-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.65rem;
  padding-top: 0.95rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.btn-dialog-cancel {
  background: #111a2e;
  border: 1px solid #1e293b;
  border-radius: 6px;
  color: #94a3b8;
  padding: 0.5rem 1rem;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  transition: all 0.15s ease;
}

.btn-dialog-cancel:hover {
  background: #18243e;
  color: #ffffff;
  border-color: #334155;
}

.btn-dialog-confirm {
  background: #00e5ff;
  border: none;
  border-radius: 6px;
  color: #040810;
  padding: 0.5rem 1.15rem;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  box-shadow: 0 2px 10px rgba(0, 229, 255, 0.35);
  transition: all 0.15s ease;
}

.btn-dialog-confirm:hover {
  background: #38bdf8;
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(0, 229, 255, 0.5);
}

.btn-dialog-confirm.confirm {
  background: #ef4444;
  color: #ffffff;
  box-shadow: 0 2px 10px rgba(239, 68, 68, 0.35);
}

.btn-dialog-confirm.confirm:hover {
  background: #dc2626;
  box-shadow: 0 4px 14px rgba(239, 68, 68, 0.5);
}

.btn-dialog-confirm.warning {
  background: #f59e0b;
  color: #040810;
  box-shadow: 0 2px 10px rgba(245, 158, 11, 0.35);
}

.btn-dialog-confirm.warning:hover {
  background: #d97706;
}

/* =========================================================
   LIGHT MODE OVERRIDES FOR REUSABLE DIALOG
   ========================================================= */
.dialog-card.is-light,
:global([data-theme="light"]) .dialog-card {
  background: #ffffff !important;
  border: 1px solid #cbd5e1 !important;
  box-shadow: 0 25px 60px rgba(15, 23, 42, 0.18), 0 0 25px rgba(2, 132, 199, 0.12) !important;
  color: #0f172a !important;
}

.dialog-card.is-light .dialog-title,
:global([data-theme="light"]) .dialog-card .dialog-title {
  color: #0f172a !important;
}

.dialog-card.is-light .dialog-message,
:global([data-theme="light"]) .dialog-card .dialog-message {
  color: #475569 !important;
}

.dialog-card.is-light .dialog-status-pill,
:global([data-theme="light"]) .dialog-card .dialog-status-pill {
  background: rgba(2, 132, 199, 0.1) !important;
  border-color: rgba(2, 132, 199, 0.3) !important;
}

.dialog-card.is-light .status-name,
:global([data-theme="light"]) .dialog-card .status-name {
  color: #0284c7 !important;
}

.dialog-card.is-light .dialog-node-tag,
:global([data-theme="light"]) .dialog-card .dialog-node-tag {
  color: #64748b !important;
}

.dialog-card.is-light .dialog-close-btn,
:global([data-theme="light"]) .dialog-card .dialog-close-btn {
  color: #64748b !important;
}

.dialog-card.is-light .dialog-close-btn:hover,
:global([data-theme="light"]) .dialog-card .dialog-close-btn:hover {
  color: #0284c7 !important;
  background: rgba(2, 132, 199, 0.1) !important;
}

.dialog-card.is-light .dialog-footer,
:global([data-theme="light"]) .dialog-card .dialog-footer {
  border-top-color: #e2e8f0 !important;
}

.dialog-card.is-light .btn-dialog-cancel,
:global([data-theme="light"]) .dialog-card .btn-dialog-cancel {
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
  color: #475569 !important;
}

.dialog-card.is-light .btn-dialog-cancel:hover,
:global([data-theme="light"]) .dialog-card .btn-dialog-cancel:hover {
  background: #e2e8f0 !important;
  color: #0f172a !important;
}

.dialog-card.is-light .btn-dialog-confirm,
:global([data-theme="light"]) .dialog-card .btn-dialog-confirm {
  background: #0284c7 !important;
  color: #ffffff !important;
  box-shadow: 0 2px 10px rgba(2, 132, 199, 0.3) !important;
}

.dialog-card.is-light .btn-dialog-confirm:hover,
:global([data-theme="light"]) .dialog-card .btn-dialog-confirm:hover {
  background: #0369a1 !important;
}

.dialog-card.is-light .btn-dialog-confirm.confirm,
:global([data-theme="light"]) .dialog-card .btn-dialog-confirm.confirm {
  background: #dc2626 !important;
  color: #ffffff !important;
}
</style>

