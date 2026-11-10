<template>
  <div class="login-view-container" :class="{ 'is-light': !isDark, 'is-dark': isDark }">
    <!-- Top Utility Bar: Facility Node Info & Theme toggle -->
    <div class="login-utility-bar">
      <div class="utility-node-badge">
        <span class="node-pulse-dot"></span>
        <span class="node-title">AQUASYNC • WATER DESALINATION FACILITY #04</span>
      </div>

      <button
        type="button"
        class="utility-theme-btn"
        :title="isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
        @click="toggleTheme"
        aria-label="Toggle Theme"
      >
        <!-- Sun icon (shown in dark mode) -->
        <svg v-if="isDark" class="theme-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
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
        <!-- Moon icon (shown in light mode) -->
        <svg v-else class="theme-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
        </svg>
      </button>
    </div>

    <!-- Centered SCADA & AI Gateway Card -->
    <div class="login-view-card" role="main" aria-labelledby="view-login-title">
      <!-- Top Status Indicators -->
      <div class="card-status-bar">
        <div class="system-status-pill">
          <span class="pulse-indicator"></span>
          <span class="status-label">SYSTEM ONLINE</span>
        </div>
        <div class="network-metric">
          <span class="metric-text">TLS 1.3 • 3ms RTT</span>
        </div>
      </div>

      <!-- Center Branding & Logo -->
      <div class="card-header-branding">
        <div class="logo-box-glowing">
          <svg class="scada-droplet-icon" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="viewDropGlow" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#00e5ff" />
                <stop offset="100%" stop-color="#0077b6" />
              </linearGradient>
            </defs>
            <path
              d="M24 6C24 6 13 18.5 13 28C13 34.075 17.925 39 24 39C30.075 39 35 34.075 35 28C35 18.5 24 6 24 6Z"
              fill="url(#viewDropGlow)"
              opacity="0.9"
            />
            <!-- Internal steam / waveform lines -->
            <path d="M20 23C21.5 25 21.5 27 20 29" stroke="#ffffff" stroke-width="2" stroke-linecap="round" />
            <path d="M24 21C25.5 23 25.5 25 24 27M24 29C25.5 31 25.5 33 24 35" stroke="#ffffff" stroke-width="2" stroke-linecap="round" />
            <path d="M28 23C29.5 25 29.5 27 28 29" stroke="#ffffff" stroke-width="2" stroke-linecap="round" />
          </svg>
        </div>

        <h1 id="view-login-title" class="gateway-title">AquaSync SCADA &amp; AI Gateway</h1>
        <p class="gateway-subtitle">Zero-Trust Supervisory Control • Plant Node #04</p>
      </div>

      <!-- Alert Banners -->
      <transition name="alert-slide">
        <div v-if="errorMessage" class="login-alert alert-error">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
          <span>{{ errorMessage }}</span>
        </div>
      </transition>

      <transition name="alert-slide">
        <div v-if="successMessage" class="login-alert alert-success">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="20 6 9 17 4 12" />
          </svg>
          <span>{{ successMessage }}</span>
        </div>
      </transition>

      <!-- Main Login Form -->
      <form @submit.prevent="handleLogin" class="gateway-form">
        <!-- Field 1: USERNAME -->
        <div class="input-block">
          <label class="input-tag" for="gateway-username">USERNAME</label>
          <div class="input-shell">
            <input
              id="gateway-username"
              v-model="username"
              type="text"
              class="gateway-input"
              placeholder="op_sysadmin_04"
              autocomplete="username"
              required
              :disabled="isLoading"
            />
            <button
              v-if="username"
              type="button"
              class="btn-clear-value"
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
        <div class="input-block">
          <div class="input-tag-row">
            <label class="input-tag" for="gateway-password">PASSWORD</label>
            <a href="javascript:void(0)" class="forgot-pwd-link" @click="handleForgotPassword">Forgot Password?</a>
          </div>
          <div class="input-shell">
            <span class="icon-prefix">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                <path d="M7 11V7a5 5 0 0 1 10 0v4" />
              </svg>
            </span>
            <input
              id="gateway-password"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              class="gateway-input with-prefix with-suffix"
              placeholder="••••••••••••••••"
              autocomplete="current-password"
              required
              :disabled="isLoading"
            />
            <button
              type="button"
              class="btn-toggle-eye"
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

        <!-- Remember station checkbox -->
        <div class="station-checkbox-row">
          <label class="station-checkbox-label">
            <input
              type="checkbox"
              v-model="rememberStation"
              class="station-checkbox"
            />
            <span class="station-box-mark"></span>
            <span class="station-text">
              Remember station <span class="station-hmi-id">(DESAL-HMI-01)</span>
            </span>
          </label>
        </div>

        <!-- Primary Sign In Button -->
        <button
          type="submit"
          class="btn-gateway-signin"
          :disabled="isLoading || !username || !password"
        >
          <span v-if="!isLoading" class="btn-text-row">
            Sign In to SCADA Gateway <span class="arrow-sym">→</span>
          </span>
          <span v-else class="btn-loading-row">
            <span class="btn-loading-spinner"></span>
            <span>Verifying Operator Certificate...</span>
          </span>
        </button>

        <!-- Secondary PKI Hardware Token Button -->
        <button
          type="button"
          class="btn-gateway-token"
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
      <div class="card-footer-compliance">
        <div class="compliance-pill">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" class="shield-icon">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
            <polyline points="9 12 11 14 15 10" />
          </svg>
          <span class="compliance-text">SECURED VIA IEC 62443 INDUSTRIAL STANDARD</span>
        </div>
        <p class="audit-notice">Immutable cryptographic audit logging active on node USW2-EDGE-01</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDialog } from '../composables/useDialog'

