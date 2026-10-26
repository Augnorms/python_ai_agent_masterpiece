<template>
  <div class="cockpit-container">
    <!-- Cockpit Sub-Header -->
    <div class="cockpit-header">
      <div class="cockpit-title-row">
        <div class="title-with-status">
          <span class="pulse-indicator"></span>
          <h2 class="cockpit-title">Agent Orchestrator & Tool Execution Cockpit</h2>
        </div>
        <div class="session-info">
          <span class="session-label">Session #{{ sessionId.slice(0, 8) }}: Conversational Multi-Tool Synthesis (Multi-Agent Swarm)</span>
        </div>
      </div>

      <div class="cockpit-controls">
        <div class="control-pill latency-pill">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
          </svg>
          <span>
            {{ latency > 0 ? `${latency}ms latency` : '00 ms latency' }} 
            <span :class="successRate === 100 ? 'dim-success' : 'dim-error'">
              ({{ successRate }} % success)
            </span>
          </span>
        </div>

        <div class="control-pill security-pill">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
            <path d="M7 11V7a5 5 0 0 1 10 0v4" />
          </svg>
          <span>HITL Security Gate</span>
        </div>

        <button @click="clearMemory" class="control-btn clear-btn" :disabled="isClearingMemory" title="Clear conversation memory & session history">
          <svg :class="{ 'spinning': isClearingMemory }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="1 4 1 10 7 10" />
            <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10" />
          </svg>
          <span>{{ isClearingMemory ? 'Clearing...' : 'Clear Memory' }}</span>
        </button>
      </div>
    </div>

    <!-- 2-Column Split Workspace -->
    <div class="cockpit-workspace">
      <!-- Left Column: Task Execution & Lifecycle -->
      <section class="lifecycle-panel">
        <div class="panel-header">
          <div class="panel-title-group">
            <h3 class="panel-title">Task Execution & Lifecycle</h3>
            <span class="task-count-badge">{{ taskLifecycle.length }}/{{ taskLifecycle.length }} Active & Done</span>
          </div>
          <span class="swarm-health-tag">● Swarm Healthy</span>
        </div>
        <p class="panel-subtitle">Continuous real-time sub-task execution pipeline</p>

        <!-- Pipeline Task Cards -->
        <div class="task-cards-list">
          <div v-for="(task, idx) in taskLifecycle" :key="idx" class="task-card">
            <div class="task-card-top">
              <div class="task-id-badge">
                <span class="task-id">#TASK-0{{ idx + 1 }}</span>
                <span class="task-status">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <polyline points="20 6 9 17 4 12" />
                  </svg>
                  Completed
                </span>
                <span class="task-timing">{{ task.duration }}</span>
              </div>
              <span class="task-output-badge" :title="'Output: ' + task.outputPreview">
                {{ formatBadgeOutput(task.outputPreview) }}
              </span>
            </div>

            <div class="task-card-body">
              <h4 class="task-name">{{ task.name }}</h4>
              <p class="task-desc">{{ task.description }}</p>
              
              <!-- Dedicated Output Box for Detailed/Long Results -->
              <div v-if="task.outputPreview && task.outputPreview !== 'Pending' && task.outputPreview.length > 22" class="task-output-box">
                <span class="output-box-label">Output:</span>
                <span class="output-box-content">{{ task.outputPreview }}</span>
              </div>
            </div>

            <div class="task-card-footer">
              <span class="tool-tag">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
                  <line x1="8" y1="21" x2="16" y2="21" />
                  <line x1="12" y1="17" x2="12" y2="21" />
                </svg>
                {{ task.tool }}
              </span>
              <span class="exit-code">EXIT CODE: 0</span>
            </div>
          </div>
        </div>

        <!-- Execution Timeline Sparkline -->
        <div class="timeline-footer">
          <div class="timeline-meta">
            <span class="meta-label">Execution Timeline & Health</span>
            <span class="meta-val">Avg: 0.16s / task</span>
          </div>
          <div class="sparkline-wrapper">
            <svg class="sparkline" viewBox="0 0 300 24" fill="none">
              <path d="M0 16 Q 40 8, 80 14 T 160 12 T 240 6 T 300 12" stroke="#00e5ff" stroke-width="1.8" />
            </svg>
          </div>
        </div>
      </section>

      <!-- Right Column: Orchestration Stream & Chat -->
      <section class="stream-panel">
        <div class="panel-header">
          <div class="panel-title-group">
            <span class="stream-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="4 17 10 11 4 5" />
                <line x1="12" y1="19" x2="20" y2="19" />
              </svg>
            </span>
            <h3 class="panel-title">Orchestration Stream</h3>
          </div>
          <div class="stream-tags">
            <span class="reasoning-tag">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" />
                <path d="M12 16v-4M12 8h.01" />
              </svg>
              Reasoning Enabled
            </span>
            <span class="agent-connected-tag">● Agent Connected • Ready</span>
          </div>
        </div>

        <!-- Messages Chat Box -->
        <div class="stream-chat-box" ref="chatBoxRef">
          <div v-for="(msg, index) in messages" :key="index" :class="['chat-turn', msg.role]">
            <!-- Turn Tag -->
            <div class="turn-header">
              <span class="turn-number">TURN {{ index + 1 }}</span>
              <span class="turn-time">{{ msg.time || '12:41:02 PM' }}</span>
            </div>

            <!-- User Bubble -->
            <div v-if="msg.role === 'user'" class="user-bubble-card">
              <div class="user-avatar-small">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
              </div>
              <div class="user-content">
                <span class="author-tag">User (You)</span>
                <p class="user-text">{{ msg.text }}</p>
              </div>
            </div>

            <!-- Agent / Orchestrator Card -->
            <div v-else class="agent-bubble-card">
              <div class="agent-card-header">
                <div class="agent-meta">
                  <div class="agent-logo-pill">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="3" fill="#00e5ff" stroke="none" />
                      <circle cx="5" cy="8" r="2" fill="#00e5ff" stroke="none" />
                      <circle cx="19" cy="8" r="2" fill="#00e5ff" stroke="none" />
                      <circle cx="7" cy="19" r="2" fill="#00e5ff" stroke="none" />
                      <circle cx="17" cy="19" r="2" fill="#00e5ff" stroke="none" />
                      <path d="M12 12L5 8M12 12L19 8M12 12L7 19M12 12L17 19" stroke="#00e5ff" stroke-width="1.8" />
                    </svg>
                  </div>
                  <span class="agent-name">SwarmFlow Orchestrator</span>
                </div>
                <span class="agent-status-tag">● Success</span>
              </div>

              <div class="agent-card-body">
                <!-- Raw Thought / Reasoning Section -->
                <div v-if="getThoughts(msg.text)" class="thought-section">
                  <div class="thought-header">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10" />
                      <path d="M12 16v-4M12 8h.01" />
                    </svg>
                    <span>Agent Thought</span>
                  </div>
                  <div class="thought-content">
                    <p>{{ getThoughts(msg.text) }}</p>
                  </div>
                </div>

                <!-- Tool Executions Chips -->
                <div v-if="getToolCalls(msg.text).length" class="tool-calls-chips">
                  <div v-for="(tc, tidx) in getToolCalls(msg.text)" :key="tidx" class="tool-chip">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
                      <line x1="8" y1="21" x2="16" y2="21" />
                      <line x1="12" y1="17" x2="12" y2="21" />
                    </svg>
                    <span class="chip-label">Tool:</span>
                    <span class="chip-val">{{ tc }}</span>
                  </div>
                </div>

                <!-- Final Answer Banner -->
                <div class="final-answer-box">
                  <div class="answer-header">FINAL ANSWER</div>
                  <div class="answer-text">{{ getFinalAnswer(msg.text) }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Cockpit Input Form Bar -->
        <div class="stream-input-container">
          <form @submit.prevent="sendMessage" class="cockpit-form">
            <div class="input-wrapper">
              <svg class="search-input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="4 17 10 11 4 5" />
                <line x1="12" y1="19" x2="20" y2="19" />
              </svg>
              <input
                v-model="userInput"
                type="text"
                placeholder="Ask agent or orchestrate tools"
                :disabled="isLoading"
                required
              />
            </div>

            <div class="form-bottom-row">
              <div class="tools-info-pills">
                <span class="pill-item">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" />
                  </svg>
                  Tools: Math, Weather, DB, Email, RAG
                </span>
                <span class="pill-item">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10" />
                    <line x1="12" y1="8" x2="12" y2="12" />
                    <line x1="12" y1="16" x2="12.01" y2="16" />
                  </svg>
                  Model: Qwen 2.5 / DeepSeek
                </span>
              </div>

              <div class="form-actions">
                <span class="shortcut-hint">Press ↵ Enter to execute</span>
                <button type="submit" class="send-btn" :disabled="isLoading">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polygon points="5 3 19 12 5 21 5 3" />
                  </svg>
                  <span>{{ isLoading ? 'Executing...' : 'Send Query' }}</span>
                </button>
              </div>
            </div>
          </form>
        </div>
      </section>
    </div>

    <!-- Human In The Loop (HITL) Review Gate Modal Component -->
    <HumanInTheLoopModal
      :is-open="!!pendingApproval"
      :payload="pendingApproval"
      :session-id="sessionId"
      @approve="handleApproval(true)"
      @reject="handleApproval(false)"
      @close="pendingApproval = null"
      @inject="handleInjectPrompt"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import HumanInTheLoopModal from '../components/HumanInTheLoopModal.vue'

const userInput = ref('')
const messages = ref([])
const isLoading = ref(false)
const isClearingMemory = ref(false)
const sessionId = ref(crypto.randomUUID())
const pendingApproval = ref(null)
const chatBoxRef = ref(null)
const taskLifecycle = ref([])
const latency = ref(0)
const successRate = ref(100)

const scrollToBottom = async () => {
  await nextTick()
  if (chatBoxRef.value) {
    chatBoxRef.value.scrollTop = chatBoxRef.value.scrollHeight
  }
}

onMounted(async () => {
  let savedSessionId = localStorage.getItem('agent_session_id')
  if (!savedSessionId) {
    savedSessionId = crypto.randomUUID()
    localStorage.setItem('agent_session_id', savedSessionId)
  }
  sessionId.value = savedSessionId

  try {
    const res = await fetch(`http://127.0.0.1:8000/api/history?session_id=${savedSessionId}`)
    if (res.ok) {
      const data = await res.json()
      if (data.messages && data.messages.length > 0) {
        messages.value = data.messages
      }
      scrollToBottom()
    }
  } catch (err) {
    console.error('Failed to load history:', err)
  }
})

const clearMemory = async () => {
  if (isClearingMemory.value) return
  isClearingMemory.value = true

  const prevSessionId = sessionId.value
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/memory/${prevSessionId}`, {
      method: 'DELETE'
    })
    if (!res.ok) {
      console.warn(`Memory clear returned status ${res.status}`)
    }
  } catch (err) {
    console.error('Failed to clear memory on backend:', err)
  } finally {
    const newId = crypto.randomUUID()
    localStorage.setItem('agent_session_id', newId)
    sessionId.value = newId
    messages.value = []
    taskLifecycle.value = []
    isClearingMemory.value = false
  }
}

const handleApproval = async (isApproved) => {
  try {
    await fetch('http://127.0.0.1:8000/api/approve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId.value,
        approved: isApproved
      })
    })
  } catch (err) {
    console.error('Failed to send approval:', err)
  } finally {
    pendingApproval.value = null
  }
}

const handleInjectPrompt = (steeringText) => {
  userInput.value = steeringText
  handleApproval(false)
  sendMessage()
}

const getThoughts = (text) => {
  if (!text) return ''
  const match = text.match(/Thought:\s*([\s\S]*?)(?=(Final Answer:|\[Final Answer\]|\[step|$))/i)
  return match ? match[1].trim() : ''
}

const getToolCalls = (text) => {
  if (!text) return []
  const calls = []
  const lines = text.split('\n')
  for (const line of lines) {
    if (line.includes('calling') || line.includes('Tool:')) {
      calls.push(line.replace(/\[.*?\]/g, '').replace('calling', '').trim())
    }
  }
  return calls.slice(0, 3)
}

const getFinalAnswer = (text) => {
  if (!text) return text
  if (text.includes('[Final Answer]')) {
    return text.split('[Final Answer]')[1].trim()
  }
  if (text.includes('Final Answer:')) {
    return text.split('Final Answer:')[1].trim()
  }
  return text.trim()
}

const formatBadgeOutput = (output) => {
  if (!output || output === 'Pending') return 'Pending'
  if (output.length <= 20) return `Output: ${output}`
  return `Output: ${output.slice(0, 16)}...`
}

const sendMessage = async () => {
  if (!userInput.value.trim()) return

  const prompt = userInput.value
  const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  messages.value.push({ role: 'user', text: prompt, time: now })
  userInput.value = ''
  isLoading.value = true

  const agentMsgIndex = messages.value.push({ role: 'agent', text: '', time: now }) - 1
  scrollToBottom()

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/chat?prompt=${encodeURIComponent(prompt)}&session_id=${sessionId.value}`)
    if (!response.body) throw new Error('ReadableStream not supported')

    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')

    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const parts = buffer.split('\n\n')
      buffer = parts.pop() || ''

      for (const part of parts) {
        const trimmed = part.trim()
        if (trimmed.startsWith('data: ')) {
          const raw = trimmed.slice(6)
          let payload = raw
          
          try {
            payload = JSON.parse(raw)
          } catch {
             // fallback for raw strings
          }

          // 1. Handle structured Task Events (Left Panel)
          if (payload && payload.type === "task_event") {
            const taskData = payload.data;
            const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

            // If it's a "running" event, push a new card
            if (taskData.status === "running") {
              taskLifecycle.value.push({
                name: `Executing ${taskData.tool}`,
                description: `Args: ${JSON.stringify(taskData.args)}`,
                duration: 'Running...',
                outputPreview: 'Pending',
                tool: taskData.tool,
                time: now
              })
            }
            // If it's a "completed" event, update the last card
            else if (taskData.status === "completed") {
              // Find the most recent task with this tool name and update it
              const taskIndex = taskLifecycle.value.findLastIndex(t => t.tool === taskData.tool && t.outputPreview === 'Pending')
              if (taskIndex !== -1) {
                taskLifecycle.value[taskIndex].outputPreview = taskData.result
                taskLifecycle.value[taskIndex].duration = '0.15s'
              }
            }
          } 
          
          // 2. Handle normal chat text (Right Panel)
          else if (payload && payload.type === "text") {
            const textData = payload.data || ''
            if (typeof textData === 'string' && textData.startsWith('[WAITING_FOR_APPROVAL]')) {
              pendingApproval.value = textData.replace('[WAITING_FOR_APPROVAL]', '').trim()
            }
            messages.value[agentMsgIndex].text += textData + '\n'
          }
          
          // 3. Fallback for old string messages
          else if (typeof payload === 'string') {
             if (payload.startsWith('[WAITING_FOR_APPROVAL]')) {
                pendingApproval.value = payload.replace('[WAITING_FOR_APPROVAL]', '').trim()
             }
             messages.value[agentMsgIndex].text += payload + '\n'
          }

          // 3. Handle Metrics (Top right pill)
          else if (payload && payload.type === "metrics") {
            latency.value = payload.data.latency_ms
            if (!payload.data.success) {
              successRate.value = 0
            } else {
              successRate.value = 100
            }
          }

          scrollToBottom()
        }
      }
    }
  } catch (error) {
    messages.value[agentMsgIndex].text = `Error: ${error.message}`
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}
</script>

