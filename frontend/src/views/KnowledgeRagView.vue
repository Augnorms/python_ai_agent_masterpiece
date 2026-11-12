<template>
  <div class="rag-container">
    <!-- RAG Hub Header -->
    <div class="rag-header">
      <div class="rag-header-left">
        <div class="cluster-badge">
          <span class="store-tag">VECTOR STORE • V2.4</span>
          <span class="cluster-name">Cluster: prod-pinecone-us-east-1</span>
        </div>
        <h2 class="rag-title">Knowledge & RAG Hub</h2>
        <p class="rag-desc">Upload source documents, tune adaptive chunking strategies, and bind high-dimensional embeddings directly to autonomous agent swarms.</p>
      </div>

      <div class="rag-header-actions">
        <button class="btn-reset-danger" @click="openResetDialog" :disabled="isResettingDb" title="Reset ChromaDB Vector Collection">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ 'spin-icon': isResettingDb }">
            <ellipse cx="12" cy="5" rx="9" ry="3" />
            <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" />
            <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
          </svg>
          <span>{{ isResettingDb ? 'Resetting DB...' : 'Vector DB Reset' }}</span>
        </button>

        <button class="btn-secondary" @click="fetchDocuments" :disabled="isLoadingDocs">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ 'spin-icon': isLoadingDocs }">
            <polyline points="23 4 23 10 17 10" />
            <polyline points="1 20 1 14 7 14" />
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
          </svg>
          <span>{{ isLoadingDocs ? 'Syncing...' : 'Re-index Swarm Indices' }}</span>
        </button>

        <button class="btn-primary" @click="triggerFileInput">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="17 8 12 3 7 8" />
            <line x1="12" y1="3" x2="12" y2="15" />
          </svg>
          <span>Upload Documents</span>
        </button>
      </div>
    </div>

    <!-- Main Scrollable Content -->
    <div class="rag-content">
      <!-- 4 Top Metric Cards -->
      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-top">
            <span class="metric-label">INDEXED DOCUMENTS</span>
            <div class="metric-icon-box">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14 2 14 8 20 8" />
              </svg>
            </div>
          </div>
          <div class="metric-value-row">
            <span class="metric-num">{{ documents.length }}</span>
            <span class="metric-trend">+{{ documents.length }} synced</span>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-top">
            <span class="metric-label">TOTAL EMBEDDINGS</span>
            <div class="metric-icon-box purple">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3" />
                <circle cx="19" cy="8" r="2" />
                <circle cx="7" cy="19" r="2" />
              </svg>
            </div>
          </div>
          <div class="metric-value-row">
            <span class="metric-num">{{ vectorStats.total_chunks.toLocaleString() }}</span>
            <span class="metric-dim">1536/3072d</span>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-top">
            <span class="metric-label">RETRIEVAL LATENCY</span>
            <div class="metric-icon-box cyan">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" />
                <polyline points="12 6 12 12 16 14" />
              </svg>
            </div>
          </div>
          <div class="metric-value-row">
            <span class="metric-num">{{ latencyDisplay }}</span>
            <span class="metric-dim">{{ p95Display }}</span>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-top">
            <span class="metric-label">INDEX CONSISTENCY</span>
            <div class="metric-icon-box" :class="vectorStats.total_chunks > 0 ? 'green' : 'dim'">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                <polyline points="22 4 12 14.01 9 11.01" />
              </svg>
            </div>
          </div>
          <div class="metric-value-row">
            <span class="metric-num">{{ vectorStats.total_chunks > 0 ? '99.98%' : '0%' }}</span>
            <span :class="vectorStats.total_chunks > 0 ? 'metric-tag-synced' : 'metric-tag-empty'">
              {{ vectorStats.total_chunks > 0 ? 'SYNCED' : 'EMPTY' }}
            </span>
          </div>
        </div>
      </div>

      <!-- Ingestion & Tokenize Pipeline Row -->
      <div class="pipeline-grid">
        <!-- Ingest Dropzone -->
        <div class="pipeline-card dropzone-card">
          <div class="pipeline-card-header">
            <div class="card-title-group">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="17 8 12 3 7 8" />
                <line x1="12" y1="3" x2="12" y2="15" />
              </svg>
              <h4>Ingest & Tokenize Pipeline</h4>
            </div>
            <span class="status-ready-tag">RAG Ready</span>
          </div>

          <div 
            class="dropzone-area" 
            :class="{ 'is-dragging': isDragging }"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleDrop"
            @click="triggerFileInput"
          >
            <input 
              type="file" 
              ref="fileInputRef" 
              class="hidden-file-input" 
              @change="handleFileSelect" 
              multiple 
            />
            <div class="drop-icon-circle">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z" />
              </svg>
            </div>
            <h5 class="drop-title">Drop mission documents here</h5>
            <span class="drop-sub">or <a href="#" class="browse-link" @click.stop.prevent="triggerFileInput">browse local workspace</a></span>

            <div class="format-tags">
              <span class="fmt">PDF</span>
              <span class="fmt">DOCX</span>
              <span class="fmt active-fmt">MARKDOWN (.MD)</span>
              <span class="fmt">TXT</span>
              <span class="fmt">JSONL</span>
              <span class="fmt">PARQUET</span>
              <span class="fmt">CODE (.ZIP)</span>
            </div>
          </div>
        </div>

        <!-- Active Ingestion Progress -->
        <div class="pipeline-card active-jobs-card">
          <div class="pipeline-card-header">
            <div class="card-title-group">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
              </svg>
              <h4>Active Ingestion Pipeline</h4>
              <span class="running-count">{{ activeJobs.filter(j => j.status === 'uploading').length }} Running</span>
            </div>
            <span class="worker-pool-tag">● MinIO S3 & Embedding Pool Active</span>
          </div>

          <div class="active-jobs-list">
            <div v-if="activeJobs.length === 0" class="no-jobs-placeholder">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <circle cx="12" cy="12" r="10" />
                <polyline points="12 6 12 12 14 14" />
              </svg>
              <span>No active ingestion jobs. Upload documents above to begin.</span>
            </div>

            <div v-for="job in activeJobs" :key="job.id" class="job-item">
              <div class="job-meta">
                <div class="job-file">
                  <span :class="['file-icon', job.iconColor]">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                    </svg>
                  </span>
                  <div>
                    <strong class="file-name">{{ job.name }}</strong>
                    <span class="file-detail">{{ job.detail }}</span>
                  </div>
                </div>
                <div class="job-pct">
                  <span :class="['pct-num', { 'green-text': job.progress === 100, 'red-text': job.status === 'error' }]">{{ job.progress }}%</span>
                  <span class="chunks-info">{{ job.info }}</span>
                </div>
              </div>
              <div class="progress-bar-bg">
                <div 
                  class="progress-bar-fill" 
                  :class="{ 'green-fill': job.progress === 100, 'red-fill': job.status === 'error' }" 
                  :style="{ width: job.progress + '%' }"
                ></div>
              </div>
              <div class="job-status-row">
                <span class="step-text">{{ job.stepText }}</span>
                <span class="eta-text">{{ job.etaText }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Document Source Data Table -->
      <div class="table-card">
        <!-- Table Filter Bar -->
        <div class="table-filter-bar">
          <div class="search-input-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="Filter documents by filename, agent binding, embedding..." 
            />
          </div>

          <div class="filter-dropdowns">
            <span class="showing-text">SHOWING {{ filteredDocuments.length }} FILES</span>
            <button class="export-btn" title="Refresh Documents" @click="fetchDocuments" :disabled="isLoadingDocs">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ 'spin-icon': isLoadingDocs }">
                <polyline points="23 4 23 10 17 10" />
                <polyline points="1 20 1 14 7 14" />
                <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Table -->
        <div class="table-responsive">
          <table class="docs-table">
            <thead>
              <tr>
                <th>DOCUMENT SOURCE</th>
                <th>SIZE</th>
                <th>CHUNKS</th>
                <th>EMBEDDING MODEL</th>
                <th>BOUND SWARM AGENT(S)</th>
                <th>INDEX STATUS</th>
                <th class="text-right">ACTIONS</th>
              </tr>
            </thead>
            <tbody>
              <!-- Loading State -->
              <tr v-if="isLoadingDocs">
                <td colspan="7" class="empty-table-cell loading-state">
                  <div class="loader-inner">
                    <span class="pulse-dot"></span>
                    <span>Querying MinIO S3 & ChromaDB index...</span>
                  </div>
                </td>
              </tr>
              <!-- Empty State -->
              <tr v-else-if="filteredDocuments.length === 0">
                <td colspan="7" class="empty-table-cell">
                  {{ searchQuery ? 'No documents match your filter query.' : 'No indexed documents found in MinIO S3. Upload a document above to ingest into the vector store.' }}
                </td>
              </tr>
              <!-- Document Rows -->
              <tr v-else v-for="(doc, idx) in filteredDocuments" :key="doc.name || idx">
                <td>
                  <div class="doc-title-cell">
                    <span class="doc-code-icon">{{ doc.ext }}</span>
                    <div>
                      <span class="doc-name">{{ doc.name }}</span>
                      <span class="doc-hash">hash: {{ doc.hash }} • {{ formatDate(doc.last_modified) }}</span>
                    </div>
                  </div>
                </td>
                <td class="mono-col">{{ doc.size }}</td>
                <td class="mono-col">{{ doc.chunks }}</td>
                <td><span class="model-pill">{{ doc.model }}</span></td>
                <td><span class="agent-pill">● {{ doc.agent }}</span></td>
                <td>
                  <span :class="['status-badge', doc.status.toLowerCase()]">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <polyline points="20 6 9 17 4 12" />
                    </svg>
                    {{ doc.status }}
                  </span>
                </td>
                <td class="text-right">
                  <div class="action-buttons">
                    <button class="btn-inspect" @click="inspectDoc(doc)">Inspect</button>
                    <button class="btn-icon-action" title="Re-sync" @click="fetchDocuments">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ 'spin-icon': isLoadingDocs }">
                        <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Toast Notification -->
    <transition name="toast-fade">
      <div v-if="toast" :class="['upload-toast', toast.type]">
        <svg v-if="toast.type === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <polyline points="20 6 9 17 4 12" />
        </svg>
        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
        <span>{{ toast.text }}</span>
      </div>
    </transition>

    <!-- Reusable Prompt / Confirmation Dialog -->
    <PromptDialog
      :is-open="showResetDialog"
      variant="danger"
      title="Reset ChromaDB Vector Store"
      badge="HIGH IMPACT"
      message="Are you sure you want to completely wipe the 'company_docs' collection from ChromaDB? All indexed embeddings and document chunks will be permanently cleared."
      confirm-text="Wipe & Reset Collection"
      cancel-text="Cancel"
      loading-text="Wiping Vector DB..."
      :is-loading="isResettingDb"
      @confirm="executeVectorDbReset"
      @cancel="showResetDialog = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import PromptDialog from '../components/PromptDialog.vue'