const router = useRouter()
const dialog = useDialog()

const username = ref('op_sysadmin_04')
const password = ref('')
const showPassword = ref(false)
const rememberStation = ref(true)
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const isDark = ref(true)

onMounted(() => {
  const savedTheme = localStorage.getItem('theme') || 'dark'
  isDark.value = savedTheme !== 'light'
  document.documentElement.setAttribute('data-theme', isDark.value ? 'dark' : 'light')

  const savedUser = localStorage.getItem('scada_station_operator')
  if (savedUser) {
    username.value = savedUser
  }
})

const toggleTheme = () => {
  isDark.value = !isDark.value
  const theme = isDark.value ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
  window.dispatchEvent(new CustomEvent('theme-changed', { detail: { theme } }))
}

const handleLogin = async () => {
  errorMessage.value = ''
  successMessage.value = ''
  isLoading.value = true

  try {
    const res = await fetch('http://127.0.0.1:8000/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username.value.trim(),
        password: password.value
      })
    })

    const data = await res.json()

    if (!res.ok) {
      errorMessage.value = data.detail || 'Authentication failed. Please verify operator ID and password.'
      return
    }

    if (data.status === 'success' && data.access_token) {
      successMessage.value = `Access granted: Operator ${data.user?.username || username.value} authenticated`

      // Store JWT token & authenticated user profile
      localStorage.setItem('scada_access_token', data.access_token)
      localStorage.setItem('scada_user', JSON.stringify(data.user || { username: username.value }))
      if (data.user?.id) {
        localStorage.setItem('agent_session_id', String(data.user.id))
      }
      if (rememberStation.value) {
        localStorage.setItem('scada_station_operator', username.value.trim())
      }

      // Notify application of auth change
      window.dispatchEvent(new CustomEvent('auth-changed', {
        detail: {
          isAuthenticated: true,
          user: data.user || { username: username.value }
        }
      }))

      // Redirect to SCADA overview
      setTimeout(() => {
        router.push('/overview')
      }, 700)
    } else {
      errorMessage.value = 'Unrecognized response received from SCADA Gateway.'
    }
  } catch (err) {
    errorMessage.value = 'Failed to connect to SCADA Gateway on port 8000. Ensure server is running.'
  } finally {
    isLoading.value = false
  }
}

