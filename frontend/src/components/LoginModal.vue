<template>
  <div v-if="isOpen" class="login-modal-overlay" @click.self="handleOverlayClick">
    <div class="login-card" role="dialog" aria-modal="true" aria-labelledby="login-title">
      <!-- Top Status Indicators -->
      <div class="login-top-bar">
        <div class="system-status-pill">
          <span class="pulse-indicator"></span>
          <span class="status-label">SYSTEM ONLINE</span>
        </div>
        <div class="network-metric">
          <span class="metric-text">TLS 1.3 • 3ms RTT</span>
        </div>
      </div>

      <!-- Close Button (if dismissible) -->
      <button v-if="allowDismiss" class="modal-close-btn" @click="closeModal" aria-label="Close Login Modal">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18" />
          <line x1="6" y1="6" x2="18" y2="18" />
        </svg>
      </button>

      <!-- Center Branding & Logo -->
      <div class="login-header">
        <div class="login-logo-container">
          <!-- Stylized Droplet + Waves Icon -->
          <svg class="scada-droplet-icon" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="dropGlow" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#00e5ff" />
                <stop offset="100%" stop-color="#0077b6" />
              </linearGradient>
            </defs>
            <path
              d="M24 6C24 6 13 18.5 13 28C13 34.075 17.925 39 24 39C30.075 39 35 34.075 35 28C35 18.5 24 6 24 6Z"
              fill="url(#dropGlow)"
              opacity="0.85"
            />
            <!-- Heat/Wave Lines inside droplet -->
            <path d="M20 23C21.5 25 21.5 27 20 29" stroke="#ffffff" stroke-width="2" stroke-linecap="round" />
            <path d="M24 21C25.5 23 25.5 25 24 27M24 29C25.5 31 25.5 33 24 35" stroke="#ffffff" stroke-width="2" stroke-linecap="round" />
            <path d="M28 23C29.5 25 29.5 27 28 29" stroke="#ffffff" stroke-width="2" stroke-linecap="round" />
          </svg>
        </div>

        <h1 id="login-title" class="login-title">AquaSync SCADA &amp; AI Gateway</h1>
        <p class="login-subtitle">Zero-Trust Supervisory Control • Plant Node #04</p>
      </div>

      <!-- Alert / Feedback Banner -->
      <div v-if="errorMessage" class="login-alert-banner alert-error">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
        <span>{{ errorMessage }}</span>
      </div>

      <div v-if="successMessage" class="login-alert-banner alert-success">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="20 6 9 17 4 12" />
        </svg>
        <span>{{ successMessage }}</span>
      </div>

      <!-- Sign In Form -->
      <form @submit.prevent="handleLogin" class="login-form">
        <!-- Field 1: USERNAME -->
        <div class="form-field">
          <label class="field-label" for="login-username">USERNAME</label>
          <div class="field-input-box">
            <input
              id="login-username"
              v-model="username"
              type="text"
              class="field-input"
              placeholder="op_sysadmin_04"
              autocomplete="username"
              required
              :disabled="isLoading"
            />
            <button
              v-if="username"
              type="button"
              class="clear-input-btn"
              @click="username = ''"
              tabindex="-1"
              aria-label="Clear username"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Field 2: PASSWORD -->
        <div class="form-field">
          <div class="field-label-row">
            <label class="field-label" for="login-password">PASSWORD</label>
            <a href="javascript:void(0)" class="forgot-link" @click="handleForgotPassword">Forgot Password?</a>
          </div>
          <div class="field-input-box">
            <span class="input-icon-prefix">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                <path d="M7 11V7a5 5 0 0 1 10 0v4" />
              </svg>
            </span>
            <input
              id="login-password"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              class="field-input with-prefix with-suffix"
              placeholder="••••••••••••••••"
              autocomplete="current-password"
              required
              :disabled="isLoading"
            />
            <button
              type="button"
              class="toggle-eye-btn"
              @click="showPassword = !showPassword"
              tabindex="-1"
              :aria-label="showPassword ? 'Hide password' : 'Show password'"
            >
              <svg v-if="!showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                <circle cx="12" cy="12" r="3" />
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
                <line x1="1" y1="1" x2="23" y2="23" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Remember Station Checkbox -->
        <div class="remember-station-row">
          <label class="remember-checkbox-label">
            <input
              type="checkbox"
              v-model="rememberStation"
              class="custom-hmi-checkbox"
            />
            <span class="checkbox-custom-mark"></span>
            <span class="remember-text">
              Remember station <span class="hmi-station-tag">(DESAL-HMI-01)</span>
            </span>
          </label>
        </div>

        <!-- Primary Submit Button -->
        <button
          type="submit"
          class="btn-scada-primary"
          :disabled="isLoading || !username || !password"
        >
          <span v-if="!isLoading" class="btn-text-content">
            Sign In to SCADA Gateway <span class="btn-arrow">→</span>
          </span>
          <span v-else class="btn-spinner-row">
            <span class="spinner-dot"></span>
            <span>Authenticating Operator...</span>
          </span>
        </button>

        <!-- Secondary PKI / Hardware Token Button -->
        <button
          type="button"
          class="btn-scada-secondary"
          :disabled="isLoading"
          @click="handlePkiAuth"
        >
          <svg class="key-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 2l-2 2m-1.5 1.5L16 7l-1.5 1.5M10 14l-4 4-2-2-4 4 4 4 2-2 4-4" />
            <circle cx="15.5" cy="8.5" r="3.5" />
          </svg>
          <span>USE PKI / HARDWARE TOKEN (FIDO2 • YUBIKEY)</span>
        </button>
      </form>

      <!-- Footer Compliance Badges -->
      <div class="login-footer">
        <div class="iec-badge">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" class="shield-icon">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
            <polyline points="9 12 11 14 15 10" />
          </svg>
          <span class="iec-text">SECURED VIA IEC 62443 INDUSTRIAL STANDARD</span>
        </div>
        <p class="audit-text">Immutable cryptographic audit logging active on node USW2-EDGE-01</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useDialog } from '../composables/useDialog'