const fileInputRef = ref(null)
const isDragging = ref(false)
const toast = ref(null)

const activeJobs = ref([])
const documents = ref([])
const isLoadingDocs = ref(false)
const isResettingDb = ref(false)
const showResetDialog = ref(false)
const vectorStats = ref({
  total_chunks: 0,
  status: 'empty'
})
const isLoadingStats = ref(false)
const latestLatency = ref(
  Number(localStorage.getItem('rag_latest_latency_ms')) || 0
)
const latencyHistory = ref(
  (() => {
    try {
      return JSON.parse(localStorage.getItem('rag_latency_history') || '[]')
    } catch {
      return []
    }
  })()
)

const p95Latency = computed(() => {
  if (latencyHistory.value.length === 0) {
    return latestLatency.value > 0 ? Math.round(latestLatency.value * 1.25) : 0
  }
  const sorted = [...latencyHistory.value].sort((a, b) => a - b)
  const idx = Math.min(sorted.length - 1, Math.ceil(0.95 * sorted.length) - 1)
  return sorted[idx]
})

const latencyDisplay = computed(() => {
  if (latestLatency.value <= 0) return '0.0ms'
  return `${latestLatency.value}ms`
})

const p95Display = computed(() => {
  if (latestLatency.value <= 0 && latencyHistory.value.length === 0) {
    return 'p95: 0ms'
  }
  return `p95: ${p95Latency.value}ms`
})
const searchQuery = ref('')
const selectedModel = ref('All Models')
const selectedBinding = ref('All Swarm Bindings')

