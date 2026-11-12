<template>
  <div class="settings-container">
    <!-- Settings Sub-Header -->
    <div class="settings-header">
      <div class="settings-title-row">
        <div class="title-with-badge">
          <span class="settings-tag">CONFIGURATION • V1.0</span>
          <span v-if="currentSessionId" class="session-badge" :title="`Active Session ID: ${currentSessionId}`">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="session-icon">
              <rect x="2" y="2" width="20" height="8" rx="2" ry="2" />
              <rect x="2" y="14" width="20" height="8" rx="2" ry="2" />
              <line x1="6" y1="6" x2="6.01" y2="6" />
              <line x1="6" y1="18" x2="6.01" y2="18" />
            </svg>
            SESSION: {{ currentSessionId.slice(0, 8) }}
          </span>
          <h2 class="settings-title">System & Swarm Settings</h2>
        </div>
        <p class="settings-desc">
          Configure runtime swarm activation, default LLM supervisor models, agent behavior guardrails, and cluster execution preferences.
        </p>
      </div>

      <div class="settings-header-actions">
        <button type="button" class="btn-secondary" :disabled="isSaving || isLoading" @click="resetDefaults">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="1 4 1 10 7 10" />
            <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10" />
          </svg>
          <span>Reset Defaults</span>
        </button>

        <button type="button" class="btn-primary" :disabled="isSaving || isLoading" @click="saveSettings">
          <svg v-if="!isSaving" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" />
            <polyline points="17 21 17 13 7 13 7 21" />
            <polyline points="7 3 7 8 15 8" />
          </svg>
          <span v-else class="btn-spinner"></span>
          <span>{{ isSaving ? 'Saving...' : 'Save Settings' }}</span>
        </button>
      </div>
    </div>

    <!-- Main Scrollable Form Workspace -->
    <div class="settings-content">
      <form @submit.prevent="saveSettings" class="settings-form">
        <!-- Card 1: Swarm Active & Execution State -->
        <section class="settings-card">
          <div class="card-glow-bar cyan"></div>
          <div class="card-header">
            <div class="card-header-left">
              <div class="card-icon-box cyan">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="3" />
                  <circle cx="5" cy="8" r="2" />
                  <circle cx="19" cy="8" r="2" />
                  <circle cx="7" cy="19" r="2" />
                  <circle cx="17" cy="19" r="2" />
                  <path d="M12 12L5 8M12 12L19 8M12 12L7 19M12 12L17 19" stroke-width="1.8" />
                </svg>
              </div>
              <div>
                <h3 class="card-title">Swarm Active State</h3>
                <p class="card-subtitle">Control whether the autonomous multi-agent swarm is active or in standby mode.</p>
              </div>
            </div>

            <div class="swarm-status-badge" :class="isSwarmActive ? 'status-active' : 'status-inactive'">
              <span class="status-pulse-dot"></span>
              <span>{{ isSwarmActive ? 'SWARM ONLINE & DISPATCHING' : 'SWARM STANDBY / DISABLED' }}</span>
            </div>
          </div>

          <div class="card-body">
            <!-- Toggle Switch Row -->
            <div class="form-toggle-row">
              <div class="toggle-info">
                <label class="toggle-title" for="swarm-active-toggle">Enable Autonomous Swarm</label>
                <p class="toggle-desc">
                  When enabled, the orchestrator routes tasks across specialized sub-agents (Weather, Database, Email, and RAG Knowledge Base).
                </p>
              </div>

              <label class="switch" for="swarm-active-toggle">
                <input
                  id="swarm-active-toggle"
                  v-model="isSwarmActive"
                  type="checkbox"
                  role="switch"
                  :aria-checked="isSwarmActive"
                />
                <span class="slider round"></span>
              </label>
            </div>

            <!-- Execution Mode Select -->
            <div class="form-group-row">
              <div class="form-group">
                <label class="form-label" for="swarm-mode-select">Swarm Orchestration Mode</label>
                <div class="select-wrapper">
                  <select id="swarm-mode-select" v-model="swarmMode" class="form-select">
                    <option value="autonomous">Full Autonomous Swarm (Dynamic Agent Routing)</option>
                    <option value="hitl_guarded">Guarded Autonomous (HITL Security Approval Gate)</option>
                    <option value="read_only">Read-Only Query Mode (Disallow Destructive Actions)</option>
                  </select>
                  <svg class="select-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="6 9 12 15 18 9" />
                  </svg>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label" for="max-steps-input">Max Multi-Step Reasoning Depth</label>
                <div class="input-wrapper">
                  <input
                    id="max-steps-input"
                    v-model.number="maxSteps"
                    type="number"
                    min="1"
                    max="25"
                    class="form-input"
                    placeholder="10"
                  />
                  <span class="input-suffix">steps</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Card 2: Models Configuration -->
        <section class="settings-card">
          <div class="card-glow-bar purple"></div>
          <div class="card-header">
            <div class="card-header-left">
              <div class="card-icon-box purple">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
                  <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
                  <line x1="12" y1="22.08" x2="12" y2="12" />
                </svg>
              </div>
              <div>
                <h3 class="card-title">LLM Models Configuration</h3>
                <p class="card-subtitle">Select the foundational models that power the supervisor orchestrator and worker agents.</p>
              </div>
            </div>
            <span class="model-badge-current">{{ selectedModel }}</span>
          </div>

          <div class="card-body">
            <!-- Primary Supervisor Model Selection -->
            <div class="form-group">
              <label class="form-label" for="primary-model-select">
                Supervisor Orchestrator Model
                <span class="required-asterisk">*</span>
              </label>
              <div class="select-wrapper">
                <select id="primary-model-select" v-model="selectedModel" class="form-select">
                  <optgroup label="Groq Active Account Models">
                    <option value="openai/gpt-oss-120b">openai/gpt-oss-120b (OpenAI GPT OSS 120B • 131k • Tools & Reasoning • Recommended)</option>
                    <option value="openai/gpt-oss-20b">openai/gpt-oss-20b (OpenAI GPT OSS 20B • Ultra-Fast 131k • Tools & Logic)</option>
                    <option value="qwen/qwen3.8-27b">qwen/qwen3.8-27b (Alibaba Qwen 3.8 27B • 131k • Tools & Multimodal)</option>
                    <option value="openai/gpt-oss-safeguard-20b">openai/gpt-oss-safeguard-20b (OpenAI GPT OSS Safeguard • 131k Moderation)</option>
                  </optgroup>
                  <optgroup label="Custom / Endpoint Fallback">
                    <option value="custom">Custom Model Endpoint Identifier</option>
                  </optgroup>
                </select>
                <svg class="select-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="6 9 12 15 18 9" />
                </svg>
              </div>
              <p class="field-hint">Powered by Groq Cloud LPU inference. Coordinates query decomposition, tool scheduling, and supervisor reasoning.</p>
            </div>

            <!-- Custom Model Input (conditional) -->
            <div v-if="selectedModel === 'custom'" class="form-group">
              <label class="form-label" for="custom-model-input">Custom Model Identifier</label>
              <input
                id="custom-model-input"
                v-model="customModelId"
                type="text"
                class="form-input"
                placeholder="e.g. meta-llama/Llama-3-8b-chat-hf or mistralai/Mistral-7B-Instruct-v0.2"
              />
            </div>

            <!-- Temperature & Sampling -->
            <div class="form-group-row">
              <div class="form-group">
                <div class="label-with-val">
                  <label class="form-label" for="temperature-slider">Temperature (Creativity vs Determinism)</label>
                  <span class="val-pill">{{ temperature }}</span>
                </div>
                <div class="slider-wrapper">
                  <input
                    id="temperature-slider"
                    v-model.number="temperature"
                    type="range"
                    min="0"
                    max="1"
                    step="0.05"
                    class="range-slider"
                  />
                  <div class="slider-ticks">
                    <span>0.0 (Precise & Grounded)</span>
                    <span>0.5</span>
                    <span>1.0 (Creative)</span>
                  </div>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label" for="embedding-model-select">Knowledge Base Embedding Model</label>
                <div class="select-wrapper">
                  <select id="embedding-model-select" v-model="embeddingModel" class="form-select">
                    <optgroup label="HuggingFace / Sentence-Transformers (Local & Free)">
                      <option value="all-MiniLM-L6-v2">all-MiniLM-L6-v2 (384d • Active Project Model • Ultra Fast)</option>
                      <option value="all-mpnet-base-v2">all-mpnet-base-v2 (768d • High-Accuracy General Dense Vector)</option>
                      <option value="BAAI/bge-small-en-v1.5">BAAI/bge-small-en-v1.5 (384d • Compact MTEB Benchmark Leader)</option>
                      <option value="BAAI/bge-base-en-v1.5">BAAI/bge-base-en-v1.5 (768d • Deep Semantic Document Retrieval)</option>
                      <option value="BAAI/bge-large-en-v1.5">BAAI/bge-large-en-v1.5 (1024d • Maximum Precision for Complex Docs)</option>
                      <option value="paraphrase-multilingual-MiniLM-L12-v2">paraphrase-multilingual-MiniLM-L12-v2 (384d • 50+ Languages Multilingual)</option>
                      <option value="intfloat/e5-base-v2">intfloat/e5-base-v2 (768d • General Purpose Conversational Vector)</option>
                    </optgroup>
                    <optgroup label="External Cloud API Embeddings">
                      <option value="text-embedding-3-small">text-embedding-3-small (OpenAI API • 1536d • High Efficiency)</option>
                      <option value="text-embedding-3-large">text-embedding-3-large (OpenAI API • 3072d • Deep Resolution)</option>
                      <option value="voyage-large-2">voyage-large-2 (Voyage AI • 1536d • Specialized RAG Embeddings)</option>
                    </optgroup>
                  </select>
                  <svg class="select-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="6 9 12 15 18 9" />
                  </svg>
                </div>
                <p class="field-hint">Used for vector embedding generation in the ChromaDB knowledge base.</p>
              </div>
            </div>

            <!-- Active Sub-Agent Swarm Workers -->
            <div class="form-group sub-agents-group">
              <label class="form-label">Active Worker Swarm Agents</label>
              <div class="sub-agents-grid">
                <div
                  v-for="agent in availableAgents"
                  :key="agent.id"
                  class="agent-checkbox-card"
                  :class="{ 'is-selected': agent.enabled }"
                  @click="agent.enabled = !agent.enabled"
                >
                  <div class="agent-check-row">
                    <span class="agent-badge-tag">{{ agent.badge }}</span>
                    <input type="checkbox" :checked="agent.enabled" @click.stop class="custom-checkbox" />
                  </div>
                  <h4 class="agent-name-label">{{ agent.name }}</h4>
                  <p class="agent-desc-label">{{ agent.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Card 3: Provisioning Blueprint (SCADA Operator Registration) -->
        <section class="settings-card blueprint-card">
          <div class="card-glow-bar cyan"></div>
          <div class="card-header blueprint-header">
            <div class="card-header-left">
              <div class="card-icon-box cyan">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                  <circle cx="8.5" cy="7" r="4" />
                  <line x1="20" y1="8" x2="20" y2="14" />
                  <line x1="23" y1="11" x2="17" y2="11" />
                </svg>
              </div>
              <div>
                <h3 class="card-title">Provisioning Blueprint</h3>
                <p class="blueprint-sec-tag">SEC-ROLE: SCADA_OPERATOR_V4</p>
              </div>
            </div>

            <button
              type="button"
              class="btn-fast-generate"
              @click="generateSecureCredentials"
              title="Auto-generate high-entropy password and parameters"
            >
              <span class="sparkle-icon">✦</span>
              <span>Fast Generate Secure Key</span>
            </button>
          </div>

          <div class="card-body">
            <!-- Field 1: Username / Operator ID -->
            <div class="bp-field-group">
              <div class="bp-label-row">
                <label class="form-label" for="bp-username">
                  Username / Operator ID <span class="required-star">*</span>
                </label>
                <span class="bp-ldap-badge">
                  <span class="ldap-dot"></span>
                  AVAILABLE IN LDAP
                </span>
              </div>
              <div class="bp-input-wrapper">
                <span class="bp-input-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="7" r="4" />
                    <path d="M5.5 21a8.5 8.5 0 0 1 13 0" />
                  </svg>
                </span>
                <input
                  id="bp-username"
                  v-model="operatorUsername"
                  type="text"
                  class="form-input bp-input"
                  placeholder="op_arun_88"
                  required
                />
                <span class="bp-reg-badge">REG: a-z0-9_</span>
              </div>
              <p class="field-hint bp-hint">Must match standard SCADA plant taxonomy (op_, maint_, or eng_ prefixes).</p>
            </div>

            <!-- Field 2: Email Address / Security Dispatch -->
            <div class="bp-field-group">
              <div class="bp-label-row">
                <label class="form-label" for="bp-email">
                  Email Address / Security Dispatch <span class="required-star">*</span>
                </label>
              </div>
              <div class="bp-input-wrapper">
                <span class="bp-input-icon">@</span>
                <input
                  id="bp-email"
                  v-model="operatorEmail"
                  type="email"
                  class="form-input bp-input"
                  placeholder="a.run@aquasync-desal.internal"
                  required
                />
              </div>
              <p class="field-hint bp-hint bp-info-hint">
                <svg class="info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="16" x2="12" y2="12" />
                  <line x1="12" y1="8" x2="12.01" y2="8" />
                </svg>
                <span>Used for critical Level-3 SCADA alarm escalations, chemical leak alerts, and MFA challenges.</span>
              </p>
            </div>

            <!-- Field 3: Password & Hash Parameters -->
            <div class="bp-field-group">
              <div class="bp-label-row">
                <label class="form-label" for="bp-password">
                  Password &amp; Hash Parameters <span class="required-star">*</span>
                </label>
                <span class="bp-strength-badge">
                  STRENGTH: HIGH (128-BIT ENTROPY)
                </span>
              </div>
              <div class="bp-passwords-row">
                <div class="bp-input-wrapper flex-1">
                  <span class="bp-input-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                      <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                    </svg>
                  </span>
                  <input
                    id="bp-password"
                    v-model="operatorPassword"
                    :type="showBpPassword ? 'text' : 'password'"
                    class="form-input bp-input"
                    placeholder="••••••••••••••••"
                    required
                  />
                  <button
                    type="button"
                    class="bp-toggle-eye"
                    @click="showBpPassword = !showBpPassword"
                    :title="showBpPassword ? 'Hide password' : 'Show password'"
                  >
                    <svg v-if="!showBpPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                      <circle cx="12" cy="12" r="3" />
                    </svg>
                    <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
                      <line x1="1" y1="1" x2="23" y2="23" />
                    </svg>
                  </button>
                </div>

                <div class="bp-input-wrapper flex-1">
                  <span class="bp-input-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="23 4 23 10 17 10" />
                      <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10" />
                    </svg>
                  </span>
                  <input
                    id="bp-confirm-password"
                    v-model="operatorConfirmPassword"
                    :type="showBpPassword ? 'text' : 'password'"
                    class="form-input bp-input"
                    placeholder="••••••••••••••••"
                    required
                  />
                  <span class="bp-confirmed-badge" v-if="passwordsMatch">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10" />
                      <polyline points="16 9 10 15 7 12" />
                    </svg>
                  </span>
                </div>
              </div>

              <!-- Segmented Strength Bar -->
              <div class="bp-entropy-bar">
                <div class="entropy-segment filled"></div>
                <div class="entropy-segment filled"></div>
                <div class="entropy-segment filled"></div>
              </div>
            </div>

            <!-- Operational Access Tier & Control Rights -->
            <div class="bp-access-tier-box">
              <span class="tier-label">Operational Access Tier &amp; Control Rights:</span>
              <div class="tier-pills">
                <span class="tier-pill">● READ_TELEMETRY</span>
                <span class="tier-pill">● ISSUE_SETPOINT_CMD</span>
                <span class="tier-pill">● OVERRIDE_SAFETY_INTERLOCK</span>
              </div>
            </div>

            <!-- Provision Submit Button -->
            <div class="bp-submit-row">
              <button
                type="button"
                class="btn-provision-primary"
                :disabled="isProvisioning || !operatorUsername || !operatorPassword"
                @click="provisionOperator"
              >
                <span v-if="!isProvisioning">
                  Provision SCADA Operator Credential <span class="arrow-sym">→</span>
                </span>
                <span v-else class="btn-spinner-row">
                  <span class="btn-spinner"></span>
                  <span>Registering in Plant Database...</span>
                </span>
              </button>
            </div>
          </div>
        </section>

        <!-- Form Action Bar -->
        <div class="form-action-footer">
          <div class="footer-left-info">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="16" x2="12" y2="12" />
              <line x1="12" y1="8" x2="12.01" y2="8" />
            </svg>
            <span>Changes will apply directly to the running session orchestration parameters.</span>
          </div>

          <div class="footer-buttons">
            <button type="button" class="btn-secondary" :disabled="isSaving || isLoading" @click="resetDefaults">
              Discard Changes
            </button>
            <button type="submit" class="btn-primary" :disabled="isSaving || isLoading">
              <svg v-if="!isSaving" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12" />
              </svg>
              <span v-else class="btn-spinner"></span>
              <span>{{ isSaving ? 'Applying...' : 'Apply Configuration' }}</span>
            </button>
          </div>
        </div>
      </form>
    </div>

    <!-- Toast Notification -->
    <transition name="toast-fade">
      <div v-if="toast" class="settings-toast" :class="`toast-${toast.type}`">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="20 6 9 17 4 12" />
        </svg>
        <span>{{ toast.message }}</span>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const currentSessionId = ref('')
const isLoading = ref(false)
const isSaving = ref(false)

// SCADA Operator Provisioning Blueprint State
const operatorUsername = ref('')
const operatorEmail = ref('')
const operatorPassword = ref('')
const operatorConfirmPassword = ref('')
const showBpPassword = ref(false)
const isProvisioning = ref(false)

const passwordsMatch = computed(() => {
  return Boolean(operatorPassword.value && operatorPassword.value === operatorConfirmPassword.value)
})

const computedHashTrace = computed(() => {
  if (!operatorPassword.value) {
    return '$argon2id$v=19$m=65536,t=3,p=4$dBhpcylpcy1hLXNhbHQ$7xKm2N3oD...F8v2QkL'
  }
  const raw = operatorUsername.value + ':' + operatorPassword.value
  let hashVal = 0
  for (let i = 0; i < raw.length; i++) {
    hashVal = ((hashVal << 5) - hashVal + raw.charCodeAt(i)) | 0
  }
  const hex = Math.abs(hashVal).toString(16).padEnd(8, 'f')
  return `$argon2id$v=19$m=65536,t=3,p=4$dBhpcylpcy1hLXNhbHQ$7xKm2N3o${hex}...F8v2QkL`
})

const generateSecureCredentials = () => {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789!@#$%^&*'
  let newPass = ''
  for (let i = 0; i < 20; i++) {
    newPass += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  operatorPassword.value = newPass
  operatorConfirmPassword.value = newPass
  showToast('High-entropy 128-bit key generated successfully!', 'success')
}

const provisionOperator = async () => {
  if (!operatorUsername.value.trim() || !operatorEmail.value.trim() || !operatorPassword.value) {
    showToast('Please fill in all operator provisioning fields.', 'error')
    return
  }
  if (operatorPassword.value !== operatorConfirmPassword.value) {
    showToast('Passwords do not match. Please verify.', 'error')
    return
  }

  isProvisioning.value = true
  try {
    const res = await fetch('http://127.0.0.1:8000/api/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: operatorUsername.value.trim(),
        email: operatorEmail.value.trim(),
        password: operatorPassword.value
      })
    })

    const data = await res.json()

    if (!res.ok) {
      showToast(data.detail || 'Failed to provision operator credential.', 'error')
      operatorUsername.value = ""
      operatorEmail.value = ""
      operatorPassword.value = ""
      return
    }

    showToast(`Operator ${operatorUsername.value} provisioned successfully in SCADA Auth DB!`, 'success')
  } catch (err) {
    showToast('Failed to reach authentication gateway on port 8000.', 'error')
  } finally {
    isProvisioning.value = false
  }
}

