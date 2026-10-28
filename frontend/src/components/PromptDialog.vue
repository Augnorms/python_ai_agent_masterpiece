<template>
  <transition name="dialog-fade">
    <div
      v-if="isOpen"
      class="dialog-backdrop"
      tabindex="-1"
      @keydown.esc="onCancel"
      @click.self="onCancel"
    >
      <div class="dialog-card" :class="`variant-${variant}`" role="dialog" aria-modal="true">
        <!-- Top Glowing Bar -->
        <div class="dialog-glow-bar"></div>

        <!-- Header -->
        <div class="dialog-header">
          <div class="header-left">
            <div class="dialog-icon-box" :class="`icon-${variant}`">
              <!-- Danger Icon -->
              <svg v-if="variant === 'danger'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
                <line x1="12" y1="9" x2="12" y2="13" />
                <line x1="12" y1="17" x2="12.01" y2="17" />
              </svg>
              <!-- Warning Icon -->
              <svg v-else-if="variant === 'warning'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="8" x2="12" y2="12" />
                <line x1="12" y1="16" x2="12.01" y2="16" />
              </svg>
              <!-- Info / Primary Icon -->
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="16" x2="12" y2="12" />
                <line x1="12" y1="8" x2="12.01" y2="8" />
              </svg>
            </div>

            <div class="header-text">
              <div class="title-row">
                <h3 class="dialog-title">{{ title }}</h3>
                <span v-if="badge" class="dialog-badge" :class="`badge-${variant}`">{{ badge }}</span>
              </div>
              <p v-if="subtitle" class="dialog-subtitle">{{ subtitle }}</p>
            </div>
          </div>

          <button class="close-btn" @click="onCancel" :disabled="isLoading" title="Close dialog">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="18" x2="18" y2="6" />
            </svg>
          </button>
        </div>

        <!-- Body Message & Context -->
        <div class="dialog-body">
          <p class="dialog-message">{{ message }}</p>

          <!-- Optional Input Field (Prompt style) -->
          <div v-if="showInput" class="input-wrapper">
            <label v-if="inputLabel" class="input-label">{{ inputLabel }}</label>
            <input
              ref="inputFieldRef"
              v-model="inputVal"
              type="text"
              class="dialog-input"
              :placeholder="inputPlaceholder"
              :disabled="isLoading"
              @keyup.enter="onConfirm"
            />
          </div>

          <!-- Slot for additional custom content -->
          <slot />
        </div>

        <!-- Footer Buttons -->
        <div class="dialog-footer">
          <button
            type="button"
            class="btn-dialog btn-cancel"
            :disabled="isLoading"
            @click="onCancel"
          >
            {{ cancelText }}
          </button>

          <button
            type="button"
            class="btn-dialog btn-confirm"
            :class="`btn-${variant}`"
            :disabled="isLoading || (requireInput && !inputVal.trim())"
            @click="onConfirm"
          >
            <svg
              v-if="isLoading"
              class="spin-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <polyline points="23 4 23 10 17 10" />
              <polyline points="1 20 1 14 7 14" />
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
            </svg>
            <span>{{ isLoading ? loadingText : confirmText }}</span>
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Confirm Action'
  },
  subtitle: {
    type: String,
    default: ''
  },
  message: {
    type: String,
    default: 'Are you sure you want to proceed with this action?'
  },
  badge: {
    type: String,
    default: ''
  },
  variant: {
    type: String,
    default: 'danger', // 'danger' | 'warning' | 'primary'
    validator: (val) => ['danger', 'warning', 'primary'].includes(val)
  },
  confirmText: {
    type: String,
    default: 'Confirm'
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  },
  loadingText: {
    type: String,
    default: 'Processing...'
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  showInput: {
    type: Boolean,
    default: false
  },
  inputLabel: {
    type: String,
    default: ''
  },
  inputPlaceholder: {
    type: String,
    default: 'Type your response here...'
  },
  defaultValue: {
    type: String,
    default: ''
  },
  requireInput: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['confirm', 'cancel', 'close'])

const inputVal = ref(props.defaultValue)
const inputFieldRef = ref(null)

watch(
  () => props.isOpen,
  (newVal) => {
    if (newVal) {
      inputVal.value = props.defaultValue
      if (props.showInput) {
        nextTick(() => {
          if (inputFieldRef.value) {
            inputFieldRef.value.focus()
          }
        })
      }
    }
  }
)

const onCancel = () => {
  if (props.isLoading) return
  emit('cancel')
  emit('close')
}

const onConfirm = () => {
  if (props.isLoading) return
  if (props.requireInput && !inputVal.value.trim()) return
  emit('confirm', props.showInput ? inputVal.value : true)
}
</script>

<style scoped>
.dialog-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(3, 7, 18, 0.78);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2200;
  padding: 16px;
}

.dialog-fade-enter-active,
.dialog-fade-leave-active {
  transition: opacity 0.18s ease-out;
}

.dialog-fade-enter-from,
.dialog-fade-leave-to {
  opacity: 0;
}

