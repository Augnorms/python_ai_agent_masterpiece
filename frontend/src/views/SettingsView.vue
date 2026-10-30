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
                  When enabled, the orchestrator routes tasks across specialized sub-agents (Math, Weather, Database, Email, and RAG Knowledge Base).
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
import { ref, onMounted } from 'vue'

const currentSessionId = ref('')
const isLoading = ref(false)
const isSaving = ref(false)

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
    id: 'math_agent',
    name: 'Math Calculator Agent',
    badge: 'ARITHMETIC & LOGIC',
    description: 'Executes deterministic calculation operations and prevents LLM hallucination.',
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

// Session ID grabber from localStorage <agent_session_id>
const getSessionId = () => {
  let savedId = localStorage.getItem('agent_session_id')
  if (!savedId) {
    savedId = crypto.randomUUID()
    localStorage.setItem('agent_session_id', savedId)
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

<style scoped>
.settings-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  background: var(--bg-app);
  overflow: hidden;
  position: relative;
}

/* Header */
.settings-header {
  padding: 16px 24px;
  background: rgba(10, 16, 29, 0.6);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
  gap: 16px;
}

.settings-title-row {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.title-with-badge {
  display: flex;
  align-items: center;
  gap: 10px;
}

.settings-tag {
  font-size: 9.5px;
  font-weight: 700;
  padding: 2px 7px;
  background: rgba(0, 229, 255, 0.12);
  color: var(--primary-cyan);
  border: 1px solid rgba(0, 229, 255, 0.3);
  border-radius: 4px;
  letter-spacing: 0.6px;
}

.settings-title {
  font-size: 17px;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.2px;
  margin: 0;
}

.settings-desc {
  font-size: 11.5px;
  color: var(--text-muted);
  margin: 0;
  max-width: 720px;
  line-height: 1.45;
}

.settings-header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* Buttons */
.btn-secondary {
  background: rgba(13, 21, 39, 0.8);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-main);
  padding: 7px 14px;
  font-size: 11.5px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(0, 229, 255, 0.3);
}
.btn-secondary svg {
  width: 13px;
  height: 13px;
  color: var(--text-muted);
}

.btn-primary {
  background: #00e5ff;
  border: none;
  border-radius: 6px;
  color: #060a14;
  padding: 7px 16px;
  font-size: 11.5px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  box-shadow: 0 0 12px rgba(0, 229, 255, 0.3);
  transition: all 0.2s;
}
.btn-primary:hover {
  background: #38bdf8;
  transform: translateY(-1px);
}
.btn-primary svg {
  width: 14px;
  height: 14px;
}

/* Content */
.settings-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px 32px 48px 32px;
}

.settings-form {
  max-width: 980px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Cards */
.settings-card {
  background: rgba(13, 21, 39, 0.6);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}

.card-glow-bar {
  height: 2px;
  width: 100%;
}
.card-glow-bar.cyan {
  background: linear-gradient(90deg, #00e5ff 0%, #9d72ff 100%);
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.5);
}
.card-glow-bar.purple {
  background: linear-gradient(90deg, #9d72ff 0%, #00e5ff 100%);
  box-shadow: 0 0 10px rgba(157, 114, 255, 0.5);
}

.card-header {
  padding: 16px 22px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-color);
  background: rgba(10, 16, 31, 0.4);
}

.card-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.card-icon-box {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.card-icon-box svg {
  width: 18px;
  height: 18px;
}
.card-icon-box.cyan {
  background: rgba(0, 229, 255, 0.1);
  color: var(--primary-cyan);
  border: 1px solid rgba(0, 229, 255, 0.3);
}
.card-icon-box.purple {
  background: rgba(157, 114, 255, 0.1);
  color: var(--primary-purple);
  border: 1px solid rgba(157, 114, 255, 0.3);
}

.card-title {
  font-size: 14.5px;
  font-weight: 700;
  color: #fff;
  margin: 0;
}

.card-subtitle {
  font-size: 11.5px;
  color: var(--text-muted);
  margin: 2px 0 0 0;
}

.swarm-status-badge {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.5px;
}
.swarm-status-badge.status-active {
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.35);
  color: #34d399;
}
.swarm-status-badge.status-inactive {
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.35);
  color: #f87171;
}

.status-pulse-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background-color: currentColor;
  box-shadow: 0 0 8px currentColor;
  animation: pulse-dot 1.8s infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.85); }
}

.model-badge-current {
  font-size: 11px;
  font-family: var(--font-mono);
  color: var(--primary-purple);
  background: rgba(157, 114, 255, 0.12);
  border: 1px solid rgba(157, 114, 255, 0.3);
  padding: 3px 9px;
  border-radius: 6px;
  font-weight: 600;
}

.card-body {
  padding: 22px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

/* Toggle Row */
.form-toggle-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(10, 16, 31, 0.5);
  border: 1px solid var(--border-color);
  padding: 16px 18px;
  border-radius: 8px;
}

.toggle-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.toggle-title {
  font-size: 13px;
  font-weight: 600;
  color: #fff;
  cursor: pointer;
}