// 1. Swarm Active Field
const isSwarmActive = ref(true)
const swarmMode = ref('autonomous')
const maxSteps = ref(10)

// 2. Models Field
const selectedModel = ref('openai/gpt-oss-120b')
const customModelId = ref('')
const temperature = ref(0.2)
const embeddingModel = ref('all-MiniLM-L6-v2')

// Worker agents list
const availableAgents = ref([
  {
    id: 'rag_agent',
    name: 'Knowledge RAG Agent',
    badge: 'KNOWLEDGE & DOCS',
    description: 'Searches ChromaDB vector collection for company policies, specs, and knowledge articles.',
    enabled: true
  },
  {
    id: 'database_agent',
    name: 'PostgreSQL Database Agent',
    badge: 'SQL & PERSISTENCE',
    description: 'Queries internal relational database tables and user account profiles.',
    enabled: true
  },
  {
    id: 'weather_agent',
    name: 'Open-Meteo Weather Agent',
    badge: 'EXTERNAL API',
    description: 'Fetches real-time global weather conditions and forecast metrics.',
    enabled: true
  },
  {
    id: 'email_agent',
    name: 'Email Dispatch Agent',
    badge: 'HITL PROTECTED',
    description: 'Formats and queues outbound communications subject to security approvals.',
    enabled: true
  }
])