<style scoped>
.cockpit-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  background: var(--bg-app);
  overflow: hidden;
}

/* Header */
.cockpit-header {
  padding: 16px 24px;
  background: rgba(10, 16, 29, 0.6);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.cockpit-title-row {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.title-with-status {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pulse-indicator {
  width: 7px;
  height: 7px;
  background: var(--primary-cyan);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--primary-cyan);
}

.cockpit-title {
  font-size: 15px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.2px;
}

.session-info {
  font-size: 11px;
  color: var(--text-dim);
  font-family: var(--font-mono);
}

.cockpit-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.control-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  padding: 6px 12px;
  border-radius: 6px;
  font-weight: 600;
}

.latency-pill {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  color: #f1f5f9;
}
.latency-pill svg {
  width: 14px;
  height: 14px;
  color: var(--primary-cyan);
}
.dim-success {
  color: #10b981;
  font-weight: 600;
}

.security-pill {
  background: rgba(157, 114, 255, 0.15);
  border: 1px solid rgba(157, 114, 255, 0.35);
  color: #c084fc;
}
.security-pill svg {
  width: 14px;
  height: 14px;
}

.control-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  padding: 6px 12px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  background: rgba(23, 36, 60, 0.5);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  transition: all 0.2s;
}
.control-btn:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.15);
  border-color: rgba(239, 68, 68, 0.4);
  color: #f87171;
}
.clear-btn {
  background: red;
  border: 1px solid #cc0000;
  color: #ffffff;
  font-weight: 600;
}
.clear-btn:hover:not(:disabled) {
  background: #cc0000;
  border-color: #990000;
  color: #ffffff;
  box-shadow: 0 0 12px rgba(255, 0, 0, 0.45);
}
.clear-btn svg {
  color: #ffffff;
}
.control-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.control-btn svg {
  width: 13px;
  height: 13px;
}
.spinning {
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 2-Column Layout */
.cockpit-workspace {
  flex: 1;
  display: grid;
  grid-template-columns: 420px 1fr;
  gap: 16px;
  padding: 16px 24px;
  overflow: hidden;
}

/* Left Panel */
.lifecycle-panel {
  background: rgba(13, 21, 39, 0.5);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-header {
  padding: 14px 16px 6px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  flex-wrap: nowrap;
}

.panel-title-group {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  white-space: nowrap;
}

.panel-title {
  font-size: 13px;
  font-weight: 700;
  color: #fff;
  white-space: nowrap;
}

.task-count-badge {
  background: rgba(16, 185, 129, 0.12);
  color: #34d399;
  font-size: 9px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid rgba(16, 185, 129, 0.25);
  white-space: nowrap;
  flex-shrink: 0;
}

.swarm-health-tag {
  color: var(--status-green);
  font-size: 10px;
  font-weight: 600;
  white-space: nowrap;
  flex-shrink: 0;
}

.panel-subtitle {
  font-size: 10px;
  color: var(--text-dim);
  padding: 0 16px 12px 16px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.task-cards-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 16px 16px 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.task-card {
  background: rgba(10, 16, 31, 0.9);
  border: 1px solid rgba(23, 36, 60, 0.8);
  border-radius: 8px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  transition: border-color 0.2s;
}
.task-card:hover {
  border-color: rgba(0, 229, 255, 0.3);
}

.task-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  min-width: 0;
}

.task-id-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  flex-shrink: 0;
  white-space: nowrap;
}

.task-id {
  color: var(--text-dim);
  font-family: var(--font-mono);
  font-weight: 700;
  white-space: nowrap;
}

.task-status {
  display: flex;
  align-items: center;
  gap: 3px;
  color: var(--status-green);
  font-weight: 600;
  white-space: nowrap;
}
.task-status svg {
  width: 10px;
  height: 10px;
  flex-shrink: 0;
}

.task-timing {
  color: var(--text-dim);
  font-family: var(--font-mono);
  white-space: nowrap;
}

.task-output-badge {
  background: rgba(0, 229, 255, 0.08);
  color: var(--primary-cyan);
  font-size: 10px;
  padding: 2px 8px;
  border-radius: 4px;
  border: 1px solid rgba(0, 229, 255, 0.2);
  font-family: var(--font-mono);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 170px;
  flex-shrink: 1;
  text-align: right;
}

.task-card-body {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.task-name {
  font-size: 12px;
  font-weight: 600;
  color: #f1f5f9;
}

.task-desc {
  font-size: 11px;
  color: var(--text-muted);
  word-break: break-all;
}

.task-output-box {
  margin-top: 4px;
  padding: 6px 8px;
  background: rgba(0, 229, 255, 0.05);
  border: 1px solid rgba(0, 229, 255, 0.18);
  border-radius: 4px;
  font-size: 11px;
  line-height: 1.45;
  color: #cbd5e1;
  max-height: 80px;
  overflow-y: auto;
  word-break: break-word;
}

.output-box-label {
  color: var(--primary-cyan);
  font-weight: 700;
  margin-right: 4px;
  font-family: var(--font-mono);
  font-size: 10px;
}

.output-box-content {
  font-family: var(--font-mono);
  font-size: 10.5px;
}

.task-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 4px;
  padding-top: 6px;
  border-top: 1px solid rgba(23, 36, 60, 0.6);
  font-size: 10px;
}

.tool-tag {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--text-dim);
  font-family: var(--font-mono);
}
.tool-tag svg {
  width: 11px;
  height: 11px;
  color: var(--primary-cyan);
}