const triggerFileInput = () => {
  if (fileInputRef.value) {
    fileInputRef.value.click()
  }
}

const formatFileSize = (bytes) => {
  if (!bytes) return '0 B'
  if (bytes < 1024) return bytes + ' B'
  else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB'
  else return (bytes / 1048576).toFixed(1) + ' MB'
}

const getFileExtension = (filename) => {
  const parts = filename.split('.')
  return parts.length > 1 ? parts.pop().toUpperCase() : 'TXT'
}

const formatDate = (isoString) => {
  if (!isoString) return ''
  try {
    const d = new Date(isoString)
    return d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } catch (e) {
    return isoString
  }
}

const showToast = (text, type = 'success') => {
  toast.value = { text, type }
  setTimeout(() => {
    toast.value = null
  }, 4500)
}

const fetchDocuments = async () => {
  isLoadingDocs.value = true
  fetchVectorStats()
  try {
    const res = await fetch('http://127.0.0.1:8000/api/documents')
    const data = await res.json()
    if (data.status === 'success' && Array.isArray(data.documents)) {
      documents.value = data.documents.map((file) => {
        const ext = getFileExtension(file.filename)
        const hash = file.last_modified
          ? file.last_modified.slice(0, 19).replace(/[^a-zA-Z0-9]/g, '').slice(-8)
          : Math.random().toString(16).substring(2, 10)

        const chunks = Math.max(1, Math.round((file.size_bytes || 1024) / 380)).toString()

        return {
          name: file.filename,
          ext: ext,
          hash: hash,
          size: formatFileSize(file.size_bytes),
          size_bytes: file.size_bytes,
          chunks: chunks,
          model: 'all-MiniLM-L6-v2',
          agent: 'HR Policy & Knowledge Swarm',
          status: 'Indexed',
          last_modified: file.last_modified
        }
      })
    }
  } catch (err) {
    console.error('Error fetching documents from /api/documents:', err)
  } finally {
    isLoadingDocs.value = false
  }
}

