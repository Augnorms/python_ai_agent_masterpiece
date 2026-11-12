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
              <p class="task-desc">
                <span class="args-badge">Args:</span>
                <span class="args-text">{{ formatTaskDesc(task.description) }}</span>
              </p>
              
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
                <span class="tool-label">Tool:</span>
                <span class="tool-name">{{ task.tool }}</span>
              </span>
              <span class="exit-code">EXIT CODE: 0</span>
            </div>
          </div>
        </div>

        <!-- Execution Timeline Sparkline -->
        <div class="timeline-footer">
          <div class="timeline-meta">
            <span class="meta-label">Execution Timeline & Health</span>
            <span class="meta-val">Avg: {{ averageDuration }} / task</span>
          </div>
          <div class="sparkline-wrapper">
            <svg class="sparkline" viewBox="0 0 300 24" fill="none">
              <path :d="sparklinePath" stroke="#00e5ff" stroke-width="1.8" stroke-linecap="round" />
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
              <div class="user-avatar-small" :title="loggedInUsername ? `Operator: ${loggedInUsername}` : 'Operator'">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
              </div>
              <div class="user-content">
                <span class="author-tag">{{ loggedInUsername ? `${loggedInUsername} (You)` : 'User (You)' }}</span>
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
                  Tools: Weather, DB, Email, RAG
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
import { ref, onMounted, nextTick, computed  } from 'vue'
import HumanInTheLoopModal from '../components/HumanInTheLoopModal.vue'

const userInput = ref('')
const messages = ref([])
const isLoading = ref(false)
const isClearingMemory = ref(false)
const sessionId = ref('default')
const loggedInUsername = ref('')
const pendingApproval = ref(null)
const chatBoxRef = ref(null)
const taskLifecycle = ref([])
const latency = ref(0)
const successRate = ref(0)
const taskDurations = ref([])

const getLoggedInUsername = () => {
  const userJson = localStorage.getItem('scada_user')
  if (userJson) {
    try {
      const u = JSON.parse(userJson)
      if (u && u.username) return u.username
    } catch {}
  }
  const token = localStorage.getItem('scada_access_token')
  if (token) {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      if (payload && payload.sub) return payload.sub
    } catch {}
  }
  return localStorage.getItem('scada_station_operator') || ''
}

const getUserSessionId = () => {
  const token = localStorage.getItem('scada_access_token')
  if (token) {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      if (payload && payload.id) {
        return String(payload.id)
      }
    } catch (e) {
      console.warn('Could not decode token payload', e)
    }
  }
  const userStr = localStorage.getItem('scada_user')
  if (userStr) {
    try {
      const u = JSON.parse(userStr)
      if (u && (u.id || u.user_id)) return String(u.id || u.user_id)
    } catch (e) {}
  }
  return localStorage.getItem('agent_session_id') || 'default'
}

const scrollToBottom = async () => {
  await nextTick()
  if (chatBoxRef.value) {
    chatBoxRef.value.scrollTop = chatBoxRef.value.scrollHeight
  }
}

onMounted(async () => {
  loggedInUsername.value = getLoggedInUsername()
  window.addEventListener('auth-changed', () => {
    loggedInUsername.value = getLoggedInUsername()
  })

  const currentSid = getUserSessionId()
  sessionId.value = currentSid
  localStorage.setItem('agent_session_id', currentSid)

  try {
    const res = await fetch(`http://127.0.0.1:8000/api/history?session_id=${encodeURIComponent(currentSid)}`)
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

const averageDuration = computed(() => {
  if (taskDurations.value.length === 0) return "0.00s"
  const sum = taskDurations.value.reduce((a, b) => a + b, 0)
  const avgMs = sum / taskDurations.value.length
  return (avgMs / 1000).toFixed(2) + "s"
})

const sparklinePath = computed(() => {
  if (taskDurations.value.length < 2) {
    return 'M0 16 Q 40 10, 80 14 T 160 12 T 240 8 T 300 14'
  }
  const durations = taskDurations.value
  const max = Math.max(...durations, 300)
  const min = Math.min(...durations, 50)
  const range = max - min || 1
  const step = 300 / (durations.length - 1)

  const points = durations.map((d, i) => {
    const x = Math.round(i * step)
    const y = Math.round(20 - ((d - min) / range) * 14)
    return { x, y }
  })

  let path = `M ${points[0].x} ${points[0].y}`
  for (let i = 1; i < points.length; i++) {
    const prev = points[i - 1]
    const curr = points[i]
    const midX = (prev.x + curr.x) / 2
    path += ` C ${midX} ${prev.y}, ${midX} ${curr.y}, ${curr.x} ${curr.y}`
  }
  return path
})

const clearMemory = async () => {
  if (isClearingMemory.value) return
  isClearingMemory.value = true

  const prevSessionId = sessionId.value
  const token = localStorage.getItem('scada_access_token')
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/memory/${encodeURIComponent(prevSessionId)}`, {
      method: 'DELETE',
      headers: {
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
      }
    })
    if (!res.ok) {
      console.warn(`Memory clear returned status ${res.status}`)
    }
  } catch (err) {
    console.error('Failed to clear memory on backend:', err)
  } finally {
    messages.value = []
    taskLifecycle.value = []
    taskDurations.value = []
    isClearingMemory.value = false
  }
}

const handleApproval = async (isApproved) => {
  const token = localStorage.getItem('scada_access_token')
  try {
    await fetch('http://127.0.0.1:8000/api/approve', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
      },
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

const formatTaskDesc = (desc) => {
  if (!desc) return ''
  return desc.startsWith('Args:') ? desc.replace(/^Args:\s*/, '') : desc
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

  const token = localStorage.getItem('scada_access_token')
  if (!token) {
    messages.value[agentMsgIndex].text = '[Authentication Error] SCADA Session Token missing. Please sign in via the SCADA gateway.'
    isLoading.value = false
    return
  }

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/chat?prompt=${encodeURIComponent(prompt)}&session_id=${encodeURIComponent(sessionId.value)}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.status === 401) {
      messages.value[agentMsgIndex].text = '[Authentication Error] Session expired or invalid credentials (401 Unauthorized). Please sign in again.'
      isLoading.value = false
      return
    }

    if (!response.ok) {
      throw new Error(`Server returned ${response.status} ${response.statusText}`)
    }

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
                const durMs = Number(taskData.duration_ms) || 150
                taskLifecycle.value[taskIndex].duration = (durMs / 1000).toFixed(2) + 's'

                // Save the duration for the sparkline
                taskDurations.value.push(durMs) 
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

<style scoped src="@/style_folder/AgentOrchestratorView.css"></style>