.exit-code {
  color: var(--text-dim);
  font-family: var(--font-mono);
}

.timeline-footer {
  padding: 10px 16px;
  background: rgba(10, 16, 31, 0.95);
  border-top: 1px solid var(--border-color);
}
.timeline-meta {
  display: flex;
  justify-content: space-between;
  font-size: 10px;
  color: var(--text-dim);
  margin-bottom: 6px;
}
.sparkline-wrapper {
  height: 24px;
}
.sparkline {
  width: 100%;
  height: 100%;
}

/* Right Panel */
.stream-panel {
  background: rgba(13, 21, 39, 0.5);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.stream-icon {
  color: var(--primary-cyan);
  display: flex;
  align-items: center;
}
.stream-icon svg {
  width: 15px;
  height: 15px;
}

.stream-tags {
  display: flex;
  align-items: center;
  gap: 12px;
}

.reasoning-tag {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 10px;
  color: #c084fc;
}
.reasoning-tag svg {
  width: 12px;
  height: 12px;
}

.agent-connected-tag {
  color: var(--status-green);
  font-size: 10px;
  font-weight: 600;
}

.stream-chat-box {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chat-turn {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.turn-header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 10px;
  color: var(--text-dim);
  font-family: var(--font-mono);
}

.turn-number {
  font-weight: 700;
  color: #38bdf8;
}

.user-bubble-card {
  display: flex;
  gap: 10px;
  background: rgba(14, 23, 42, 0.85);
  border: 2px solid dodgerblue;
  border-radius: 8px;
  padding: 12px 14px;
  box-shadow: 0 0 14px rgba(30, 144, 255, 0.2);
}

.user-avatar-small {
  width: 26px;
  height: 26px;
  border-radius: 6px;
  background: rgba(0, 229, 255, 0.1);
  color: var(--primary-cyan);
  display: flex;
  align-items: center;
  justify-content: center;
}
.user-avatar-small svg {
  width: 14px;
  height: 14px;
}

.user-content {
  flex: 1;
}

.author-tag {
  font-size: 10px;
  color: var(--text-dim);
  display: block;
  margin-bottom: 4px;
}

.user-text {
  font-size: 13px;
  color: #f8fafc;
  line-height: 1.5;
}

.agent-bubble-card {
  background: rgba(10, 16, 31, 0.95);
  border: 1px solid deeppink;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 0 15px rgba(255, 20, 147, 0.18);
}

.agent-card-header {
  padding: 8px 14px;
  background: rgba(255, 20, 147, 0.06);
  border-bottom: 1px solid rgba(255, 20, 147, 0.3);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.agent-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.agent-logo-pill {
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
}
.agent-logo-pill svg {
  width: 18px;
  height: 18px;
}

.agent-name {
  font-size: 12px;
  font-weight: 700;
  color: #fff;
}

.agent-status-tag {
  color: var(--status-green);
  font-size: 10px;
  font-weight: 600;
}

.agent-card-body {
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.thought-section {
  background: rgba(15, 23, 42, 0.6);
  border-left: 2px solid var(--primary-purple);
  border-radius: 4px;
  padding: 8px 12px;
}

.thought-header {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  font-weight: 600;
  color: #c084fc;
  margin-bottom: 4px;
}
.thought-header svg {
  width: 12px;
  height: 12px;
}

.thought-content p {
  font-size: 11px;
  color: #94a3b8;
  font-family: var(--font-mono);
  line-height: 1.4;
}

.tool-calls-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tool-chip {
  background: rgba(0, 229, 255, 0.06);
  border: 1px solid rgba(0, 229, 255, 0.2);
  border-radius: 4px;
  padding: 4px 8px;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  font-family: var(--font-mono);
}
.tool-chip svg {
  width: 11px;
  height: 11px;
  color: var(--primary-cyan);
}
.chip-label {
  color: var(--text-dim);
}
.chip-val {
  color: #38bdf8;
}

.final-answer-box {
  background: rgba(16, 185, 129, 0.05);
  border: 1px solid rgba(16, 185, 129, 0.25);
  border-radius: 6px;
  padding: 10px 12px;
}

.answer-header {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.8px;
  color: #34d399;
  margin-bottom: 4px;
}

.answer-text {
  font-size: 12px;
  color: #f1f5f9;
  line-height: 1.5;
  white-space: pre-wrap;
}

/* Input Form */
.stream-input-container {
  padding: 12px 16px;
  background: rgba(10, 16, 31, 0.95);
  border-top: 1px solid var(--border-color);
}

.cockpit-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input-icon {
  position: absolute;
  left: 12px;
  width: 16px;
  height: 16px;
  color: var(--text-dim);
}

.input-wrapper input {
  width: 100%;
  background: rgba(13, 21, 39, 0.8);
  border: 1px solid rgba(23, 36, 60, 0.9);
  border-radius: 6px;
  padding: 10px 12px 10px 38px;
  color: #fff;
  font-size: 12px;
  outline: none;
  transition: all 0.2s;
}
.input-wrapper input:focus {
  border-color: var(--primary-cyan);
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.15);
}

.form-bottom-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.tools-info-pills {
  display: flex;
  align-items: center;
  gap: 12px;
}

.pill-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 10px;
  color: var(--text-dim);
}
.pill-item svg {
  width: 12px;
  height: 12px;
  color: var(--primary-cyan);
}

.form-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.shortcut-hint {
  font-size: 10px;
  color: var(--text-dim);
  font-family: var(--font-mono);
}

.send-btn {
  background: #00e5ff;
  border: none;
  border-radius: 6px;
  padding: 6px 14px;
  color: #080d1a;
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 0 12px rgba(0, 229, 255, 0.3);
}
.send-btn:hover:not(:disabled) {
  background: #38bdf8;
  transform: translateY(-1px);
}
.send-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.send-btn svg {
  width: 13px;
  height: 13px;
  fill: currentColor;
}

/* HITL Modal */
.hitl-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.hitl-modal {
  width: 480px;
  background: #0d1527;
  border: 1px solid rgba(239, 68, 68, 0.4);
  border-radius: 12px;
  box-shadow: 0 0 30px rgba(239, 68, 68, 0.2);
  overflow: hidden;
}

.modal-glow-header {
  padding: 14px 18px;
  background: rgba(239, 68, 68, 0.08);
  border-bottom: 1px solid rgba(239, 68, 68, 0.2);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.warning-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 700;
  color: #f87171;
}
.warning-badge svg {
  width: 18px;
  height: 18px;
}

.security-level {
  font-size: 9px;
  font-weight: 700;
  background: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  padding: 2px 6px;
  border-radius: 4px;
}

.modal-body {
  padding: 18px;
}

.modal-notice {
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 12px;
}

.code-payload pre {
  background: #060a14;
  border: 1px solid #1e293b;
  border-radius: 6px;
  padding: 12px;
  color: #38bdf8;
  font-family: var(--font-mono);
  font-size: 11px;
  white-space: pre-wrap;
}

.modal-actions {
  padding: 14px 18px;
  background: rgba(10, 16, 31, 0.95);
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn-deny {
  background: transparent;
  border: 1px solid rgba(239, 68, 68, 0.4);
  color: #f87171;
  padding: 8px 14px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}
.btn-deny:hover {
  background: rgba(239, 68, 68, 0.15);
}
.btn-deny svg {
  width: 13px;
  height: 13px;
}

.btn-approve {
  background: #10b981;
  border: none;
  color: #060a14;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
  transition: all 0.2s;
}
.btn-approve:hover {
  background: #34d399;
}
.btn-approve svg {
  width: 13px;
  height: 13px;
}
</style>