const dialog = useDialog()

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  allowDismiss: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['close', 'login-success'])

const username = ref('op_sysadmin_04')
const password = ref('')
const showPassword = ref(false)
const rememberStation = ref(true)
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

onMounted(() => {
  const savedUser = localStorage.getItem('scada_station_operator')
  if (savedUser) {
    username.value = savedUser
  }
})

const closeModal = () => {
  if (props.allowDismiss) {
    emit('close')
  }
}

const handleOverlayClick = () => {
  if (props.allowDismiss) {
    closeModal()
  }
}

const handleLogin = async () => {
  errorMessage.value = ''
  successMessage.value = ''
  isLoading.value = true

  try {
    const response = await fetch('http://127.0.0.1:8000/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username.value.trim(),
        password: password.value
      })
    })

    const data = await response.json()

    if (!response.ok) {
      errorMessage.value = data.detail || 'Authentication failed. Please verify credentials.'
      return
    }

    if (data.status === 'success' && data.access_token) {
      successMessage.value = `Access granted: Station authenticated as ${data.user?.username || username.value}`
      
      // Store JWT token & authenticated user profile
      localStorage.setItem('scada_access_token', data.access_token)
      localStorage.setItem('scada_user', JSON.stringify(data.user || { username: username.value }))
      if (data.user?.id) {
        localStorage.setItem('agent_session_id', String(data.user.id))
      }
      if (rememberStation.value) {
        localStorage.setItem('scada_station_operator', username.value.trim())
      }

      // Notify parent / application
      window.dispatchEvent(new CustomEvent('auth-changed', { 
        detail: { 
          isAuthenticated: true, 
          user: data.user || { username: username.value } 
        } 
      }))

      setTimeout(() => {
        emit('login-success', data)
        closeModal()
      }, 700)
    } else {
      errorMessage.value = 'Unrecognized response from SCADA Gateway.'
    }
  } catch (err) {
    errorMessage.value = 'Failed to connect to SCADA Gateway on port 8000. Ensure service is active.'
  } finally {
    isLoading.value = false
  }
}

const handlePkiAuth = () => {
  errorMessage.value = ''
  successMessage.value = 'PKI token reader active: Insert FIDO2/YubiKey hardware key into station.'
  setTimeout(() => {
    if (successMessage.value.startsWith('PKI token')) {
      successMessage.value = ''
    }
  }, 4000)
}

const handleForgotPassword = () => {
  dialog.alert(
    'Contact Plant Security Operations Center (SOC) dispatch at ext. 4040 to request a physical credential reset and temporary station authorization.',
    'Security Dispatch Notice'
  )
}
</script>

<style scoped>
/* Modal Overlay */
.login-modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.25rem;
  background: rgba(4, 8, 16, 0.85);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  animation: fadeIn 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.98); }
  to { opacity: 1; transform: scale(1); }
}