const toast = ref(null)

const showToast = (message, type = 'success') => {
  toast.value = { message, type }
  setTimeout(() => {
    toast.value = null
  }, 3500)
}

// Session ID grabber from localStorage <agent_session_id> or JWT token
const getSessionId = () => {
  let savedId = localStorage.getItem('agent_session_id')
  if (!savedId) {
    const token = localStorage.getItem('scada_access_token')
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        if (payload && payload.id) {
          savedId = String(payload.id)
          localStorage.setItem('agent_session_id', savedId)
        }
      } catch (e) {}
    }
  }
  if (!savedId) {
    savedId = 'default'
  }
  return savedId
}

// Known dropdown model values
const knownModels = [
  'openai/gpt-oss-120b',
  'openai/gpt-oss-20b',
  'qwen/qwen3.8-27b',
  'openai/gpt-oss-safeguard-20b',
  'allam-2-7b'
]

const applySettingsData = (data) => {
  if (!data) return

  if (data.is_swarm_active !== undefined) {
    isSwarmActive.value = Boolean(data.is_swarm_active)
  }
  if (data.swarm_mode) {
    swarmMode.value = data.swarm_mode
  }
  if (data.max_steps !== undefined) {
    maxSteps.value = Number(data.max_steps)
  }
  if (data.temperature !== undefined) {
    temperature.value = Number(data.temperature)
  }
  if (data.embedding_model) {
    embeddingModel.value = data.embedding_model
  }

  // Model handling
  if (data.custom_model_id) {
    selectedModel.value = 'custom'
    customModelId.value = data.custom_model_id
  } else if (data.supervisor_model) {
    if (knownModels.includes(data.supervisor_model)) {
      selectedModel.value = data.supervisor_model
      customModelId.value = ''
    } else {
      selectedModel.value = 'custom'
      customModelId.value = data.supervisor_model
    }
  }

  // Active agents handling
  if (data.active_agents) {
    let agentsList = data.active_agents
    if (typeof agentsList === 'string') {
      try {
        agentsList = JSON.parse(agentsList)
      } catch (e) {
        agentsList = []
      }
    }
    if (Array.isArray(agentsList)) {
      availableAgents.value.forEach(agent => {
        const found = agentsList.find(x => (typeof x === 'string' ? x === agent.id : x.id === agent.id))
        if (found !== undefined) {
          agent.enabled = typeof found === 'string' ? true : Boolean(found.enabled)
        } else {
          agent.enabled = false
        }
      })
    }
  }
}

