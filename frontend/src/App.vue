<template>
  <div class="chat-container">
    <h1>Agentic Ops Assistant</h1>
    
    <div class="chat-box">
      <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role]">
        <strong>{{ msg.role === 'user' ? 'You' : 'Agent' }}:</strong> {{ msg.text }}
      </div>
    </div>

    <form @submit.prevent="sendMessage" class="input-form">
      <input v-model="userInput" type="text" placeholder="Ask me to do math or check the weather..." required />
      <button type="submit" :disabled="isLoading">Send</button>
    </form>

        <!-- HITL Approval Modal -->
    <div v-if="pendingApproval" class="approval-modal">
      <div class="modal-content">
        <h3>⚠️ Human Approval Required</h3>
        <p>The agent wants to run a dangerous tool:</p>
        <pre>{{ pendingApproval }}</pre>
        <div class="button-group">
          <button @click="handleApproval(true)" class="btn-approve">Approve</button>
          <button @click="handleApproval(false)" class="btn-deny">Deny</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const userInput = ref('')
const messages = ref([])
const isLoading = ref(false)
const sessionId = ref(crypto.randomUUID())
const pendingApproval = ref(null)

// This runs automatically when the page loads
onMounted(async () => {
  // 1. Check if we have a session ID saved in the browser
  let savedSessionId = localStorage.getItem('agent_session_id')
  
  if (!savedSessionId) {
    // If not, create a new one and save it
    savedSessionId = crypto.randomUUID()
    localStorage.setItem('agent_session_id', savedSessionId)
  }
  
  sessionId.value = savedSessionId

  // 2. Fetch the chat history from the backend
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/history?session_id=${savedSessionId}`)
    if (res.ok) {
      const data = await res.json()
      messages.value = data.messages
    }
  } catch (err) {
    console.error("Failed to load history:", err)
  }
})

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
    console.error("Failed to send approval:", err)
  } finally {
    pendingApproval.value = null // Hide the modal
  }
}


const sendMessage = async () => {
  if (!userInput.value.trim()) return

  const prompt = userInput.value
  messages.value.push({ role: 'user', text: prompt })
  userInput.value = ''
  isLoading.value = true

  // Add a placeholder for the agent's response
  const agentMsgIndex = messages.value.push({ role: 'agent', text: '' }) - 1

  try {
    // Connect to the FastAPI SSE endpoint
    const response = await fetch(`http://127.0.0.1:8000/api/chat?prompt=${encodeURIComponent(prompt)}&session_id=${sessionId.value}`)


    if (!response.body) throw new Error("ReadableStream not supported")
    
    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')

    let buffer = ''
    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      // Decode the chunk and append to buffer
      buffer += decoder.decode(value, { stream: true })
      
      // Split by SSE double-newline
      const parts = buffer.split('\n\n')
      // Retain incomplete trailing data in the buffer
      buffer = parts.pop() || ''

      for (const part of parts) {
        const trimmed = part.trim()
        if (trimmed.startsWith('data: ')) {
          const raw = trimmed.slice(6)
          let text = raw
          try {
            // Parse JSON-encoded message safely
            text = JSON.parse(raw)
          } catch {
            // Fallback for raw text
          }

          // Check for human-in-the-loop approval trigger
          if (typeof text === 'string' && text.startsWith('[WAITING_FOR_APPROVAL]')) {
            pendingApproval.value = text.replace('[WAITING_FOR_APPROVAL]', '').trim()
          }

          messages.value[agentMsgIndex].text += text + '\n'
        }
      }
    }
  } catch (error) {
    messages.value[agentMsgIndex].text = `Error: ${error.message}`
  } finally {
    isLoading.value = false
  }
}
</script>

<style>
/* Basic styling to make it look like a chat app */
.chat-container {
  max-width: 600px;
  margin: 40px auto;
  font-family: sans-serif;
}
.chat-box {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  height: 400px;
  overflow-y: auto;
  background: #f9f9f9;
  margin-bottom: 20px;
}
.message {
  margin-bottom: 10px;
  white-space: pre-wrap; /* Keeps the line breaks from SSE */
}
.message.user { color: blue; }
.message.agent { color: green; }
.input-form { display: flex; gap: 10px; }
.input-form input { flex: 1; padding: 10px; }
.input-form button { padding: 10px 20px; }
.approval-modal {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex; justify-content: center; align-items: center;
  z-index: 1000;
}
.modal-content {
  background: white; padding: 20px; border-radius: 8px; max-width: 400px;
}
pre { background: #f4f4f4; padding: 10px; overflow-x: auto; }
.button-group { display: flex; gap: 10px; margin-top: 15px; }
.btn-approve { background: #4CAF50; color: white; padding: 10px; border: none; cursor: pointer; }
.btn-deny { background: #f44336; color: white; padding: 10px; border: none; cursor: pointer; }
</style>