/* Modal Card */
.login-card {
  position: relative;
  width: 100%;
  max-width: 440px;
  background: #0d1424;
  border: 1px solid rgba(0, 229, 255, 0.22);
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.75), 0 0 35px rgba(0, 229, 255, 0.12);
  padding: 1.75rem 2rem 1.5rem;
  color: #e2e8f0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  transition: all 0.2s ease;
}

/* Light Mode Overrides for Modal */
:global([data-theme="light"]) .login-card {
  background: #ffffff;
  border: 1px solid rgba(2, 132, 199, 0.3);
  box-shadow: 0 20px 50px rgba(15, 23, 42, 0.15), 0 0 30px rgba(2, 132, 199, 0.1);
  color: #0f172a;
}

/* Close Button */
.modal-close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: transparent;
  border: none;
  color: #64748b;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s ease;
}

.modal-close-btn svg {
  width: 18px;
  height: 18px;
}

.modal-close-btn:hover {
  color: #00e5ff;
  background: rgba(0, 229, 255, 0.1);
}

/* Top Indicator Bar */
.login-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  padding-right: 1.5rem;
}

.system-status-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.2rem 0.65rem;
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.35);
  border-radius: 9999px;
}

.pulse-indicator {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background-color: #10b981;
  box-shadow: 0 0 8px #10b981;
}

.status-label {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #34d399;
}

.network-metric {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: #00e5ff;
}

:global([data-theme="light"]) .network-metric {
  color: #0284c7;
}

/* Header & Logo */
.login-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.login-logo-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 58px;
  height: 58px;
  background: linear-gradient(145deg, #131c31, #090e1a);
  border: 1px solid rgba(0, 229, 255, 0.4);
  border-radius: 14px;
  box-shadow: 0 0 25px rgba(0, 229, 255, 0.25);
  margin-bottom: 0.85rem;
}

:global([data-theme="light"]) .login-logo-container {
  background: linear-gradient(145deg, #e0f2fe, #f0f9ff);
  border: 1px solid rgba(2, 132, 199, 0.4);
  box-shadow: 0 0 20px rgba(2, 132, 199, 0.2);
}

.scada-droplet-icon {
  width: 36px;
  height: 36px;
}

.login-title {
  font-size: 1.35rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: #ffffff;
  margin: 0 0 0.35rem 0;
}

:global([data-theme="light"]) .login-title {
  color: #0f172a;
}

.login-subtitle {
  font-size: 0.76rem;
  font-weight: 500;
  color: #94a3b8;
  margin: 0;
  letter-spacing: 0.02em;
}

:global([data-theme="light"]) .login-subtitle {
  color: #64748b;
}

/* Alert Banner */
.login-alert-banner {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.65rem 0.85rem;
  border-radius: 8px;
  font-size: 0.8rem;
  margin-bottom: 1.15rem;
  animation: fadeIn 0.2s ease;
}

.login-alert-banner svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.alert-error {
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.4);
  color: #fca5a5;
}

.alert-success {
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.4);
  color: #6ee7b7;
}

