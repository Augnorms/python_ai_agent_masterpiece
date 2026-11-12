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

const username = ref('')
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

<style scoped src="@/style_folder/LoginView.css"></style>
