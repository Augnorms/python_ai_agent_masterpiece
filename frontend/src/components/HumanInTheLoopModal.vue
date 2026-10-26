<template>
  <div v-if="isOpen" class="hitl-backdrop" @click.self="onClose">
    <div class="hitl-card">
      <!-- Top Glowing Border Gradient -->
      <div class="card-glow-bar"></div>

      <!-- Header -->
      <div class="hitl-header">
        <div class="header-left">
          <div class="shield-icon-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
            </svg>
          </div>
          <div class="header-titles">
            <div class="title-row">
              <h3 class="main-title">Human-in-the-Loop Review Gate</h3>
              <span class="gate-tag">#HITL-104</span>
            </div>
            <p class="subtitle">
              Step #{{ stepNumber }} of Autonomous Incident Triage Session #{{ sessionId ? sessionId.slice(0, 4) : '4092' }}
            </p>
          </div>
        </div>

        <button class="close-btn" @click="onClose" title="Close">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>

      <!-- Risk Level & Target Bar -->
      <div class="risk-target-row">
        <div class="risk-badge">
          <span class="risk-dot"></span>
          HIGH RISK — {{ riskLabel }}
        </div>
        <div class="target-info">
          <span class="target-label">Target:</span>
          <span class="target-value">{{ targetHost }}</span>
        </div>
      </div>

      <!-- Description Context -->
      <p class="context-desc">
        Supervisor Agent requests elevated authorization to dispatch a high-privilege execution script. 
        You may approve execution immediately, modify the instructions with injected prompt guidance, or abort the entire sequence.
      </p>

      <!-- Payload Preview & Verification Card -->
      <div class="payload-box">
        <div class="payload-header">
          <div class="payload-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="4 17 10 11 4 5" />
              <line x1="12" y1="19" x2="20" y2="19" />
            </svg>
            <span>Payload Preview & Verification</span>
          </div>
          <span class="simulation-status">
            <span class="sim-dot"></span>
            Dry-run Simulation Passed
          </span>
        </div>

        <div class="code-editor-view">
          <pre class="code-content"><code>{{ formattedPayload }}</code></pre>
        </div>
      </div>

      <!-- Modify & Inject Steering Prompt Input -->
      <div class="steering-section">
        <label class="steering-label">MODIFY & INJECT STEERING PROMPT (OPTIONAL)</label>
        <div class="steering-input-group">
          <input
            v-model="steeringPrompt"
            type="text"
            placeholder="e.g. 'Omit the CASCADE drop and only run reindex concurrently...'"
            @keyup.enter="handleInject"
          />
          <button class="inject-btn" @click="handleInject" :disabled="!steeringPrompt.trim()">
            Inject Correction
          </button>
        </div>
      </div>

      <!-- Footer Actions -->
      <div class="hitl-footer">
        <button class="btn-reject" @click="handleReject">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10" />
            <line x1="15" y1="9" x2="9" y2="15" />
            <line x1="9" y1="9" x2="15" y2="15" />
          </svg>
          Reject & Abort Flow
        </button>

        <div class="footer-right-actions">
          <button class="btn-minimize" @click="onClose">
            Minimize
          </button>
          <button class="btn-approve" @click="handleApprove">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="20 6 9 17 4 12" />
            </svg>
            Approve & Execute
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: true
  },
  payload: {
    type: [String, Object],
    default: ''
  },
  sessionId: {
    type: String,
    default: '4092'
  },
  stepNumber: {
    type: [Number, String],
    default: 5
  },
  riskType: {
    type: String,
    default: 'SCHEMA MUTATION'
  },
  target: {
    type: String,
    default: 'db.prod.replica-02 (PostgreSQL 16.2)'
  }
})

const emit = defineEmits(['approve', 'reject', 'close', 'inject'])

const steeringPrompt = ref('')

const riskLabel = computed(() => {
  if (typeof props.payload === 'string') {
    if (props.payload.includes('delete_user')) return 'DATA DELETION (RESTRICTED)'
    if (props.payload.includes('send_email')) return 'EXTERNAL DISPATCH (RESTRICTED)'
  }
  return props.riskType
})

const targetHost = computed(() => {
  if (typeof props.payload === 'string' && props.payload.includes('delete_user')) {
    return 'agent_memory.db (SQLite / Users Table)'
  }
  if (typeof props.payload === 'string' && props.payload.includes('send_email')) {
    return 'smtp.relay.service / sent_emails.log'
  }
  return props.target
})

const formattedPayload = computed(() => {
  if (!props.payload) {
    return `-- Confirmed target PID from Task #2 telemetry:\nSELECT pg_terminate_backend(4819);\n\n-- Warning: cascading metadata eviction\nDROP TABLE IF EXISTS audit_staging CASCADE;\nREINDEX TABLE CONCURRENTLY orders_v2;`
  }

  if (typeof props.payload === 'object') {
    return JSON.stringify(props.payload, null, 2)
  }

  // If it's a string, format cleanly
  if (props.payload.includes('Tool:')) {
    return `-- Elevated Action Intercepted by HITL Gate:\n${props.payload}\n\n-- Pre-execution verification status: READY FOR AUTHORIZATION`
  }

  return props.payload
})

const handleApprove = () => {
  emit('approve', { approved: true, steering: steeringPrompt.value })
  steeringPrompt.value = ''
}

const handleReject = () => {
  emit('reject', { approved: false, steering: steeringPrompt.value })
  steeringPrompt.value = ''
}

const handleInject = () => {
  if (steeringPrompt.value.trim()) {
    emit('inject', steeringPrompt.value.trim())
  }
}

const onClose = () => {
  emit('close')
}
</script>