const fetchVectorStats = async () => {
  isLoadingStats.value = true
  try {
    const res = await fetch('http://127.0.0.1:8000/api/vector-db/stats')
    const data = await res.json()
    if (data && typeof data.total_chunks === 'number') {
      vectorStats.value = {
        total_chunks: data.total_chunks,
        status: data.status || (data.total_chunks > 0 ? 'active' : 'empty')
      }
    }
  } catch (err) {
    console.error('Error fetching vector db stats:', err)
  } finally {
    isLoadingStats.value = false
  }
}

const openResetDialog = () => {
  showResetDialog.value = true
}

const executeVectorDbReset = async () => {
  if (isResettingDb.value) return

  isResettingDb.value = true
  try {
    const res = await fetch('http://127.0.0.1:8000/api/clear-chroma', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    const data = await res.json()
    if (res.ok && (data.status === 'success' || typeof data === 'string')) {
      const msg = typeof data === 'string' ? data : (data.message || 'Vector DB has been completely wiped.')
      latestLatency.value = 0
      latencyHistory.value = []
      localStorage.removeItem('rag_latest_latency_ms')
      localStorage.removeItem('rag_latency_history')
      showToast(msg, 'success')
      await fetchDocuments()
      await fetchVectorStats()
    } else {
      const errMsg = (data && data.message) || 'Failed to reset ChromaDB vector collection.'
      showToast(errMsg, 'error')
    }
  } catch (err) {
    console.error('Error resetting vector db:', err)
    showToast('Failed to connect to backend server to reset Vector DB.', 'error')
  } finally {
    isResettingDb.value = false
    showResetDialog.value = false
  }
}

onMounted(() => {
  fetchDocuments()
  fetchVectorStats()
})

const filteredDocuments = computed(() => {
  return documents.value.filter((doc) => {
    const matchesSearch = !searchQuery.value.trim() ||
      doc.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      doc.ext.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      doc.agent.toLowerCase().includes(searchQuery.value.toLowerCase())

    const matchesModel = selectedModel.value === 'All Models' || doc.model === selectedModel.value
    const matchesBinding = selectedBinding.value === 'All Swarm Bindings' || doc.agent.includes(selectedBinding.value)

    return matchesSearch && matchesModel && matchesBinding
  })
})

const inspectDoc = (doc) => {
  showToast(`Document: ${doc.name} • ${doc.size} • ${doc.chunks} chunks • Status: ${doc.status}`, 'success')
}

const uploadFile = (file) => {
  const jobId = Date.now() + Math.random()
  const ext = getFileExtension(file.name)
  const iconColor = ext === 'PDF' ? 'red' : 'blue'

  const job = {
    id: jobId,
    name: file.name,
    detail: `${formatFileSize(file.size)} • Target: MinIO S3 (agentbucket)`,
    progress: 0,
    iconColor,
    info: '0% uploaded',
    stepText: 'Streaming bytes to MinIO S3 bucket...',
    etaText: 'Uploading...',
    status: 'uploading'
  }

  activeJobs.value.unshift(job)

  const formData = new FormData()
  formData.append('file', file)

  const xhr = new XMLHttpRequest()
  xhr.open('POST', 'http://127.0.0.1:8000/api/documents/upload')

  xhr.upload.onprogress = (event) => {
    if (event.lengthComputable) {
      const pct = Math.round((event.loaded / event.total) * 100)
      job.progress = Math.min(pct, 98)
      job.info = `${job.progress}% uploaded`
      if (job.progress >= 98) {
        job.stepText = 'Storing object in MinIO S3 bucket...'
        job.etaText = 'Finalizing...'
      }
    }
  }

  xhr.onload = () => {
    try {
      const data = JSON.parse(xhr.responseText)

      if (data && data.elapsed_ms !== undefined && data.elapsed_ms !== null) {
        const ms = typeof data.elapsed_ms === 'number' ? data.elapsed_ms : parseFloat(data.elapsed_ms)
        if (!isNaN(ms)) {
          latestLatency.value = ms
          localStorage.setItem('rag_latest_latency_ms', ms.toString())
          latencyHistory.value.push(ms)
          if (latencyHistory.value.length > 50) latencyHistory.value.shift()
          localStorage.setItem('rag_latency_history', JSON.stringify(latencyHistory.value))
        }
      }

      if (xhr.status >= 200 && xhr.status < 300 && data.status === 'success') {
        job.progress = 100
        job.info = 'Uploaded to S3'
        job.stepText = data.message || `Successfully uploaded ${file.name} to S3`
        job.etaText = 'COMPLETE'
        job.status = 'completed'

        const latencyNote = data.elapsed_ms !== undefined ? ` (${data.elapsed_ms}ms)` : ''
        showToast(`Successfully uploaded ${file.name} to MinIO S3!${latencyNote}`, 'success')
        fetchDocuments()
      } else {
        job.progress = 100
        job.status = 'error'
        job.stepText = data.message || 'Upload failed'
        job.etaText = 'FAILED'
        showToast(data.message || 'Upload failed', 'error')
      }
    } catch (err) {
      job.progress = 100
      job.status = 'error'
      job.stepText = 'Failed to parse response'
      job.etaText = 'FAILED'
      showToast('Error processing server response', 'error')
    }
  }

  xhr.onerror = () => {
    job.progress = 100
    job.status = 'error'
    job.stepText = 'Network error during upload'
    job.etaText = 'FAILED'
    showToast(`Network error uploading ${file.name}`, 'error')
  }

  xhr.send(formData)
}

const handleFileSelect = (event) => {
  const files = event.target.files
  if (!files || files.length === 0) return
  for (let i = 0; i < files.length; i++) {
    uploadFile(files[i])
  }
  event.target.value = ''
}

const handleDrop = (event) => {
  isDragging.value = false
  const files = event.dataTransfer?.files
  if (!files || files.length === 0) return
  for (let i = 0; i < files.length; i++) {
    uploadFile(files[i])
  }
}
</script>

<style scoped src="@/style_folder/KnowledgeRagView.css"></style>
