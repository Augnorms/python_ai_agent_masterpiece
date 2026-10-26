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
        <button class="btn-secondary">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <ellipse cx="12" cy="5" rx="9" ry="3" />
            <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" />
            <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
          </svg>
          <span>Vector DB Config</span>
        </button>

        <button class="btn-secondary">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="23 4 23 10 17 10" />
            <polyline points="1 20 1 14 7 14" />
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
          </svg>
          <span>Re-index Swarm Indices</span>
        </button>

        <button class="btn-primary">
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
            <span class="metric-num">1,420</span>
            <span class="metric-trend">+18 today</span>
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
            <span class="metric-num">3.84M</span>
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
            <span class="metric-num">16.2ms</span>
            <span class="metric-dim">p95: 28ms</span>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-top">
            <span class="metric-label">INDEX CONSISTENCY</span>
            <div class="metric-icon-box green">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                <polyline points="22 4 12 14.01 9 11.01" />
              </svg>
            </div>
          </div>
          <div class="metric-value-row">
            <span class="metric-num">99.98%</span>
            <span class="metric-tag-synced">SYNCED</span>
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

          <div class="dropzone-area">
            <div class="drop-icon-circle">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z" />
              </svg>
            </div>
            <h5 class="drop-title">Drop mission documents here</h5>
            <span class="drop-sub">or <a href="#" class="browse-link">browse local workspace</a></span>

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
              <span class="running-count">2 Running</span>
            </div>
            <span class="worker-pool-tag">● Embedding Worker Pool: 8/8 Active</span>
          </div>

          <div class="active-jobs-list">
            <div class="job-item">
              <div class="job-meta">
                <div class="job-file">
                  <span class="file-icon red">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                    </svg>
                  </span>
                  <div>
                    <strong class="file-name">production_failover_playbook_v3.pdf</strong>
                    <span class="file-detail">3.4 MB • Embedding Model: text-embedding-3-large (3072d)</span>
                  </div>
                </div>
                <div class="job-pct">
                  <span class="pct-num">82%</span>
                  <span class="chunks-info">412 chunks ready</span>
                </div>
              </div>
              <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: 82%"></div>
              </div>
              <div class="job-status-row">
                <span class="step-text">Generating dense embeddings + HyDE synthetic queries</span>
                <span class="eta-text">ETA: ~4s</span>
              </div>
            </div>

            <div class="job-item">
              <div class="job-meta">
                <div class="job-file">
                  <span class="file-icon blue">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                    </svg>
                  </span>
                  <div>
                    <strong class="file-name">company_policy.txt</strong>
                    <span class="file-detail">ChromaDB Collection: company_docs (all-MiniLM-L6-v2)</span>
                  </div>
                </div>
                <div class="job-pct">
                  <span class="pct-num green-text">100%</span>
                  <span class="chunks-info">6 chunks indexed</span>
                </div>
              </div>
              <div class="progress-bar-bg">
                <div class="progress-bar-fill green-fill" style="width: 100%"></div>
              </div>
              <div class="job-status-row">
                <span class="step-text">Broadcasting vectors to ChromaDB cluster</span>
                <span class="eta-text">COMPLETE</span>
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
            <input type="text" placeholder="Filter documents by filename, agent binding, embedding..." />
          </div>

          <div class="filter-dropdowns">
            <select class="filter-select">
              <option>All Models</option>
              <option>all-MiniLM-L6-v2</option>
              <option>text-embedding-3-large</option>
            </select>

            <select class="filter-select">
              <option>All Swarm Bindings</option>
              <option>HR Policy Agent</option>
              <option>Architect Swarm</option>
            </select>

            <span class="showing-text">SHOWING 5 OF 1,420 FILES</span>
            <button class="export-btn" title="Export Manifest">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="7 10 12 15 17 10" />
                <line x1="12" y1="15" x2="12" y2="3" />
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
              <tr v-for="(doc, idx) in documents" :key="idx">
                <td>
                  <div class="doc-title-cell">
                    <span class="doc-code-icon">{{ doc.ext }}</span>
                    <div>
                      <span class="doc-name">{{ doc.name }}</span>
                      <span class="doc-hash">hash: {{ doc.hash }}</span>
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
                    <button class="btn-inspect">Inspect</button>
                    <button class="btn-icon-action" title="Re-sync">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
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
  </div>
</template>

<script setup>
import { ref } from 'vue'