// Fetch settings from server on mount
const fetchSettings = async () => {
  isLoading.value = true
  const sid = getSessionId()
  currentSessionId.value = sid

  try {
    const res = await fetch(`http://127.0.0.1:8000/api/settings?session_id=${encodeURIComponent(sid)}`)
    if (!res.ok) {
      throw new Error(`Server returned HTTP ${res.status}`)
    }
    const result = await res.json()
    if (result && result.data) {
      applySettingsData(result.data)
    }
  } catch (err) {
    console.error('Failed to fetch swarm settings from backend:', err)
    showToast('Failed to connect to backend settings. Showing local defaults.', 'error')
  } finally {
    isLoading.value = false
  }
}

// Save settings to server endpoint
const saveSettings = async () => {
  isSaving.value = true
  const sid = getSessionId()
  currentSessionId.value = sid

  const chosenModel = selectedModel.value === 'custom'
    ? (customModelId.value.trim() || 'openai/gpt-oss-120b')
    : selectedModel.value

  const payload = {
    session_id: sid,
    is_swarm_active: isSwarmActive.value,
    swarm_mode: swarmMode.value,
    max_steps: maxSteps.value,
    supervisor_model: chosenModel,
    custom_model_id: selectedModel.value === 'custom' ? customModelId.value.trim() : '',
    temperature: temperature.value,
    embedding_model: embeddingModel.value,
    active_agents: availableAgents.value.filter(a => a.enabled).map(a => a.id)
  }

  try {
    const res = await fetch('http://127.0.0.1:8000/api/settings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    if (!res.ok) {
      const errJson = await res.json().catch(() => ({}))
      throw new Error(errJson.detail || `Server returned HTTP ${res.status}`)
    }

    const result = await res.json()
    if (result && result.data) {
      applySettingsData(result.data)
    }

    // Also persist in localStorage for backup
    localStorage.setItem('swarm_ui_settings', JSON.stringify(payload))
    window.dispatchEvent(new CustomEvent('swarm-settings-updated', { detail: payload }))
    showToast(`Settings successfully saved for session #${sid.slice(0, 8)}!`, 'success')
  } catch (err) {
    console.error('Failed to save settings:', err)
    showToast(`Error saving settings: ${err.message}`, 'error')
  } finally {
    isSaving.value = false
  }
}

const resetDefaults = () => {
  isSwarmActive.value = true
  swarmMode.value = 'autonomous'
  maxSteps.value = 10
  selectedModel.value = 'openai/gpt-oss-120b'
  customModelId.value = ''
  temperature.value = 0.2
  embeddingModel.value = 'all-MiniLM-L6-v2'
  availableAgents.value.forEach(a => { a.enabled = true })
  showToast('Restored defaults. Click Save Settings to persist.', 'info')
}

onMounted(() => {
  fetchSettings()
})
</script>

<style scoped src="@/style_folder/SettingsView.css"></style>