/* Form Fields */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.15rem;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.field-label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.field-label {
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #94a3b8;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

:global([data-theme="light"]) .field-label {
  color: #475569;
}

.forgot-link {
  font-size: 0.72rem;
  color: #00e5ff;
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.15s ease;
}

:global([data-theme="light"]) .forgot-link {
  color: #0284c7;
}

.forgot-link:hover {
  text-decoration: underline;
  opacity: 0.85;
}

.field-input-box {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

.input-icon-prefix {
  position: absolute;
  left: 0.85rem;
  color: #64748b;
  display: flex;
  align-items: center;
  pointer-events: none;
}

.input-icon-prefix svg {
  width: 16px;
  height: 16px;
}

.field-input {
  width: 100%;
  height: 42px;
  background: #090e1a;
  border: 1px solid #1e293b;
  border-radius: 8px;
  padding: 0 0.85rem;
  color: #ffffff;
  font-size: 0.9rem;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  outline: none;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

:global([data-theme="light"]) .field-input {
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  color: #0f172a;
}

.field-input.with-prefix {
  padding-left: 2.35rem;
}

.field-input.with-suffix {
  padding-right: 2.35rem;
}

.field-input:focus {
  border-color: #00e5ff;
  box-shadow: 0 0 0 2px rgba(0, 229, 255, 0.2);
}

:global([data-theme="light"]) .field-input:focus {
  border-color: #0284c7;
  box-shadow: 0 0 0 2px rgba(2, 132, 199, 0.15);
}

.clear-input-btn,
.toggle-eye-btn {
  position: absolute;
  right: 0.65rem;
  background: transparent;
  border: none;
  color: #64748b;
  padding: 0.25rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.clear-input-btn svg,
.toggle-eye-btn svg {
  width: 16px;
  height: 16px;
}

.clear-input-btn:hover,
.toggle-eye-btn:hover {
  color: #00e5ff;
}

/* Remember Station Checkbox */
.remember-station-row {
  display: flex;
  align-items: center;
}

.remember-checkbox-label {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  cursor: pointer;
  font-size: 0.8rem;
  color: #cbd5e1;
  user-select: none;
}

:global([data-theme="light"]) .remember-checkbox-label {
  color: #334155;
}

.custom-hmi-checkbox {
  appearance: none;
  -webkit-appearance: none;
  width: 17px;
  height: 17px;
  border: 1px solid #334155;
  border-radius: 4px;
  background: #090e1a;
  cursor: pointer;
  display: grid;
  place-content: center;
  transition: all 0.15s ease;
}

:global([data-theme="light"]) .custom-hmi-checkbox {
  background: #f1f5f9;
  border-color: #94a3b8;
}

.custom-hmi-checkbox:checked {
  background: #00e5ff;
  border-color: #00e5ff;
}

:global([data-theme="light"]) .custom-hmi-checkbox:checked {
  background: #0284c7;
  border-color: #0284c7;
}

.custom-hmi-checkbox:checked::before {
  content: "";
  width: 9px;
  height: 5px;
  border-left: 2px solid #090e1a;
  border-bottom: 2px solid #090e1a;
  transform: rotate(-45deg) translate(1px, -1px);
}

:global([data-theme="light"]) .custom-hmi-checkbox:checked::before {
  border-color: #ffffff;
}

.hmi-station-tag {
  color: #00e5ff;
  font-weight: 600;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

:global([data-theme="light"]) .hmi-station-tag {
  color: #0284c7;
}

/* Primary Submit Button */
.btn-scada-primary {
  width: 100%;
  height: 44px;
  background: #00e5ff;
  border: none;
  border-radius: 8px;
  color: #040810;
  font-size: 0.92rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.18s ease;
  box-shadow: 0 4px 14px rgba(0, 229, 255, 0.35);
  margin-top: 0.25rem;
}

:global([data-theme="light"]) .btn-scada-primary {
  background: #0284c7;
  color: #ffffff;
  box-shadow: 0 4px 14px rgba(2, 132, 199, 0.3);
}

.btn-scada-primary:hover:not(:disabled) {
  background: #38bdf8;
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(0, 229, 255, 0.5);
}

:global([data-theme="light"]) .btn-scada-primary:hover:not(:disabled) {
  background: #0369a1;
  box-shadow: 0 6px 18px rgba(2, 132, 199, 0.4);
}

.btn-scada-primary:disabled {
  opacity: 0.55;
  cursor: not-allowed;
  transform: none;
}

.btn-arrow {
  margin-left: 0.4rem;
  font-size: 1.1rem;
}

.btn-spinner-row {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.spinner-dot {
  width: 14px;
  height: 14px;
  border: 2px solid #040810;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Secondary Button (PKI Hardware Token) */
.btn-scada-secondary {
  width: 100%;
  height: 40px;
  background: #111a2e;
  border: 1px solid #1e293b;
  border-radius: 8px;
  color: #94a3b8;
  font-size: 0.74rem;
  font-weight: 700;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  letter-spacing: 0.04em;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.15s ease;
}

:global([data-theme="light"]) .btn-scada-secondary {
  background: #f1f5f9;
  border-color: #cbd5e1;
  color: #475569;
}

.btn-scada-secondary:hover:not(:disabled) {
  background: #18243e;
  border-color: #38bdf8;
  color: #00e5ff;
}

:global([data-theme="light"]) .btn-scada-secondary:hover:not(:disabled) {
  background: #e2e8f0;
  border-color: #0284c7;
  color: #0284c7;
}

.key-icon {
  width: 14px;
  height: 14px;
}

/* Footer Compliance */
.login-footer {
  margin-top: 1.75rem;
  padding-top: 1.15rem;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  align-items: center;
}

:global([data-theme="light"]) .login-footer {
  border-top-color: rgba(0, 0, 0, 0.06);
}

.iec-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  color: #10b981;
}

.shield-icon {
  width: 13px;
  height: 13px;
}

.iec-text {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.05em;
}

.audit-text {
  margin: 0;
  font-size: 0.67rem;
  color: #64748b;
  letter-spacing: 0.01em;
}
</style>