const documents = ref([
  {
    name: 'company_policy.txt',
    ext: 'TXT',
    hash: '8f19ab...c01',
    size: '850 B',
    chunks: '6',
    model: 'all-MiniLM-L6-v2',
    agent: 'HR Policy Agent',
    status: 'Indexed'
  },
  {
    name: 'swarm_protocol_v2_core.ts',
    ext: '< >',
    hash: '9f81a7b...',
    size: '210 KB',
    chunks: '32',
    model: 'voyage-code-2 (1536d)',
    agent: 'Architect Swarm',
    status: 'Indexed'
  },
  {
    name: 'pci_dss_compliance_runbook_2024.pdf',
    ext: 'PDF',
    hash: 'e3a019d...',
    size: '5.2 MB',
    chunks: '512',
    model: 'text-embedding-3-large',
    agent: 'SecOps Auditor',
    status: 'Indexed'
  },
  {
    name: 'global_sla_tiering_policy.docx',
    ext: 'DOC',
    hash: 'b44901c...',
    size: '1.1 MB',
    chunks: '144',
    model: 'text-embedding-3-small',
    agent: 'Support Worker',
    status: 'Indexed'
  },
  {
    name: 'enterprise_knowledge_graph_oct.parquet',
    ext: 'PQT',
    hash: '11a4cf9...',
    size: '42.8 MB',
    chunks: '3,490',
    model: 'text-embedding-3-large',
    agent: 'Swarm Supervisor',
    status: 'Indexed'
  }
])
</script>

<style scoped>
.rag-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  background: var(--bg-app);
  overflow: hidden;
}

/* Header */
.rag-header {
  padding: 16px 24px;
  background: rgba(10, 16, 29, 0.6);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.cluster-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  margin-bottom: 4px;
}

.store-tag {
  color: var(--primary-cyan);
  font-weight: 700;
  font-family: var(--font-mono);
}

.cluster-name {
  color: var(--text-dim);
}

.rag-title {
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.2px;
}

.rag-desc {
  font-size: 11px;
  color: var(--text-muted);
  max-width: 650px;
  margin-top: 2px;
}

.rag-header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-secondary {
  background: rgba(13, 21, 39, 0.8);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-main);
  padding: 7px 12px;
  font-size: 11px;
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
  padding: 7px 14px;
  font-size: 11px;
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

/* Scrollable Content */
.rag-content {
  flex: 1;
  overflow-y: auto;
  padding: 18px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 4 Metric Cards */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}

.metric-card {
  background: rgba(13, 21, 39, 0.6);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.metric-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.metric-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.8px;
  color: var(--text-dim);
}

.metric-icon-box {
  width: 26px;
  height: 26px;
  border-radius: 6px;
  background: rgba(0, 229, 255, 0.1);
  color: var(--primary-cyan);
  display: flex;
  align-items: center;
  justify-content: center;
}
.metric-icon-box.purple {
  background: rgba(157, 114, 255, 0.1);
  color: var(--primary-purple);
}
.metric-icon-box.cyan {
  background: rgba(56, 189, 248, 0.1);
  color: #38bdf8;
}
.metric-icon-box.green {
  background: rgba(16, 185, 129, 0.1);
  color: var(--status-green);
}
.metric-icon-box svg {
  width: 14px;
  height: 14px;
}