const handlePkiAuth = () => {
  errorMessage.value = ''
  successMessage.value = 'PKI token reader active: Insert FIDO2 / YubiKey hardware key into station.'
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
/* Full Page Container */
.login-view-container {
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1.25rem;
  background: radial-gradient(circle at 50% 30%, #0d1525 0%, #060911 70%, #030509 100%);
  position: relative;
  overflow-y: auto;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  transition: all 0.3s ease;
}

.login-view-container.is-light,
:global([data-theme="light"]) .login-view-container {
  background: radial-gradient(circle at 50% 30%, #f0f9ff 0%, #e2e8f0 70%, #cbd5e1 100%) !important;
}

/* Top Utility Bar */
.login-utility-bar {
  position: absolute;
  top: 1.5rem;
  left: 2rem;
  right: 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 10;
}

.utility-node-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  color: #94a3b8;
  font-size: 0.74rem;
  font-weight: 700;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  letter-spacing: 0.06em;
  padding: 0.4rem 0.85rem;
  border-radius: 6px;
  background: rgba(13, 21, 37, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.login-view-container.is-light .utility-node-badge,
:global([data-theme="light"]) .utility-node-badge {
  background: rgba(255, 255, 255, 0.9) !important;
  border-color: #cbd5e1 !important;
  color: #475569 !important;
}

.node-pulse-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: #00e5ff;
  box-shadow: 0 0 8px #00e5ff;
}

.login-view-container.is-light .node-pulse-dot,
:global([data-theme="light"]) .node-pulse-dot {
  background-color: #0284c7 !important;
  box-shadow: 0 0 8px #0284c7 !important;
}

.node-title {
  color: #cbd5e1;
}

.login-view-container.is-light .node-title,
:global([data-theme="light"]) .node-title {
  color: #334155 !important;
}

.utility-theme-btn {
  background: rgba(13, 21, 37, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.2s ease;
}

.login-view-container.is-light .utility-theme-btn,
:global([data-theme="light"]) .utility-theme-btn {
  background: rgba(255, 255, 255, 0.9) !important;
  border-color: #cbd5e1 !important;
  color: #475569 !important;
}

.utility-theme-btn:hover {
  color: #00e5ff;
  border-color: rgba(0, 229, 255, 0.4);
}

.login-view-container.is-light .utility-theme-btn:hover,
:global([data-theme="light"]) .utility-theme-btn:hover {
  color: #0284c7 !important;
  border-color: #0284c7 !important;
}

.theme-icon {
  width: 18px;
  height: 18px;
}

/* Centered SCADA Card */
.login-view-card {
  width: 100%;
  max-width: 440px;
  background: #0d1424;
  border: 1px solid rgba(0, 229, 255, 0.22);
  border-radius: 16px;
  box-shadow: 0 25px 65px rgba(0, 0, 0, 0.8), 0 0 45px rgba(0, 229, 255, 0.12);
  padding: 2rem 2.25rem 1.75rem;
  color: #e2e8f0;
  transition: all 0.25s ease;
  margin: auto 0;
}

.login-view-container.is-light .login-view-card,
:global([data-theme="light"]) .login-view-card {
  background: #ffffff !important;
  border: 1px solid rgba(2, 132, 199, 0.35) !important;
  box-shadow: 0 25px 60px rgba(15, 23, 42, 0.16), 0 0 35px rgba(2, 132, 199, 0.12) !important;
  color: #0f172a !important;
}

/* Card Status Bar */
.card-status-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.system-status-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.22rem 0.65rem;
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

.login-view-container.is-light .network-metric,
:global([data-theme="light"]) .network-metric {
  color: #0284c7 !important;
}

/* Header & Logo */
.card-header-branding {
  text-align: center;
  margin-bottom: 1.5rem;
}

.logo-box-glowing {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  background: linear-gradient(145deg, #131c31, #090e1a);
  border: 1px solid rgba(0, 229, 255, 0.45);
  border-radius: 14px;
  box-shadow: 0 0 25px rgba(0, 229, 255, 0.25);
  margin-bottom: 0.85rem;
}

.login-view-container.is-light .logo-box-glowing,
:global([data-theme="light"]) .logo-box-glowing {
  background: linear-gradient(145deg, #e0f2fe, #f0f9ff) !important;
  border: 1px solid rgba(2, 132, 199, 0.45) !important;
  box-shadow: 0 0 20px rgba(2, 132, 199, 0.2) !important;
}

.scada-droplet-icon {
  width: 38px;
  height: 38px;
}

.gateway-title {
  font-size: 1.38rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: #ffffff;
  margin: 0 0 0.35rem 0;
}

.login-view-container.is-light .gateway-title,
:global([data-theme="light"]) .gateway-title {
  color: #0f172a !important;
}

.gateway-subtitle {
  font-size: 0.76rem;
  font-weight: 500;
  color: #94a3b8;
  margin: 0;
  letter-spacing: 0.02em;
}

.login-view-container.is-light .gateway-subtitle,
:global([data-theme="light"]) .gateway-subtitle {
  color: #64748b !important;
}

/* Alert Banners */
.login-alert {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.65rem 0.85rem;
  border-radius: 8px;
  font-size: 0.8rem;
  margin-bottom: 1.15rem;
}

.login-alert svg {
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

/* Form Styles */
.gateway-form {
  display: flex;
  flex-direction: column;
  gap: 1.15rem;
}

.input-block {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.input-tag-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.input-tag {
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #94a3b8;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

.login-view-container.is-light .input-tag,
:global([data-theme="light"]) .input-tag {
  color: #334155 !important;
}

.forgot-pwd-link {
  font-size: 0.72rem;
  color: #00e5ff;
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.15s ease;
}

.login-view-container.is-light .forgot-pwd-link,
:global([data-theme="light"]) .forgot-pwd-link {
  color: #0284c7 !important;
}

.forgot-pwd-link:hover {
  text-decoration: underline;
  opacity: 0.85;
}

.input-shell {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

.icon-prefix {
  position: absolute;
  left: 0.85rem;
  color: #64748b;
  display: flex;
  align-items: center;
  pointer-events: none;
}

.icon-prefix svg {
  width: 16px;
  height: 16px;
}

.gateway-input {
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

.login-view-container.is-light .gateway-input,
:global([data-theme="light"]) .gateway-input {
  background: #f8fafc !important;
  border: 1.5px solid #cbd5e1 !important;
  color: #0f172a !important;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05) !important;
}

.gateway-input.with-prefix {
  padding-left: 2.35rem;
}

.gateway-input.with-suffix {
  padding-right: 2.35rem;
}

.gateway-input:focus {
  border-color: #00e5ff;
  box-shadow: 0 0 0 2px rgba(0, 229, 255, 0.2);
}

.login-view-container.is-light .gateway-input:focus,
:global([data-theme="light"]) .gateway-input:focus {
  border-color: #0284c7 !important;
  box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.25) !important;
}

.btn-clear-value,
.btn-toggle-eye {
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

.btn-clear-value svg,
.btn-toggle-eye svg {
  width: 16px;
  height: 16px;
}

.btn-clear-value:hover,
.btn-toggle-eye:hover {
  color: #00e5ff;
}

.login-view-container.is-light .btn-clear-value,
.login-view-container.is-light .btn-toggle-eye,
:global([data-theme="light"]) .btn-clear-value,
:global([data-theme="light"]) .btn-toggle-eye {
  color: #64748b !important;
}

.login-view-container.is-light .btn-clear-value:hover,
.login-view-container.is-light .btn-toggle-eye:hover,
:global([data-theme="light"]) .btn-clear-value:hover,
:global([data-theme="light"]) .btn-toggle-eye:hover {
  color: #0284c7 !important;
}

/* Remember station */
.station-checkbox-row {
  display: flex;
  align-items: center;
}

.station-checkbox-label {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  cursor: pointer;
  font-size: 0.8rem;
  color: #cbd5e1;
  user-select: none;
}

.login-view-container.is-light .station-checkbox-label,
:global([data-theme="light"]) .station-checkbox-label {
  color: #334155 !important;
}

.station-checkbox {
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

.login-view-container.is-light .station-checkbox,
:global([data-theme="light"]) .station-checkbox {
  background: #f1f5f9 !important;
  border-color: #94a3b8 !important;
}

.station-checkbox:checked {
  background: #00e5ff;
  border-color: #00e5ff;
}

.login-view-container.is-light .station-checkbox:checked,
:global([data-theme="light"]) .station-checkbox:checked {
  background: #0284c7 !important;
  border-color: #0284c7 !important;
}

.station-checkbox:checked::before {
  content: "";
  width: 9px;
  height: 5px;
  border-left: 2px solid #090e1a;
  border-bottom: 2px solid #090e1a;
  transform: rotate(-45deg) translate(1px, -1px);
}

.login-view-container.is-light .station-checkbox:checked::before,
:global([data-theme="light"]) .station-checkbox:checked::before {
  border-color: #ffffff !important;
}

.station-hmi-id {
  color: #00e5ff;
  font-weight: 600;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

.login-view-container.is-light .station-hmi-id,
:global([data-theme="light"]) .station-hmi-id {
  color: #0284c7 !important;
}

/* Primary Sign In Button */
.btn-gateway-signin {
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

.login-view-container.is-light .btn-gateway-signin,
:global([data-theme="light"]) .btn-gateway-signin {
  background: #0284c7 !important;
  color: #ffffff !important;
  box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35) !important;
}

.btn-gateway-signin:hover:not(:disabled) {
  background: #38bdf8;
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(0, 229, 255, 0.5);
}

.login-view-container.is-light .btn-gateway-signin:hover:not(:disabled),
:global([data-theme="light"]) .btn-gateway-signin:hover:not(:disabled) {
  background: #0369a1 !important;
  box-shadow: 0 6px 18px rgba(2, 132, 199, 0.45) !important;
}

.btn-gateway-signin:disabled {
  opacity: 0.55;
  cursor: not-allowed;
  transform: none;
}

.arrow-sym {
  margin-left: 0.4rem;
  font-size: 1.1rem;
}

.btn-loading-row {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-loading-spinner {
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

/* Secondary Button */
.btn-gateway-token {
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

.login-view-container.is-light .btn-gateway-token,
:global([data-theme="light"]) .btn-gateway-token {
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
  color: #475569 !important;
}

.btn-gateway-token:hover:not(:disabled) {
  background: #18243e;
  border-color: #38bdf8;
  color: #00e5ff;
}

.login-view-container.is-light .btn-gateway-token:hover:not(:disabled),
:global([data-theme="light"]) .btn-gateway-token:hover:not(:disabled) {
  background: #e2e8f0 !important;
  border-color: #0284c7 !important;
  color: #0284c7 !important;
}

.key-icon {
  width: 14px;
  height: 14px;
}

/* Footer Compliance */
.card-footer-compliance {
  margin-top: 1.75rem;
  padding-top: 1.15rem;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  align-items: center;
}

.login-view-container.is-light .card-footer-compliance,
:global([data-theme="light"]) .card-footer-compliance {
  border-top-color: rgba(0, 0, 0, 0.08) !important;
}

.compliance-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  color: #10b981;
}

.shield-icon {
  width: 13px;
  height: 13px;
}

.compliance-text {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.05em;
}

.audit-notice {
  margin: 0;
  font-size: 0.67rem;
  color: #64748b;
  letter-spacing: 0.01em;
}
</style>