.dialog-fade-enter-active .dialog-card {
  animation: popIn 0.18s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes popIn {
  from {
    transform: scale(0.96) translateY(4px);
    opacity: 0;
  }
  to {
    transform: scale(1) translateY(0);
    opacity: 1;
  }
}

.dialog-card {
  width: 520px;
  max-width: 94vw;
  background: var(--bg-card, #0d1527);
  border: 1px solid var(--border-color, #17243c);
  border-radius: 12px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.55), 0 0 20px rgba(0, 0, 0, 0.3);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* Variant Border Highlights */
.dialog-card.variant-danger {
  border-color: rgba(239, 68, 68, 0.4);
  box-shadow: 0 20px 45px rgba(0, 0, 0, 0.6), 0 0 25px rgba(239, 68, 68, 0.18);
}
.dialog-card.variant-warning {
  border-color: rgba(245, 158, 11, 0.4);
  box-shadow: 0 20px 45px rgba(0, 0, 0, 0.6), 0 0 25px rgba(245, 158, 11, 0.18);
}
.dialog-card.variant-primary {
  border-color: rgba(0, 229, 255, 0.4);
  box-shadow: 0 20px 45px rgba(0, 0, 0, 0.6), 0 0 25px rgba(0, 229, 255, 0.18);
}

/* Glowing Top Line */
.dialog-glow-bar {
  height: 3px;
  width: 100%;
}
.variant-danger .dialog-glow-bar {
  background: linear-gradient(90deg, #ef4444 0%, #f97316 100%);
  box-shadow: 0 0 10px rgba(239, 68, 68, 0.8);
}
.variant-warning .dialog-glow-bar {
  background: linear-gradient(90deg, #f59e0b 0%, #eab308 100%);
  box-shadow: 0 0 10px rgba(245, 158, 11, 0.8);
}
.variant-primary .dialog-glow-bar {
  background: linear-gradient(90deg, #00e5ff 0%, #9d72ff 100%);
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.8);
}

/* Header */
.dialog-header {
  padding: 18px 20px 14px 20px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.dialog-icon-box {
  width: 38px;
  height: 38px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.dialog-icon-box svg {
  width: 20px;
  height: 20px;
}

.icon-danger {
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.4);
  color: #ef4444;
}
.icon-warning {
  background: rgba(245, 158, 11, 0.15);
  border: 1px solid rgba(245, 158, 11, 0.4);
  color: #f59e0b;
}
.icon-primary {
  background: rgba(0, 229, 255, 0.15);
  border: 1px solid rgba(0, 229, 255, 0.4);
  color: var(--primary-cyan, #00e5ff);
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dialog-title {
  font-size: 14.5px;
  font-weight: 700;
  color: var(--text-main, #ffffff);
  margin: 0;
  letter-spacing: -0.2px;
}

.dialog-subtitle {
  font-size: 11px;
  color: var(--text-muted, #94a3b8);
  margin: 0;
}

.dialog-badge {
  font-size: 9.5px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 4px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}
.badge-danger {
  background: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.4);
}
.badge-warning {
  background: rgba(245, 158, 11, 0.2);
  color: #fde68a;
  border: 1px solid rgba(245, 158, 11, 0.4);
}
.badge-primary {
  background: rgba(0, 229, 255, 0.2);
  color: #67e8f9;
  border: 1px solid rgba(0, 229, 255, 0.4);
}

.close-btn {
  background: transparent;
  border: none;
  color: var(--text-muted, #94a3b8);
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all 0.15s;
}
.close-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.08);
  color: var(--text-main, #ffffff);
}
.close-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.close-btn svg {
  width: 16px;
  height: 16px;
}

/* Body */
.dialog-body {
  padding: 4px 20px 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.dialog-message {
  font-size: 12.5px;
  line-height: 1.55;
  color: var(--text-muted, #94a3b8);
  margin: 0;
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-top: 4px;
}

.input-label {
  font-size: 10.5px;
  font-weight: 600;
  color: var(--text-muted, #94a3b8);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.dialog-input {
  background: var(--bg-card-inner, #0a101f);
  border: 1px solid var(--border-color, #17243c);
  border-radius: 7px;
  color: var(--text-main, #ffffff);
  font-size: 12px;
  padding: 8px 12px;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  font-family: inherit;
}
.dialog-input:focus {
  border-color: var(--primary-cyan, #00e5ff);
  box-shadow: 0 0 0 2px rgba(0, 229, 255, 0.15);
}

/* Footer */
.dialog-footer {
  padding: 12px 20px;
  background: var(--bg-card-inner, #0a101f);
  border-top: 1px solid var(--border-color, #17243c);
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
}

.btn-dialog {
  padding: 7px 15px;
  border-radius: 6px;
  font-size: 11.5px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.18s;
  border: none;
}

.btn-cancel {
  background: transparent;
  border: 1px solid var(--border-color, #17243c);
  color: var(--text-muted, #94a3b8);
}
.btn-cancel:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-main, #ffffff);
}

.btn-confirm.btn-danger {
  background: #ef4444;
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.35);
}
.btn-confirm.btn-danger:hover:not(:disabled) {
  background: #dc2626;
  box-shadow: 0 2px 12px rgba(239, 68, 68, 0.5);
}

.btn-confirm.btn-warning {
  background: #f59e0b;
  color: #0f172a;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.35);
}
.btn-confirm.btn-warning:hover:not(:disabled) {
  background: #d97706;
}

.btn-confirm.btn-primary {
  background: var(--primary-cyan, #00e5ff);
  color: #060a14;
  box-shadow: 0 2px 8px rgba(0, 229, 255, 0.35);
}
.btn-confirm.btn-primary:hover:not(:disabled) {
  background: #38bdf8;
}

.btn-dialog:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spin-icon {
  width: 13px;
  height: 13px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}
</style>