.metric-value-row {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.metric-num {
  font-size: 20px;
  font-weight: 700;
  color: #fff;
}

.metric-trend {
  font-size: 10px;
  color: var(--status-green);
  font-weight: 600;
}

.metric-dim {
  font-size: 10px;
  color: var(--text-dim);
  font-family: var(--font-mono);
}

.metric-tag-synced {
  font-size: 9px;
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  padding: 1px 6px;
  border-radius: 4px;
  font-weight: 700;
}

/* Ingestion Grid */
.pipeline-grid {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 16px;
}

.pipeline-card {
  background: rgba(13, 21, 39, 0.6);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.pipeline-card-header {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-title-group {
  display: flex;
  align-items: center;
  gap: 8px;
}
.card-title-group svg {
  width: 15px;
  height: 15px;
  color: var(--primary-cyan);
}
.card-title-group h4 {
  font-size: 12px;
  font-weight: 700;
  color: #fff;
}

.status-ready-tag {
  font-size: 9px;
  background: rgba(0, 229, 255, 0.1);
  color: var(--primary-cyan);
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 700;
  border: 1px solid rgba(0, 229, 255, 0.25);
}

.running-count {
  font-size: 9px;
  background: rgba(56, 189, 248, 0.15);
  color: #38bdf8;
  padding: 1px 6px;
  border-radius: 4px;
  font-weight: 700;
}

.worker-pool-tag {
  font-size: 10px;
  color: var(--status-green);
  font-weight: 600;
}

.dropzone-area {
  padding: 28px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.drop-icon-circle {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(0, 229, 255, 0.08);
  border: 1px dashed rgba(0, 229, 255, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-cyan);
  margin-bottom: 10px;
}
.drop-icon-circle svg {
  width: 22px;
  height: 22px;
}

.drop-title {
  font-size: 12px;
  font-weight: 600;
  color: #fff;
}

.drop-sub {
  font-size: 10px;
  color: var(--text-dim);
  margin-top: 2px;
}
.browse-link {
  color: var(--primary-cyan);
  text-decoration: underline;
}

.format-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  justify-content: center;
  margin-top: 14px;
}

.fmt {
  font-size: 9px;
  font-weight: 700;
  background: #1e293b;
  border: 1px solid #334155;
  padding: 3px 8px;
  border-radius: 5px;
  color: #ffffff !important;
  letter-spacing: 0.5px;
}
.fmt.active-fmt {
  background: #0284c7;
  border-color: #38bdf8;
  color: #ffffff !important;
}

/* Active Jobs */
.active-jobs-list {
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.job-item {
  background: rgba(10, 16, 31, 0.8);
  border: 1px solid rgba(23, 36, 60, 0.8);
  border-radius: 6px;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.job-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.job-file {
  display: flex;
  align-items: center;
  gap: 8px;
}

.file-icon {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.file-icon.red { background: rgba(239, 68, 68, 0.15); color: #f87171; }
.file-icon.blue { background: rgba(56, 189, 248, 0.15); color: #38bdf8; }
.file-icon svg { width: 14px; height: 14px; }

.file-name {
  font-size: 11px;
  color: #fff;
  display: block;
}

.file-detail {
  font-size: 9px;
  color: var(--text-dim);
}

.job-pct {
  text-align: right;
}

.pct-num {
  font-size: 12px;
  font-weight: 700;
  color: var(--primary-cyan);
  display: block;
}
.pct-num.green-text { color: #34d399; }

.chunks-info {
  font-size: 9px;
  color: var(--text-dim);
}

.progress-bar-bg {
  height: 4px;
  background: rgba(23, 36, 60, 0.9);
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #00e5ff, #38bdf8);
  border-radius: 2px;
}
.progress-bar-fill.green-fill {
  background: #10b981;
}

.job-status-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 9px;
  color: var(--text-dim);
}

.eta-text {
  font-family: var(--font-mono);
  color: var(--text-muted);
}

/* Data Table */
.table-card {
  background: rgba(13, 21, 39, 0.6);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden;
}

.table-filter-bar {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.search-input-box {
  position: relative;
  display: flex;
  align-items: center;
  width: 380px;
}
.search-input-box svg {
  position: absolute;
  left: 10px;
  width: 14px;
  height: 14px;
  color: var(--text-dim);
}
.search-input-box input {
  width: 100%;
  background: rgba(10, 16, 31, 0.8);
  border: 1px solid rgba(23, 36, 60, 0.8);
  border-radius: 6px;
  padding: 6px 10px 6px 30px;
  color: #fff;
  font-size: 11px;
  outline: none;
}
.search-input-box input:focus {
  border-color: var(--primary-cyan);
}

.filter-dropdowns {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-select {
  background: rgba(10, 16, 31, 0.8);
  border: 1px solid rgba(23, 36, 60, 0.8);
  border-radius: 6px;
  color: var(--text-muted);
  font-size: 10px;
  padding: 6px 10px;
  outline: none;
}

.showing-text {
  font-size: 9px;
  font-weight: 700;
  color: var(--text-dim);
  letter-spacing: 0.5px;
}

.export-btn {
  background: transparent;
  border: 1px solid rgba(23, 36, 60, 0.8);
  border-radius: 6px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  cursor: pointer;
}
.export-btn svg { width: 13px; height: 13px; }

.table-responsive {
  overflow-x: auto;
}

.docs-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 11px;
  text-align: left;
}

.docs-table th {
  padding: 10px 16px;
  font-size: 9px;
  font-weight: 700;
  color: var(--text-dim);
  border-bottom: 1px solid var(--border-color);
  letter-spacing: 0.8px;
}

.docs-table td {
  padding: 12px 16px;
  border-bottom: 1px solid rgba(23, 36, 60, 0.4);
}

.doc-title-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.doc-code-icon {
  font-size: 8px;
  font-weight: 700;
  background: rgba(0, 229, 255, 0.1);
  color: var(--primary-cyan);
  padding: 3px 5px;
  border-radius: 4px;
  font-family: var(--font-mono);
}

.doc-name {
  color: #fff;
  font-weight: 600;
  display: block;
}

.doc-hash {
  font-size: 9px;
  color: var(--text-dim);
  font-family: var(--font-mono);
}

.mono-col {
  font-family: var(--font-mono);
  color: var(--text-muted);
}

.model-pill {
  background: rgba(13, 21, 39, 0.8);
  border: 1px solid rgba(23, 36, 60, 0.8);
  border-radius: 4px;
  padding: 2px 6px;
  font-size: 10px;
  font-family: var(--font-mono);
  color: #94a3b8;
}

.agent-pill {
  color: #c084fc;
  font-weight: 500;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 10px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
}
.status-badge.indexed {
  background: rgba(16, 185, 129, 0.12);
  color: #34d399;
}
.status-badge svg { width: 10px; height: 10px; }

.text-right {
  text-align: right;
}

.action-buttons {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-inspect {
  background: transparent;
  border: 1px solid rgba(0, 229, 255, 0.3);
  color: var(--primary-cyan);
  font-size: 10px;
  padding: 3px 8px;
  border-radius: 4px;
  cursor: pointer;
}
.btn-inspect:hover {
  background: rgba(0, 229, 255, 0.1);
}

.btn-icon-action {
  background: transparent;
  border: none;
  color: var(--text-dim);
  cursor: pointer;
  padding: 4px;
}
.btn-icon-action:hover {
  color: #fff;
}
.btn-icon-action svg { width: 13px; height: 13px; }
</style>