.toggle-desc {
  font-size: 11px;
  color: var(--text-muted);
  margin: 0;
  max-width: 650px;
}

/* Switch UI */
.switch {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 26px;
  flex-shrink: 0;
}
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}
.slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: #1a2538;
  border: 1px solid #334155;
  transition: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: #94a3b8;
  transition: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
input:checked + .slider {
  background-color: rgba(0, 229, 255, 0.25);
  border-color: #00e5ff;
}
input:checked + .slider:before {
  transform: translateX(22px);
  background-color: #00e5ff;
  box-shadow: 0 0 10px #00e5ff;
}
.slider.round {
  border-radius: 26px;
}
.slider.round:before {
  border-radius: 50%;
}

/* Form Groups & Inputs */
.form-group-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.form-label {
  font-size: 11.5px;
  font-weight: 600;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 4px;
}

.required-asterisk {
  color: #ef4444;
}

.field-hint {
  font-size: 10.5px;
  color: var(--text-dim);
  margin: 2px 0 0 0;
}

.select-wrapper {
  position: relative;
  width: 100%;
}

.form-select,
.form-input {
  width: 100%;
  background: var(--bg-card-inner, #0a101f);
  border: 1px solid var(--border-color, #17243c);
  border-radius: 7px;
  color: var(--text-main, #ffffff);
  font-size: 12px;
  padding: 9px 12px;
  outline: none;
  font-family: inherit;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-select {
  appearance: none;
  padding-right: 32px;
  cursor: pointer;
}

.select-arrow {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 14px;
  height: 14px;
  color: var(--text-dim);
  pointer-events: none;
}

.form-select:focus,
.form-input:focus {
  border-color: var(--primary-cyan, #00e5ff);
  box-shadow: 0 0 0 2px rgba(0, 229, 255, 0.15);
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}
.input-suffix {
  position: absolute;
  right: 12px;
  font-size: 11px;
  color: var(--text-dim);
  font-family: var(--font-mono);
  pointer-events: none;
}

/* Slider */
.label-with-val {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.val-pill {
  font-size: 10.5px;
  font-family: var(--font-mono);
  color: var(--primary-cyan);
  background: rgba(0, 229, 255, 0.12);
  padding: 1px 7px;
  border-radius: 4px;
  font-weight: 700;
}
.slider-wrapper {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-top: 4px;
}
.range-slider {
  width: 100%;
  accent-color: #00e5ff;
  cursor: pointer;
}
.slider-ticks {
  display: flex;
  justify-content: space-between;
  font-size: 9.5px;
  color: var(--text-dim);
  font-family: var(--font-mono);
}

/* Sub-agents Grid */
.sub-agents-group {
  margin-top: 6px;
}
.sub-agents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 12px;
}

.agent-checkbox-card {
  background: rgba(10, 16, 31, 0.5);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  cursor: pointer;
  transition: all 0.2s;
}
.agent-checkbox-card:hover {
  background: rgba(255, 255, 255, 0.02);
  border-color: rgba(0, 229, 255, 0.3);
}
.agent-checkbox-card.is-selected {
  border-color: rgba(0, 229, 255, 0.45);
  background: rgba(0, 229, 255, 0.04);
}

.agent-check-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.agent-badge-tag {
  font-size: 9px;
  font-weight: 700;
  color: var(--text-dim);
  letter-spacing: 0.5px;
}
.is-selected .agent-badge-tag {
  color: var(--primary-cyan);
}

.agent-name-label {
  font-size: 12.5px;
  font-weight: 600;
  color: #fff;
  margin: 0;
}

.agent-desc-label {
  font-size: 11px;
  color: var(--text-muted);
  line-height: 1.4;
  margin: 0;
}

.custom-checkbox {
  accent-color: #00e5ff;
  width: 14px;
  height: 14px;
  cursor: pointer;
}

/* Action Footer */
.form-action-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: rgba(13, 21, 39, 0.6);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  margin-top: 4px;
}

.footer-left-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11.5px;
  color: var(--text-muted);
}
.footer-left-info svg {
  width: 15px;
  height: 15px;
  color: var(--primary-cyan);
  flex-shrink: 0;
}

.footer-buttons {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* Toast */
.settings-toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background: #0d1527;
  border: 1px solid rgba(0, 229, 255, 0.4);
  color: #ffffff;
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 16px rgba(0, 229, 255, 0.2);
  z-index: 2500;
}
.settings-toast svg {
  width: 15px;
  height: 15px;
  color: #00e5ff;
}

.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: all 0.2s ease-out;
}
.toast-fade-enter-from,
.toast-fade-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

@media (max-width: 768px) {
  .form-group-row {
    grid-template-columns: 1fr;
  }
  .form-action-footer {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
}

.session-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 10px;
  font-weight: 700;
  font-family: var(--font-mono, monospace);
  padding: 2px 8px;
  background: rgba(168, 85, 247, 0.12);
  color: #c084fc;
  border: 1px solid rgba(168, 85, 247, 0.3);
  border-radius: 4px;
  letter-spacing: 0.5px;
}

.session-icon {
  width: 12px;
  height: 12px;
}

.btn-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  display: inline-block;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

</style>