<style scoped>
.hitl-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(3, 7, 18, 0.75);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 16px;
  animation: fadeIn 0.15s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.98); }
  to { opacity: 1; transform: scale(1); }
}

.hitl-card {
  width: 600px;
  max-width: 95vw;
  background: #0b1120;
  border: 1px solid rgba(147, 51, 234, 0.35);
  border-radius: 14px;
  box-shadow: 0 0 40px rgba(147, 51, 234, 0.25), 0 20px 30px rgba(0, 0, 0, 0.6);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* Glowing Top Accent Bar */
.card-glow-bar {
  height: 3px;
  width: 100%;
  background: linear-gradient(90deg, #a855f7 0%, #00e5ff 100%);
  box-shadow: 0 0 12px #a855f7;
}

/* Header */
.hitl-header {
  padding: 18px 22px 14px 22px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.shield-icon-box {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(147, 51, 234, 0.18);
  border: 1px solid rgba(168, 85, 247, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #c084fc;
  box-shadow: 0 0 15px rgba(168, 85, 247, 0.3);
}

.shield-icon-box svg {
  width: 20px;
  height: 20px;
}

.header-titles {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.main-title {
  font-size: 15px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.2px;
}

.gate-tag {
  color: #c084fc;
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
}

.subtitle {
  font-size: 11px;
  color: #94a3b8;
  font-family: var(--font-mono);
}

.close-btn {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  width: 28px;
  height: 28px;
  color: #94a3b8;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.close-btn svg {
  width: 14px;
  height: 14px;
}

/* Risk & Target Row */
.risk-target-row {
  padding: 0 22px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 4px;
}

.risk-badge {
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid rgba(239, 68, 68, 0.35);
  border-radius: 4px;
  padding: 3px 8px;
  color: #f87171;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.risk-dot {
  width: 5px;
  height: 5px;
  background: #ef4444;
  border-radius: 50%;
  box-shadow: 0 0 6px #ef4444;
}

.target-info {
  font-size: 11px;
  font-family: var(--font-mono);
}

.target-label {
  color: #64748b;
  margin-right: 4px;
}

.target-value {
  color: #38bdf8;
  font-weight: 500;
}

/* Context Description */
.context-desc {
  padding: 12px 22px 0 22px;
  font-size: 11.5px;
  color: #94a3b8;
  line-height: 1.5;
}

/* Payload Box */
.payload-box {
  margin: 14px 22px 0 22px;
  background: #060913;
  border: 1px solid #1e293b;
  border-radius: 8px;
  overflow: hidden;
}

.payload-header {
  padding: 8px 12px;
  background: rgba(15, 23, 42, 0.6);
  border-bottom: 1px solid #1e293b;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.payload-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  font-weight: 600;
  color: #94a3b8;
  letter-spacing: 0.3px;
}

.payload-title svg {
  width: 12px;
  height: 12px;
  color: #38bdf8;
}

.simulation-status {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #34d399;
  font-size: 10px;
  font-weight: 600;
}

.sim-dot {
  width: 5px;
  height: 5px;
  background: #10b981;
  border-radius: 50%;
  box-shadow: 0 0 6px #10b981;
}

.code-editor-view {
  padding: 12px;
  max-height: 160px;
  overflow-y: auto;
}

.code-content {
  margin: 0;
  font-family: var(--font-mono);
  font-size: 11px;
  line-height: 1.5;
  color: #cbd5e1;
  white-space: pre-wrap;
}

/* Steering Section */
.steering-section {
  padding: 14px 22px 0 22px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.steering-label {
  font-size: 9.5px;
  font-weight: 700;
  color: #64748b;
  letter-spacing: 0.8px;
}

.steering-input-group {
  display: flex;
  gap: 8px;
}

.steering-input-group input {
  flex: 1;
  background: #060913;
  border: 1px solid #1e293b;
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 11.5px;
  color: #fff;
  outline: none;
  transition: all 0.2s;
}

.steering-input-group input:focus {
  border-color: #00e5ff;
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.2);
}

.inject-btn {
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid #334155;
  border-radius: 6px;
  color: #e2e8f0;
  font-size: 11px;
  font-weight: 600;
  padding: 0 14px;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.inject-btn:hover:not(:disabled) {
  background: rgba(147, 51, 234, 0.25);
  border-color: #a855f7;
  color: #fff;
}

.inject-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Footer Actions */
.hitl-footer {
  margin-top: 18px;
  padding: 14px 22px;
  background: rgba(6, 10, 20, 0.9);
  border-top: 1px solid rgba(23, 36, 60, 0.8);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.btn-reject {
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 6px;
  color: #f87171;
  font-size: 12px;
  font-weight: 700;
  padding: 8px 16px;
  display: flex;
  align-items: center;
  gap: 7px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-reject:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: #ef4444;
}

.btn-reject svg {
  width: 14px;
  height: 14px;
}

.footer-right-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-minimize {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid #334155;
  border-radius: 6px;
  color: #94a3b8;
  font-size: 12px;
  font-weight: 600;
  padding: 8px 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-minimize:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
}

.btn-approve {
  background: #34d399;
  border: none;
  border-radius: 6px;
  color: #060a14;
  font-size: 12px;
  font-weight: 700;
  padding: 8px 18px;
  display: flex;
  align-items: center;
  gap: 7px;
  cursor: pointer;
  box-shadow: 0 0 16px rgba(52, 211, 153, 0.4);
  transition: all 0.2s;
}

.btn-approve:hover {
  background: #10b981;
  transform: translateY(-1px);
}

.btn-approve svg {
  width: 15px;
  height: 15px;
}
</style>
