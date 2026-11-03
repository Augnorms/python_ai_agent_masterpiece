<template>
  <div class="scada-container">
    <!-- Top SCADA Plant Header Ribbon -->
    <div class="scada-header-ribbon">
      <div class="ribbon-brand-section">
        <div class="brand-droplet-badge">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z" fill="#00e5ff" stroke="#00e5ff" />
          </svg>
        </div>
        <div class="brand-titles">
          <span class="brand-primary">AQUASYNC SCADA</span>
          <span class="brand-sub">SWRO PLANT #04</span>
        </div>
      </div>

      <!-- Top Network Status Indicators -->
      <div class="ribbon-center-cluster">
        <div class="status-box">
          <div class="status-top">
            <span class="dot-online"></span>
            <span class="status-name">OPC-UA:</span>
            <span class="status-state">ONLINE (3ms)</span>
          </div>
        </div>

        <div class="status-box active-modbus">
          <div class="status-top">
            <span class="dot-online"></span>
            <span class="status-name">MODBUS TCP:</span>
            <span class="status-state highlight">SLAVE #01 OK</span>
          </div>
        </div>

        <div class="alarm-banner-box">
          <span class="alarm-banner-label">ACTIVE ALARM BANNER</span>
          <div class="alarm-banner-text">
            <span class="dot-online"></span>
            <span class="alarm-msg">SYS NORMAL - ALL STAGES WITHIN PERMISSIBLE THRESHOLDS</span>
          </div>
        </div>
      </div>

      <!-- Mode Toggles, E-Stop and Profile -->
      <div class="ribbon-right-cluster">
        <div class="mode-toggle-group">
          <button 
            type="button" 
            class="mode-btn" 
            :class="{ active: currentMode === 'AUTO' }" 
            @click="currentMode = 'AUTO'"
          >
            AUTO
          </button>
          <button 
            type="button" 
            class="mode-btn" 
            :class="{ active: currentMode === 'MANUAL' }" 
            @click="currentMode = 'MANUAL'"
          >
            MANUAL
          </button>
          <button 
            type="button" 
            class="mode-btn" 
            :class="{ active: currentMode === 'SIM' }" 
            @click="currentMode = 'SIM'"
          >
            SIM
          </button>
        </div>

        <button 
          type="button" 
          class="btn-estop-armed" 
          :class="{ triggered: eStopTriggered }"
          @click="toggleEStop"
          title="Emergency Stop"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
          <div class="estop-labels">
            <span class="estop-main">E-STOP:</span>
            <span class="estop-sub">{{ eStopTriggered ? 'TRIGGERED' : 'ARMED' }}</span>
          </div>
        </button>

        <div class="profile-avatar-btn" title="SCADA Operator: Eng. Kwame Mensah">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
        </div>
      </div>
    </div>

    <!-- Main Scrollable Content -->
    <div class="scada-content">
      <!-- Modbus TCP Connection & Status Ribbon -->
      <div class="modbus-conn-ribbon">
        <div class="conn-left-items">
          <div class="conn-badge">
            <span class="pulsing-green-dot"></span>
            <span class="conn-title font-mono">MODBUS TCP: CONNECTED (192.168.1.105:502)</span>
          </div>

          <div class="conn-meta-item">
            <span class="meta-label">SLAVE ID:</span>
            <span class="meta-value font-mono">#01 (SWRO-PLC-RACK)</span>
          </div>

          <div class="conn-meta-item">
            <span class="meta-label">POLL RATE:</span>
            <span class="meta-value font-mono cyan-text">{{ pollRate }} ms</span>
          </div>

          <div class="conn-meta-item">
            <span class="meta-label">JITTER:</span>
            <span class="meta-value font-mono cyan-text">{{ jitter.toFixed(1) }} ms</span>
          </div>
        </div>

        <div class="conn-right-items">
          <div class="conn-meta-item">
            <span class="meta-label">CRC ERRORS:</span>
            <span class="meta-value font-mono green-text">0 (0.00%)</span>
          </div>

          <div class="conn-meta-item watchdog-item">
            <span class="meta-label">WATCHDOG:</span>
            <span class="watchdog-pill">
              <span class="small-green-dot"></span>
              ACTIVE
            </span>
          </div>

          <button type="button" class="btn-tool-export" @click="exportRegistersCsv">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="7 10 12 15 17 10" />
              <line x1="12" y1="15" x2="12" y2="3" />
            </svg>
            <span>EXPORT CSV</span>
          </button>

          <button type="button" class="btn-tool-pcap" @click="showPcapModal = true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
              <line x1="8" y1="21" x2="16" y2="21" />
              <line x1="12" y1="17" x2="12" y2="21" />
            </svg>
            <span>PCAP TRACE</span>
          </button>
        </div>
      </div>

      <!-- 6 Network Protocol KPI Cards -->
      <div class="kpi-metrics-grid">
        <!-- 1. Total Frames -->
        <div class="metric-card">
          <div class="metric-title">TOTAL FRAMES TX/RX</div>
          <div class="metric-value font-mono">{{ totalFrames.toLocaleString() }}</div>
          <div class="metric-subtext green-text font-mono">0 PACKET DROPS</div>
        </div>

        <!-- 2. Mean Latency -->
        <div class="metric-card">
          <div class="metric-title">MEAN LATENCY</div>
          <div class="metric-value cyan-text font-mono">{{ meanLatency.toFixed(2) }} ms</div>
          <div class="metric-subtext dim-text font-mono">σ = 0.38 ms</div>
        </div>

        <!-- 3. FC03 Read Holding -->
        <div class="metric-card">
          <div class="metric-title">FC03 (READ HOLDING)</div>
          <div class="metric-value cyan-blue-text font-mono">92.4%</div>
          <div class="metric-subtext dim-cyan-text font-mono">{{ fc03Requests.toLocaleString() }} REQS</div>
        </div>

        <!-- 4. FC06 / FC16 Writes -->
        <div class="metric-card">
          <div class="metric-title">FC06 / FC16 (WRITES)</div>
          <div class="metric-value purple-text font-mono">7.6%</div>
          <div class="metric-subtext dim-purple-text font-mono">{{ fcWrites.toLocaleString() }} COMMANDS</div>
        </div>

        <!-- 5. Exception Responses -->
        <div class="metric-card">
          <div class="metric-title">EXCEPTION RESPONSES</div>
          <div class="metric-value green-text font-mono">0</div>
          <div class="metric-subtext dim-text font-mono">LAST: 72H CLEAN</div>
        </div>

        <!-- 6. Socket Buffer Usage -->
        <div class="metric-card">
          <div class="metric-title">SOCKET BUFFER USAGE</div>
          <div class="metric-value cyan-text font-mono">14.2%</div>
          <div class="metric-subtext dim-text font-mono">64 KB TCP WINDOW</div>
        </div>
      </div>

      <!-- Main Modbus Register Mapping & Live Polling Table Panel -->
      <section class="scada-table-panel">
        <div class="table-panel-header">
          <div class="table-title-box">
            <div class="table-icon-badge">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" />
                <path d="M3 9h18M3 15h18M9 3v18M15 3v18" />
              </svg>
            </div>
            <div>
              <h3 class="table-title">MODBUS REGISTER MAPPING & LIVE POLLING TABLE</h3>
              <p class="table-sub-info font-mono">
                Holding Registers (40001 - 40024) | Input Registers (30001 - 30016) | Coils (00001 - 00008)
              </p>
            </div>
          </div>

          <!-- Quick Search Filter -->
          <div class="table-search-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Filter by Tag, Address or Unit..." 
              class="search-input font-mono"
            />
          </div>
        </div>

        <!-- Filter Segmented Tabs Bar -->
        <div class="table-tabs-bar">
          <div class="tab-pill-group">
            <button 
              type="button" 
              class="tab-pill" 
              :class="{ active: activeFilter === 'ALL' }" 
              @click="activeFilter = 'ALL'"
            >
              ALL REGISTERS
            </button>
            <button 
              type="button" 
              class="tab-pill" 
              :class="{ active: activeFilter === 'HOLDING' }" 
              @click="activeFilter = 'HOLDING'"
            >
              HOLDING (4x)
            </button>
            <button 
              type="button" 
              class="tab-pill" 
              :class="{ active: activeFilter === 'INPUT' }" 
              @click="activeFilter = 'INPUT'"
            >
              INPUT (3x)
            </button>
            <button 
              type="button" 
              class="tab-pill" 
              :class="{ active: activeFilter === 'COILS' }" 
              @click="activeFilter = 'COILS'"
            >
              COILS (0x)
            </button>
          </div>

          <div class="table-live-indicator">
            <span class="pulsing-green-dot"></span>
            <span class="indicator-text font-mono">CYCLE SCAN: {{ scanCycleClock }}</span>
          </div>
        </div>

        <!-- The SCADA Modbus Polling Table -->
        <div class="table-responsive-wrapper">
          <table class="modbus-table">
            <thead>
              <tr>
                <th class="col-addr">MODBUS ADDR</th>
                <th class="col-tag">PLC TAG / VARIABLE NAME</th>
                <th class="col-dtype">DATA TYPE</th>
                <th class="col-raw">RAW HEX / INT</th>
                <th class="col-scaled">SCALED VALUE</th>
                <th class="col-units">ENG. UNITS</th>
                <th class="col-scan">SCAN TIME</th>
                <th class="col-health">HEALTH</th>
                <th class="col-action">OVERRIDE</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="reg in filteredRegisters" 
                :key="reg.address"
                :class="{ 'row-flashing': reg.isUpdated, 'row-coil': reg.category === 'COIL' }"
              >
                <!-- 1. Modbus Address -->
                <td class="col-addr font-mono addr-cell">{{ reg.address }}</td>

                <!-- 2. PLC Tag / Variable Name -->
                <td class="col-tag font-sans tag-cell">
                  <div class="tag-flex">
                    <span class="tag-name">{{ reg.name }}</span>
                    <span v-if="reg.identifier" class="tag-identifier font-mono">{{ reg.identifier }}</span>
                  </div>
                </td>

                <!-- 3. Data Type -->
                <td class="col-dtype font-mono dtype-cell">{{ reg.dataType }}</td>

                <!-- 4. Raw Hex / Int -->
                <td class="col-raw font-mono raw-cell">{{ reg.rawHex }}</td>

                <!-- 5. Scaled Value -->
                <td class="col-scaled font-mono scaled-cell">
                  <span 
                    class="scaled-badge" 
                    :class="{ 
                      'cyan-val': typeof reg.scaledValue === 'number', 
                      'bool-true': reg.scaledValue === 'TRUE',
                      'bool-false': reg.scaledValue === 'FALSE' 
                    }"
                  >
                    {{ formatScaledValue(reg.scaledValue) }}
                  </span>
                </td>

                <!-- 6. Engineering Units -->
                <td class="col-units font-mono units-cell">{{ reg.units }}</td>

                <!-- 7. Scan Time -->
                <td class="col-scan font-mono scan-cell green-text">{{ reg.scanTime }}</td>

                <!-- 8. Health Status -->
                <td class="col-health health-cell">
                  <div class="health-badge" :class="reg.health === 'ACTIVE' ? 'health-active' : 'health-good'">
                    <span class="health-dot"></span>
                    <span class="health-label font-mono">{{ reg.health }}</span>
                  </div>
                </td>

                <!-- 9. Override Action Button -->
                <td class="col-action action-cell">
                  <button 
                    v-if="reg.category === 'HOLDING'" 
                    type="button" 
                    class="btn-table-action btn-write font-mono"
                    @click="openWriteModal(reg)"
                  >
                    WRITE
                  </button>

                  <button 
                    v-else-if="reg.category === 'COIL'" 
                    type="button" 
                    class="btn-table-action btn-force font-mono"
                    :class="{ 'btn-force-active': reg.scaledValue === 'TRUE' }"
                    @click="toggleCoil(reg)"
                  >
                    FORCE
                  </button>

                  <span v-else class="read-only-tag font-mono">READ ONLY</span>
                </td>
              </tr>

              <tr v-if="filteredRegisters.length === 0">
                <td colspan="9" class="no-records-cell font-mono">
                  No Modbus registers matched search query: "{{ searchQuery }}"
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>

    <!-- Modal 1: Write Modbus Holding Register Modal -->
    <div v-if="showWriteModal && selectedRegister" class="modal-overlay" @click.self="showWriteModal = false">
      <div class="modal-card">
        <div class="modal-header">
          <div class="modal-title-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="modal-icon">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
            </svg>
            <div>
              <h3>FC06 Modbus Register Write</h3>
              <p class="modal-sub font-mono">Target: [{{ selectedRegister.address }}] {{ selectedRegister.name }}</p>
            </div>
          </div>
          <button class="modal-close-btn" @click="showWriteModal = false">&times;</button>
        </div>

        <div class="modal-body">
          <div class="write-meta-grid font-mono">
            <div class="meta-box">
              <span class="m-label">SLAVE ADDRESS:</span>
              <span class="m-val cyan-text">#01 (192.168.1.105:502)</span>
            </div>
            <div class="meta-box">
              <span class="m-label">REGISTER ADDR:</span>
              <span class="m-val font-bold">{{ selectedRegister.address }}</span>
            </div>
            <div class="meta-box">
              <span class="m-label">DATA FORMAT:</span>
              <span class="m-val">{{ selectedRegister.dataType }}</span>
            </div>
            <div class="meta-box">
              <span class="m-label">CURRENT VALUE:</span>
              <span class="m-val green-text font-bold">{{ selectedRegister.scaledValue }} {{ selectedRegister.units }}</span>
            </div>
          </div>

          <div class="form-group-write">
            <label class="input-label">New Scaled Value ({{ selectedRegister.units }})</label>
            <div class="input-inline-wrap">
              <input 
                v-model="newScaledInput" 
                type="number" 
                step="any"
                class="write-input font-mono" 
                placeholder="Enter new value..."
                @input="calculateRawHexPreview"
              />
              <span class="unit-suffix font-mono">{{ selectedRegister.units }}</span>
            </div>
            <div class="calc-hex-preview font-mono">
              <span>Calculated Raw INT: <strong>{{ calculatedRawInt }}</strong></span>
              <span>Calculated Hex: <strong class="cyan-text">{{ calculatedRawHex }}</strong></span>
            </div>
          </div>

          <div v-if="writeSuccessMsg" class="success-alert font-mono">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="20 6 9 17 4 12" />
            </svg>
            <span>{{ writeSuccessMsg }}</span>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn-cancel font-mono" @click="showWriteModal = false">Cancel</button>
          <button type="button" class="btn-send-write font-mono" @click="executeRegisterWrite">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="5 3 19 12 5 21 5 3" />
            </svg>
            TRANSMIT FC06 WRITE
          </button>
        </div>
      </div>
    </div>

    <!-- Modal 2: PCAP Packet Trace Modal -->
    <div v-if="showPcapModal" class="modal-overlay" @click.self="showPcapModal = false">
      <div class="modal-card pcap-card">
        <div class="modal-header">
          <div class="modal-title-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="modal-icon cyan-text">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
              <line x1="8" y1="21" x2="16" y2="21" />
              <line x1="12" y1="17" x2="12" y2="21" />
            </svg>
            <div>
              <h3>Modbus TCP Live Packet Sniffer / PCAP Stream</h3>
              <p class="modal-sub font-mono">Capture buffer: 192.168.1.105:502 (Slave #01)</p>
            </div>
          </div>
          <button class="modal-close-btn" @click="showPcapModal = false">&times;</button>
        </div>

        <div class="modal-body pcap-body font-mono">
          <div class="pcap-log-list">
            <div 
              v-for="(pkt, idx) in pcapPackets" 
              :key="idx" 
              class="pcap-row" 
              :class="pkt.dir === 'TX' ? 'pcap-tx' : 'pcap-rx'"
            >
              <span class="pcap-time">{{ pkt.time }}</span>
              <span class="pcap-dir-badge" :class="pkt.dir === 'TX' ? 'badge-tx' : 'badge-rx'">{{ pkt.dir }}</span>
              <span class="pcap-fc">{{ pkt.fc }}</span>
              <span class="pcap-desc">{{ pkt.desc }}</span>
              <span class="pcap-hex">{{ pkt.hex }}</span>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn-cancel font-mono" @click="pcapPackets = []">Clear Stream</button>
          <button type="button" class="btn-primary font-mono" @click="showPcapModal = false">Close Monitor</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// Top Bar States
const currentMode = ref('AUTO')
const eStopTriggered = ref(false)

const toggleEStop = () => {
  eStopTriggered.value = !eStopTriggered.value
}

// Connection Metrics
const pollRate = ref(50)
const jitter = ref(1.2)
const totalFrames = ref(1842910)
const meanLatency = ref(2.41)
const fc03Requests = ref(1702848)
const fcWrites = ref(140062)
const scanCycleClock = ref('14:48:22.050')

// Filters and Search
const activeFilter = ref('ALL')
const searchQuery = ref('')

// Modals
const showWriteModal = ref(false)
const showPcapModal = ref(false)
const selectedRegister = ref(null)
const newScaledInput = ref('')
const calculatedRawInt = ref(0)
const calculatedRawHex = ref('0x0000')
const writeSuccessMsg = ref('')

// Modbus Register Mapping Table Dataset (Exact from user's screen + extended for tabs)
const registers = ref([
  {
    address: '40001',
    category: 'HOLDING',
    name: 'Feed Pressure (PT-202)',
    identifier: '',
    dataType: 'INT16 (x10)',
    scaleFactor: 10,
    rawInt: 48,
    rawHex: '0x0030 (48)',
    scaledValue: 4.8,
    units: 'bar',
    scanTime: '50 ms',
    health: 'GOOD',
    isUpdated: false
  },
  {
    address: '40002',
    category: 'HOLDING',
    name: 'Pump P-101 Current (CT-101)',
    identifier: '',
    dataType: 'INT16 (x10)',
    scaleFactor: 10,
    rawInt: 245,
    rawHex: '0x00F5 (245)',
    scaledValue: 24.5,
    units: 'A',
    scanTime: '50 ms',
    health: 'GOOD',
    isUpdated: false
  },
  {
    address: '40003',
    category: 'HOLDING',
    name: 'Suction Temperature (TT-101)',
    identifier: '',
    dataType: 'INT16 (x10)',
    scaleFactor: 10,
    rawInt: 260,
    rawHex: '0x0104 (260)',
    scaledValue: 26.0,
    units: '°C',
    scanTime: '50 ms',
    health: 'GOOD',
    isUpdated: false
  },
  {
    address: '40004',
    category: 'HOLDING',
    name: 'Permeate Conductivity (AT-301)',
    identifier: '',
    dataType: 'INT16 (x1)',
    scaleFactor: 1,
    rawInt: 1278,
    rawHex: '0x04FE (1278)',
    scaledValue: 1278,
    units: 'µS/cm',
    scanTime: '50 ms',
    health: 'GOOD',
    isUpdated: false
  },
  {
    address: '40005',
    category: 'HOLDING',
    name: 'Permeate TDS Sensor A (TDS-401)',
    identifier: '',
    dataType: 'INT16 (x1)',
    scaleFactor: 1,
    rawInt: 818,
    rawHex: '0x0332 (818)',
    scaledValue: 818,
    units: 'ppm',
    scanTime: '50 ms',
    health: 'GOOD',
    isUpdated: false
  },
  {
    address: '40006',
    category: 'HOLDING',
    name: 'Tank Level TK-201 (LT-201)',
    identifier: '',
    dataType: 'INT16 (x1)',
    scaleFactor: 1,
    rawInt: 30,
    rawHex: '0x001E (30)',
    scaledValue: 30,
    units: '%',
    scanTime: '50 ms',
    health: 'GOOD',
    isUpdated: false
  },
  {
    address: '40007',
    category: 'HOLDING',
    name: 'Membrane DP Filter (DPT-301)',
    identifier: '',
    dataType: 'INT16 (x100)',
    scaleFactor: 100,
    rawInt: 18,
    rawHex: '0x0012 (18)',
    scaledValue: 0.18,
    units: 'bar',
    scanTime: '50 ms',
    health: 'GOOD',
    isUpdated: false
  },
  {
    address: '30001',
    category: 'INPUT',
    name: 'Raw Sea Water Inflow (FIT-101)',
    identifier: '',
    dataType: 'INT16 (x10)',
    scaleFactor: 10,
    rawInt: 745,
    rawHex: '0x02E9 (745)',
    scaledValue: 74.5,
    units: 'm³/h',
    scanTime: '50 ms',
    health: 'GOOD',
    isUpdated: false
  },
  {
    address: '30002',
    category: 'INPUT',
    name: 'Feed ORP Potential (AT-202)',
    identifier: '',
    dataType: 'INT16 (x1)',
    scaleFactor: 1,
    rawInt: 300,
    rawHex: '0x012C (300)',
    scaledValue: 300,
    units: 'mV',
    scanTime: '50 ms',
    health: 'GOOD',
    isUpdated: false
  },
  {
    address: '30003',
    category: 'INPUT',
    name: 'High-Pressure Stage 1 (PT-301)',
    identifier: '',
    dataType: 'INT16 (x10)',
    scaleFactor: 10,
    rawInt: 580,
    rawHex: '0x0244 (580)',
    scaledValue: 58.0,
    units: 'bar',
    scanTime: '50 ms',
    health: 'GOOD',
    isUpdated: false
  },
  {
    address: '00001',
    category: 'COIL',
    name: 'Pump P-101 Run Command',
    identifier: '',
    dataType: 'COIL (BIT)',
    scaleFactor: 1,
    rawInt: 1,
    rawHex: '0x01 (1)',
    scaledValue: 'TRUE',
    units: 'BOOL',
    scanTime: '20 ms',
    health: 'ACTIVE',
    isUpdated: false
  },
  {
    address: '00002',
    category: 'COIL',
    name: 'Pump P-202 HP Run Command',
    identifier: '',
    dataType: 'COIL (BIT)',
    scaleFactor: 1,
    rawInt: 1,
    rawHex: '0x01 (1)',
    scaledValue: 'TRUE',
    units: 'BOOL',
    scanTime: '20 ms',
    health: 'ACTIVE',
    isUpdated: false
  },
  {
    address: '00003',
    category: 'COIL',
    name: 'Chemical Dosing Pump DP-101',
    identifier: '',
    dataType: 'COIL (BIT)',
    scaleFactor: 1,
    rawInt: 1,
    rawHex: '0x01 (1)',
    scaledValue: 'TRUE',
    units: 'BOOL',
    scanTime: '20 ms',
    health: 'ACTIVE',
    isUpdated: false
  },
  {
    address: '00004',
    category: 'COIL',
    name: 'RO Flush Valve SV-401',
    identifier: '',
    dataType: 'COIL (BIT)',
    scaleFactor: 1,
    rawInt: 0,
    rawHex: '0x00 (0)',
    scaledValue: 'FALSE',
    units: 'BOOL',
    scanTime: '20 ms',
    health: 'ACTIVE',
    isUpdated: false
  }
])

// PCAP Sample Frames Stream
const pcapPackets = ref([
  { time: '14:48:21.840', dir: 'TX', fc: 'FC03', desc: 'Read Holding Regs [40001 - 40007]', hex: '00 01 00 00 00 06 01 03 9C 41 00 07' },
  { time: '14:48:21.842', dir: 'RX', fc: 'FC03', desc: 'Read Holding Response (14 bytes)', hex: '00 01 00 00 00 11 01 03 0E 00 30 00 F5 01 04 04 FE 03 32 00 1E 00 12' },
  { time: '14:48:21.890', dir: 'TX', fc: 'FC01', desc: 'Read Coils [00001 - 00004]', hex: '00 02 00 00 00 06 01 01 00 01 00 04' },
  { time: '14:48:21.893', dir: 'RX', fc: 'FC01', desc: 'Read Coils Response (1 byte: 0x07)', hex: '00 02 00 00 00 04 01 01 01 07' },
  { time: '14:48:21.940', dir: 'TX', fc: 'FC04', desc: 'Read Input Regs [30001 - 30003]', hex: '00 03 00 00 00 06 01 04 75 31 00 03' },
  { time: '14:48:21.943', dir: 'RX', fc: 'FC04', desc: 'Read Input Response (6 bytes)', hex: '00 03 00 00 00 09 01 04 06 02 E9 01 2C 02 44' }
])

// Format Display for Numbers and Booleans
const formatScaledValue = (val) => {
  if (typeof val === 'number') {
    return val >= 1000 ? val.toLocaleString() : val
  }
  return val
}

// Filtered Registers Computed
const filteredRegisters = computed(() => {
  return registers.value.filter((reg) => {
    // 1. Tab filter
    if (activeFilter.value === 'HOLDING' && reg.category !== 'HOLDING') return false
    if (activeFilter.value === 'INPUT' && reg.category !== 'INPUT') return false
    if (activeFilter.value === 'COILS' && reg.category !== 'COIL') return false

    // 2. Search query filter
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase()
      const matchesAddr = reg.address.toLowerCase().includes(q)
      const matchesName = reg.name.toLowerCase().includes(q)
      const matchesUnits = reg.units.toLowerCase().includes(q)
      const matchesType = reg.dataType.toLowerCase().includes(q)
      if (!matchesAddr && !matchesName && !matchesUnits && !matchesType) return false
    }

    return true
  })
})

// Open Modal to Write Holding Register
const openWriteModal = (reg) => {
  selectedRegister.value = reg
  newScaledInput.value = String(reg.scaledValue)
  writeSuccessMsg.value = ''
  calculateRawHexPreview()
  showWriteModal.value = true
}

// Live calculation of Raw Hex when typing in Write modal
const calculateRawHexPreview = () => {
  if (!selectedRegister.value) return
  const num = parseFloat(newScaledInput.value) || 0
  const raw = Math.round(num * selectedRegister.value.scaleFactor)
  calculatedRawInt.value = raw
  const hex = (raw & 0xffff).toString(16).toUpperCase().padStart(4, '0')
  calculatedRawHex.value = `0x${hex} (${raw})`
}

// Execute Register Write (FC06 Single Register Write)
const executeRegisterWrite = () => {
  if (!selectedRegister.value) return
  const num = parseFloat(newScaledInput.value)
  if (isNaN(num)) return

  selectedRegister.value.scaledValue = num
  selectedRegister.value.rawInt = calculatedRawInt.value
  selectedRegister.value.rawHex = calculatedRawHex.value
  selectedRegister.value.isUpdated = true

  fcWrites.value++
  totalFrames.value += 2

  // Add packet trace
  const now = new Date()
  const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}.${String(now.getMilliseconds()).padStart(3, '0')}`
  pcapPackets.value.unshift({
    time: timeStr,
    dir: 'TX',
    fc: 'FC06',
    desc: `Write Single Reg [${selectedRegister.value.address}] -> ${num}`,
    hex: `00 FF 00 00 00 06 01 06 ${selectedRegister.value.address.slice(1)} ${calculatedRawHex.value.slice(2, 6)}`
  })

  writeSuccessMsg.value = `FC06 Write dispatched successfully: [${selectedRegister.value.address}] = ${num} ${selectedRegister.value.units}`

  setTimeout(() => {
    if (selectedRegister.value) selectedRegister.value.isUpdated = false
  }, 1800)

  setTimeout(() => {
    showWriteModal.value = false
  }, 1200)
}

// Toggle / Force Coil State
const toggleCoil = (coil) => {
  const isCurrentlyTrue = coil.scaledValue === 'TRUE'
  coil.scaledValue = isCurrentlyTrue ? 'FALSE' : 'TRUE'
  coil.rawInt = isCurrentlyTrue ? 0 : 1
  coil.rawHex = isCurrentlyTrue ? '0x00 (0)' : '0x01 (1)'
  coil.isUpdated = true

  fcWrites.value++
  totalFrames.value += 2

  const now = new Date()
  const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}.${String(now.getMilliseconds()).padStart(3, '0')}`
  pcapPackets.value.unshift({
    time: timeStr,
    dir: 'TX',
    fc: 'FC05',
    desc: `Force Coil [${coil.address}] -> ${coil.scaledValue}`,
    hex: `00 FE 00 00 00 06 01 05 ${coil.address.slice(1)} ${isCurrentlyTrue ? '00 00' : 'FF 00'}`
  })

  setTimeout(() => {
    coil.isUpdated = false
  }, 1500)
}

// Export Registers as CSV
const exportRegistersCsv = () => {
  let csv = 'MODBUS_ADDR,TAG_NAME,DATA_TYPE,RAW_VALUE,SCALED_VALUE,ENG_UNITS,SCAN_TIME,HEALTH\n'
  registers.value.forEach((r) => {
    csv += `"${r.address}","${r.name}","${r.dataType}","${r.rawHex}","${r.scaledValue}","${r.units}","${r.scanTime}","${r.health}"\n`
  })

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.setAttribute('href', url)
  link.setAttribute('download', `modbus_tcp_registers_slave01_${Date.now()}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// Live Polling Simulation Engine
let pollTimer = null

const tickLivePolling = () => {
  const now = new Date()
  const hh = String(now.getHours()).padStart(2, '0')
  const mm = String(now.getMinutes()).padStart(2, '0')
  const ss = String(now.getSeconds()).padStart(2, '0')
  const ms = String(now.getMilliseconds()).padStart(3, '0')
  scanCycleClock.value = `${hh}:${mm}:${ss}.${ms}`

  // Increment live polling metrics
  totalFrames.value += 20 // 20 frames per sec @ 50ms poll rate
  fc03Requests.value += 18
  jitter.value = 1.1 + (Math.sin(now.getTime() / 2500) * 0.25)
  meanLatency.value = 2.41 + (Math.cos(now.getTime() / 3200) * 0.06)

  // Subtle realistic sensor drift on Feed Pressure and Temperature
  if (!eStopTriggered.value) {
    const feedP = registers.value.find((r) => r.address === '40001')
    if (feedP && !feedP.isUpdated) {
      const delta = (Math.sin(now.getTime() / 4000) * 0.08)
      feedP.scaledValue = parseFloat((4.8 + delta).toFixed(1))
      feedP.rawInt = Math.round(feedP.scaledValue * 10)
      feedP.rawHex = `0x00${feedP.rawInt.toString(16).toUpperCase()} (${feedP.rawInt})`
    }

    const tempReg = registers.value.find((r) => r.address === '40003')
    if (tempReg && !tempReg.isUpdated) {
      const deltaT = (Math.cos(now.getTime() / 6000) * 0.1)
      tempReg.scaledValue = parseFloat((26.0 + deltaT).toFixed(1))
      tempReg.rawInt = Math.round(tempReg.scaledValue * 10)
      tempReg.rawHex = `0x01${(tempReg.rawInt - 256).toString(16).toUpperCase().padStart(2, '0')} (${tempReg.rawInt})`
    }
  }
}

onMounted(() => {
  pollTimer = setInterval(tickLivePolling, 1000)
})

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
})
</script>

<style scoped>
/* Main Container */
.scada-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  background: var(--bg-app, #060b17);
  color: var(--text-main, #f1f5f9);
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.font-mono {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
}

/* 1. Top SCADA Plant Header Ribbon */
.scada-header-ribbon {
  height: 48px;
  background: var(--bg-card, #091224);
  border-bottom: 1px solid var(--border-color, #142442);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  gap: 12px;
  flex-shrink: 0;
}

.ribbon-brand-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-droplet-badge {
  width: 28px;
  height: 28px;
  background: rgba(0, 229, 255, 0.12);
  border: 1px solid rgba(0, 229, 255, 0.35);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-droplet-badge svg {
  width: 16px;
  height: 16px;
}

.brand-titles {
  display: flex;
  flex-direction: column;
}

.brand-primary {
  font-size: 11.5px;
  font-weight: 800;
  letter-spacing: 0.5px;
  color: #ffffff;
}

.brand-sub {
  font-size: 9.5px;
  font-weight: 600;
  letter-spacing: 0.8px;
  color: #64748b;
}

/* Center Cluster */
.ribbon-center-cluster {
  display: flex;
  align-items: center;
  gap: 14px;
}

.status-box {
  background: var(--bg-card-inner, #0c1830);
  border: 1px solid var(--border-color, #172c54);
  border-radius: 4px;
  padding: 4px 9px;
  font-size: 10.5px;
  font-weight: 600;
}

.status-box.active-modbus {
  border-color: rgba(0, 229, 255, 0.4);
  background: rgba(0, 229, 255, 0.08);
}

.status-top {
  display: flex;
  align-items: center;
  gap: 5px;
}

.dot-online {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 6px #10b981;
}

.status-name {
  color: #94a3b8;
}

.status-state {
  color: #e2e8f0;
}

.status-state.highlight {
  color: #00e5ff;
  font-weight: 700;
}

.alarm-banner-box {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--bg-card-inner, #0b172d);
  border: 1px solid var(--border-color, #162a50);
  border-radius: 4px;
  padding: 4px 10px;
}

.alarm-banner-label {
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.8px;
  color: #64748b;
  border-right: 1px solid #1c3666;
  padding-right: 8px;
}

.alarm-banner-text {
  display: flex;
  align-items: center;
  gap: 6px;
}

.alarm-msg {
  font-size: 10px;
  font-weight: 600;
  color: #34d399;
}

/* Right Cluster */
.ribbon-right-cluster {
  display: flex;
  align-items: center;
  gap: 10px;
}

.mode-toggle-group {
  display: flex;
  background: #0c1830;
  border: 1px solid #1a325e;
  border-radius: 4px;
  overflow: hidden;
}

.mode-btn {
  background: transparent;
  border: none;
  color: #94a3b8;
  padding: 4px 10px;
  font-size: 10.5px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.mode-btn:hover {
  color: #ffffff;
}

.mode-btn.active {
  background: #00e5ff;
  color: #060e1d;
  font-weight: 800;
}

.btn-estop-armed {
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.5);
  color: #ef4444;
  padding: 3px 9px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-estop-armed:hover {
  background: rgba(239, 68, 68, 0.25);
  border-color: #ef4444;
}

.btn-estop-armed.triggered {
  background: #dc2626;
  color: #ffffff;
  animation: blink-red 1s infinite;
}

@keyframes blink-red {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.btn-estop-armed svg {
  width: 14px;
  height: 14px;
}

.estop-labels {
  display: flex;
  gap: 4px;
  font-size: 10px;
  font-weight: 800;
}

.profile-avatar-btn {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #0e1c36;
  border: 1px solid #1c3666;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #38bdf8;
  cursor: pointer;
}

.profile-avatar-btn svg {
  width: 14px;
  height: 14px;
}

/* 2. Scrollable Body */
.scada-content {
  flex: 1;
  overflow-y: auto;
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Modbus TCP Connection Ribbon */
.modbus-conn-ribbon {
  background: var(--bg-card, #091326);
  border: 1px solid var(--border-color, #152747);
  border-radius: 5px;
  padding: 8px 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.conn-left-items,
.conn-right-items {
  display: flex;
  align-items: center;
  gap: 16px;
}

.conn-badge {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pulsing-green-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 8px #10b981;
  animation: pulse-dot 1.5s infinite;
}

@keyframes pulse-dot {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.25); opacity: 0.7; }
}

.conn-title {
  font-size: 11.5px;
  font-weight: 700;
  color: #00e5ff;
  letter-spacing: 0.4px;
}

.conn-meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
}

.meta-label {
  color: #64748b;
  font-weight: 700;
  font-size: 10px;
  letter-spacing: 0.4px;
}

.meta-value {
  color: #e2e8f0;
  font-weight: 600;
}

.cyan-text { color: #00e5ff; }
.green-text { color: #10b981; }
.purple-text { color: #c084fc; }
.cyan-blue-text { color: #38bdf8; }
.dim-text { color: #64748b; }
.dim-cyan-text { color: #0284c7; }
.dim-purple-text { color: #9333ea; }

.watchdog-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 10px;
  font-weight: 700;
  color: #10b981;
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.35);
  padding: 2px 7px;
  border-radius: 4px;
}

.small-green-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #10b981;
}

/* Tool Buttons (CSV & PCAP) */
.btn-tool-export,
.btn-tool-pcap {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10.5px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-tool-export {
  background: #0c1830;
  border: 1px solid #1a3461;
  color: #e2e8f0;
}

.btn-tool-export:hover {
  background: #112244;
  border-color: #00e5ff;
  color: #00e5ff;
}

.btn-tool-export svg {
  width: 12px;
  height: 12px;
}

.btn-tool-pcap {
  background: #00e5ff;
  border: 1px solid #00e5ff;
  color: #060e1d;
  font-weight: 800;
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.2);
}

.btn-tool-pcap:hover {
  background: #33ecff;
  box-shadow: 0 0 14px rgba(0, 229, 255, 0.4);
}

.btn-tool-pcap svg {
  width: 12px;
  height: 12px;
}

/* 3. 6 Protocol KPI Metrics Grid */
.kpi-metrics-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 10px;
}

.metric-card {
  background: var(--bg-card, #0a1326);
  border: 1px solid var(--border-color, #142340);
  border-radius: 5px;
  padding: 10px 14px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.metric-title {
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: #64748b;
}

.metric-value {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.3px;
  color: #ffffff;
  margin: 2px 0;
}

.metric-subtext {
  font-size: 9.5px;
  font-weight: 600;
}

/* 4. MODBUS REGISTER MAPPING & LIVE POLLING TABLE */
.scada-table-panel {
  background: var(--bg-card, #091224);
  border: 1px solid var(--border-color, #142442);
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.table-panel-header {
  padding: 12px 16px;
  border-bottom: 1px solid #12203a;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.table-title-box {
  display: flex;
  align-items: center;
  gap: 10px;
}

.table-icon-badge {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: rgba(0, 229, 255, 0.12);
  border: 1px solid rgba(0, 229, 255, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #00e5ff;
}

.table-icon-badge svg {
  width: 18px;
  height: 18px;
}

.table-title {
  font-size: 13px;
  font-weight: 800;
  color: #00e5ff;
  letter-spacing: 0.6px;
  margin: 0;
}

.table-sub-info {
  font-size: 10px;
  color: #64748b;
  margin: 2px 0 0 0;
}

/* Search Box */
.table-search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--bg-card-inner, #0d1a33);
  border: 1px solid var(--border-color, #1a3461);
  border-radius: 4px;
  padding: 4px 10px;
  width: 280px;
}

.table-search-box svg {
  width: 14px;
  height: 14px;
  color: #64748b;
}

.search-input {
  background: transparent;
  border: none;
  color: #ffffff;
  font-size: 11px;
  width: 100%;
  outline: none;
}

.search-input::placeholder {
  color: #475569;
}

/* Filter Segmented Tabs Bar */
.table-tabs-bar {
  padding: 8px 16px;
  background: var(--bg-card-inner, #070e1d);
  border-bottom: 1px solid var(--border-color, #12203a);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.tab-pill-group {
  display: flex;
  gap: 6px;
}

.tab-pill {
  background: #0c1830;
  border: 1px solid #182e56;
  border-radius: 4px;
  color: #94a3b8;
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.4px;
  padding: 5px 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-pill:hover {
  background: #112244;
  color: #ffffff;
}

.tab-pill.active {
  background: #00e5ff;
  border-color: #00e5ff;
  color: #060e1d;
  font-weight: 800;
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.25);
}

.table-live-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10.5px;
  color: #64748b;
}

.indicator-text {
  color: #94a3b8;
}

/* Data Table Styling */
.table-responsive-wrapper {
  overflow-x: auto;
}

.modbus-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.modbus-table th {
  background: var(--bg-card-inner, #081122);
  color: var(--text-muted, #64748b);
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.6px;
  padding: 9px 12px;
  border-bottom: 1px solid #142442;
  white-space: nowrap;
}

.modbus-table td {
  padding: 8px 12px;
  border-bottom: 1px solid #0f1c33;
  font-size: 11.5px;
  color: #cbd5e1;
  vertical-align: middle;
  white-space: nowrap;
}

.modbus-table tbody tr {
  transition: background-color 0.15s ease;
}

.modbus-table tbody tr:hover {
  background: rgba(0, 229, 255, 0.04);
}

.modbus-table tbody tr.row-flashing {
  background: rgba(0, 229, 255, 0.12);
}

.addr-cell {
  color: #00e5ff;
  font-weight: 700;
  font-size: 11px;
}

.tag-cell {
  font-weight: 600;
  color: #ffffff;
}

.tag-flex {
  display: flex;
  align-items: center;
  gap: 6px;
}

.tag-name {
  color: #f1f5f9;
}

.tag-identifier {
  color: #64748b;
  font-size: 10px;
}

.dtype-cell {
  color: #7dd3fc;
  font-size: 10.5px;
}

.raw-cell {
  color: #94a3b8;
  font-size: 11px;
}

.scaled-cell {
  font-weight: 700;
}

.scaled-badge {
  display: inline-block;
  padding: 2px 6px;
  border-radius: 3px;
}

.scaled-badge.cyan-val {
  color: #00e5ff;
  font-size: 12px;
}

.scaled-badge.bool-true {
  color: #10b981;
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.35);
  font-size: 10.5px;
}

.scaled-badge.bool-false {
  color: #94a3b8;
  background: rgba(148, 163, 184, 0.1);
  border: 1px solid rgba(148, 163, 184, 0.25);
  font-size: 10.5px;
}

.units-cell {
  color: #94a3b8;
  font-size: 11px;
}

.scan-cell {
  font-size: 11px;
}

/* Health Badge */
.health-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 10.5px;
  font-weight: 700;
}

.health-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.health-good .health-dot {
  background: #10b981;
  box-shadow: 0 0 5px #10b981;
}

.health-good .health-label {
  color: #10b981;
}

.health-active .health-dot {
  background: #00e5ff;
  box-shadow: 0 0 5px #00e5ff;
}

.health-active .health-label {
  color: #00e5ff;
}

/* Table Override Action Buttons */
.btn-table-action {
  background: #0b1830;
  border: 1px solid #1a3666;
  border-radius: 4px;
  padding: 3px 9px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-write {
  color: #38bdf8;
  border-color: rgba(56, 189, 248, 0.4);
}

.btn-write:hover {
  background: rgba(56, 189, 248, 0.15);
  border-color: #38bdf8;
  color: #ffffff;
}

.btn-force {
  color: #10b981;
  border-color: rgba(16, 185, 129, 0.4);
}

.btn-force:hover {
  background: rgba(16, 185, 129, 0.15);
  border-color: #10b981;
}

.btn-force-active {
  background: rgba(16, 185, 129, 0.2);
  color: #34d399;
}

.read-only-tag {
  font-size: 9.5px;
  color: #475569;
  letter-spacing: 0.5px;
}

.no-records-cell {
  text-align: center;
  padding: 32px 16px;
  color: #64748b;
  font-size: 12px;
}

/* Modals */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(4, 9, 20, 0.85);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-card {
  width: 520px;
  max-width: 90vw;
  background: #091224;
  border: 1px solid #182e56;
  border-radius: 8px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.pcap-card {
  width: 720px;
}

.modal-header {
  padding: 14px 18px;
  background: #0d1a33;
  border-bottom: 1px solid #1a3461;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-title-box {
  display: flex;
  align-items: center;
  gap: 10px;
}

.modal-icon {
  width: 20px;
  height: 20px;
  color: #00e5ff;
}

.modal-header h3 {
  font-size: 13px;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
}

.modal-sub {
  font-size: 10.5px;
  color: #64748b;
  margin: 2px 0 0 0;
}

.modal-close-btn {
  background: transparent;
  border: none;
  color: #94a3b8;
  font-size: 20px;
  cursor: pointer;
  line-height: 1;
}

.modal-close-btn:hover {
  color: #ffffff;
}

.modal-body {
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.write-meta-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  background: #070e1c;
  border: 1px solid #132442;
  border-radius: 6px;
  padding: 10px;
}

.meta-box {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.m-label {
  font-size: 9px;
  color: #64748b;
  font-weight: 700;
}

.m-val {
  font-size: 11px;
}

.form-group-write {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.input-label {
  font-size: 11px;
  font-weight: 700;
  color: #cbd5e1;
}

.input-inline-wrap {
  display: flex;
  align-items: center;
  background: #070e1c;
  border: 1px solid #1c3666;
  border-radius: 5px;
  overflow: hidden;
  padding: 0 10px;
}

.input-inline-wrap:focus-within {
  border-color: #00e5ff;
  box-shadow: 0 0 8px rgba(0, 229, 255, 0.25);
}

.write-input {
  flex: 1;
  background: transparent;
  border: none;
  color: #00e5ff;
  font-size: 13px;
  font-weight: 700;
  padding: 9px 0;
  outline: none;
}

.unit-suffix {
  font-size: 11px;
  color: #64748b;
  font-weight: 700;
}

.calc-hex-preview {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 10px;
  color: #94a3b8;
  padding: 4px 2px;
}

.success-alert {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.4);
  color: #34d399;
  font-size: 11px;
  padding: 8px 12px;
  border-radius: 4px;
}

.success-alert svg {
  width: 14px;
  height: 14px;
}

.modal-footer {
  padding: 12px 18px;
  background: #081122;
  border-top: 1px solid #142442;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
}

.btn-cancel {
  background: #0c1830;
  border: 1px solid #1a325e;
  color: #94a3b8;
  padding: 6px 14px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
}

.btn-cancel:hover {
  color: #ffffff;
}

.btn-send-write,
.btn-primary {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #00e5ff;
  border: 1px solid #00e5ff;
  color: #060e1d;
  padding: 6px 16px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.25);
}

.btn-send-write:hover,
.btn-primary:hover {
  background: #33ecff;
}

.btn-send-write svg {
  width: 12px;
  height: 12px;
}

/* PCAP Trace Modal */
.pcap-body {
  max-height: 400px;
  overflow-y: auto;
  padding: 12px;
  background: #060c18;
}

.pcap-log-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.pcap-row {
  display: grid;
  grid-template-columns: 85px 40px 50px 1fr 180px;
  align-items: center;
  gap: 8px;
  font-size: 10px;
  padding: 5px 8px;
  border-radius: 4px;
  background: #0a1428;
  border: 1px solid #132442;
}

.pcap-row.pcap-tx {
  border-left: 3px solid #38bdf8;
}

.pcap-row.pcap-rx {
  border-left: 3px solid #10b981;
}

.pcap-time {
  color: #64748b;
}

.pcap-dir-badge {
  font-weight: 800;
  font-size: 9px;
  padding: 1px 4px;
  border-radius: 3px;
  text-align: center;
}

.badge-tx {
  background: rgba(56, 189, 248, 0.2);
  color: #38bdf8;
}

.badge-rx {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.pcap-fc {
  color: #f1f5f9;
  font-weight: 700;
}

.pcap-desc {
  color: #cbd5e1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.pcap-hex {
  color: #64748b;
  font-size: 9.5px;
  text-align: right;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

</style>

<style>
/* ==========================================================================
   UNSCOPED LIGHT MODE STYLES FOR MODBUS TELEMETRY
   ========================================================================== */
[data-theme="light"] .scada-container {
  background: #f1f5f9 !important;
  color: #0f172a !important;
}

[data-theme="light"] .scada-header-ribbon {
  background: #ffffff !important;
  border-bottom: 1px solid #cbd5e1 !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
}

[data-theme="light"] .brand-droplet-badge {
  background: rgba(2, 132, 199, 0.1) !important;
  border-color: rgba(2, 132, 199, 0.3) !important;
}

[data-theme="light"] .brand-droplet-badge svg path {
  fill: #0284c7 !important;
  stroke: #0284c7 !important;
}

[data-theme="light"] .brand-primary {
  color: #0f172a !important;
}

[data-theme="light"] .brand-sub {
  color: #64748b !important;
}

[data-theme="light"] .status-box {
  background: #f8fafc !important;
  border-color: #cbd5e1 !important;
}

[data-theme="light"] .status-box.active-modbus {
  background: rgba(2, 132, 199, 0.08) !important;
  border-color: rgba(2, 132, 199, 0.4) !important;
}

[data-theme="light"] .status-name {
  color: #64748b !important;
}

[data-theme="light"] .status-state {
  color: #334155 !important;
}

[data-theme="light"] .status-state.highlight {
  color: #0284c7 !important;
}

[data-theme="light"] .alarm-banner-box {
  background: #f0fdf4 !important;
  border-color: #bbf7d0 !important;
}

[data-theme="light"] .alarm-banner-label {
  color: #64748b !important;
  border-right-color: #cbd5e1 !important;
}

[data-theme="light"] .alarm-msg {
  color: #15803d !important;
}

[data-theme="light"] .mode-toggle-group {
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
}

[data-theme="light"] .mode-btn {
  color: #64748b !important;
}

[data-theme="light"] .mode-btn:hover {
  color: #0f172a !important;
}

[data-theme="light"] .mode-btn.active {
  background: #0284c7 !important;
  color: #ffffff !important;
}

[data-theme="light"] .profile-avatar-btn {
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
  color: #0284c7 !important;
}

[data-theme="light"] .modbus-conn-ribbon {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
}

[data-theme="light"] .conn-title {
  color: #0284c7 !important;
}

[data-theme="light"] .meta-label {
  color: #64748b !important;
}

[data-theme="light"] .meta-value {
  color: #0f172a !important;
}

[data-theme="light"] .cyan-text {
  color: #0284c7 !important;
}

[data-theme="light"] .green-text {
  color: #059669 !important;
}

[data-theme="light"] .purple-text {
  color: #7c3aed !important;
}

[data-theme="light"] .cyan-blue-text {
  color: #0284c7 !important;
}

[data-theme="light"] .dim-text {
  color: #64748b !important;
}

[data-theme="light"] .dim-cyan-text {
  color: #0369a1 !important;
}

[data-theme="light"] .dim-purple-text {
  color: #6d28d9 !important;
}

[data-theme="light"] .watchdog-pill {
  background: rgba(5, 150, 105, 0.1) !important;
  border-color: rgba(5, 150, 105, 0.3) !important;
  color: #059669 !important;
}

[data-theme="light"] .btn-tool-export {
  background: #f8fafc !important;
  border-color: #cbd5e1 !important;
  color: #334155 !important;
}

[data-theme="light"] .btn-tool-export:hover {
  background: #f1f5f9 !important;
  border-color: #0284c7 !important;
  color: #0284c7 !important;
}

[data-theme="light"] .btn-tool-pcap {
  background: #0284c7 !important;
  border-color: #0284c7 !important;
  color: #ffffff !important;
  box-shadow: 0 2px 6px rgba(2, 132, 199, 0.3) !important;
}

[data-theme="light"] .btn-tool-pcap:hover {
  background: #0369a1 !important;
}

[data-theme="light"] .metric-card {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
}

[data-theme="light"] .metric-title {
  color: #64748b !important;
}

[data-theme="light"] .metric-value {
  color: #0f172a !important;
}

[data-theme="light"] .scada-table-panel {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05) !important;
}

[data-theme="light"] .table-panel-header {
  border-bottom-color: #e2e8f0 !important;
}

[data-theme="light"] .table-icon-badge {
  background: rgba(2, 132, 199, 0.1) !important;
  border-color: rgba(2, 132, 199, 0.3) !important;
  color: #0284c7 !important;
}

[data-theme="light"] .table-title {
  color: #0284c7 !important;
}

[data-theme="light"] .table-sub-info {
  color: #64748b !important;
}

[data-theme="light"] .table-search-box {
  background: #f8fafc !important;
  border-color: #cbd5e1 !important;
}

[data-theme="light"] .table-search-box svg {
  color: #64748b !important;
}

[data-theme="light"] .search-input {
  color: #0f172a !important;
}

[data-theme="light"] .search-input::placeholder {
  color: #94a3b8 !important;
}

[data-theme="light"] .table-tabs-bar {
  background: #f8fafc !important;
  border-bottom-color: #e2e8f0 !important;
}

[data-theme="light"] .tab-pill {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  color: #475569 !important;
}

[data-theme="light"] .tab-pill:hover {
  background: #f1f5f9 !important;
  color: #0f172a !important;
}

[data-theme="light"] .tab-pill.active {
  background: #0284c7 !important;
  border-color: #0284c7 !important;
  color: #ffffff !important;
  box-shadow: 0 2px 6px rgba(2, 132, 199, 0.25) !important;
}

[data-theme="light"] .indicator-text {
  color: #64748b !important;
}

[data-theme="light"] .modbus-table {
  background: #ffffff !important;
}

[data-theme="light"] .modbus-table th {
  background: #f8fafc !important;
  color: #475569 !important;
  border-bottom: 1px solid #cbd5e1 !important;
}

[data-theme="light"] .modbus-table td {
  background: #ffffff !important;
  border-bottom: 1px solid #f1f5f9 !important;
  color: #334155 !important;
}

[data-theme="light"] .modbus-table tbody tr:hover td {
  background: #f8fafc !important;
}

[data-theme="light"] .modbus-table tbody tr.row-flashing td {
  background: rgba(2, 132, 199, 0.1) !important;
}

[data-theme="light"] .addr-cell {
  color: #0284c7 !important;
}

[data-theme="light"] .tag-name {
  color: #0f172a !important;
}

[data-theme="light"] .tag-identifier {
  color: #64748b !important;
}

[data-theme="light"] .dtype-cell {
  color: #0369a1 !important;
}

[data-theme="light"] .raw-cell {
  color: #64748b !important;
}

[data-theme="light"] .scaled-badge.cyan-val {
  color: #0284c7 !important;
}

[data-theme="light"] .scaled-badge.bool-true {
  color: #059669 !important;
  background: rgba(5, 150, 105, 0.1) !important;
  border-color: rgba(5, 150, 105, 0.3) !important;
}

[data-theme="light"] .scaled-badge.bool-false {
  color: #64748b !important;
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
}

[data-theme="light"] .units-cell {
  color: #64748b !important;
}

[data-theme="light"] .scan-cell {
  color: #64748b !important;
}

[data-theme="light"] .btn-write {
  color: #0284c7 !important;
  border-color: #0284c7 !important;
  background: #f0f9ff !important;
}

[data-theme="light"] .btn-write:hover {
  background: #0284c7 !important;
  color: #ffffff !important;
}

[data-theme="light"] .btn-force {
  color: #059669 !important;
  border-color: #059669 !important;
  background: #ecfdf5 !important;
}

[data-theme="light"] .btn-force:hover {
  background: #059669 !important;
  color: #ffffff !important;
}

[data-theme="light"] .btn-force-active {
  background: #059669 !important;
  color: #ffffff !important;
}

[data-theme="light"] .read-only-tag {
  color: #94a3b8 !important;
}

[data-theme="light"] .modal-overlay {
  background: rgba(15, 23, 42, 0.6) !important;
}

[data-theme="light"] .modal-card {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15) !important;
}

[data-theme="light"] .modal-header {
  background: #f8fafc !important;
  border-bottom: 1px solid #e2e8f0 !important;
}

[data-theme="light"] .modal-header h3 {
  color: #0f172a !important;
}

[data-theme="light"] .modal-sub {
  color: #64748b !important;
}

[data-theme="light"] .modal-close-btn {
  color: #64748b !important;
}

[data-theme="light"] .modal-close-btn:hover {
  color: #0f172a !important;
}

[data-theme="light"] .modal-body {
  background: #ffffff !important;
}

[data-theme="light"] .write-meta-grid {
  background: #f8fafc !important;
  border-color: #e2e8f0 !important;
}

[data-theme="light"] .write-meta-grid .m-label {
  color: #64748b !important;
}

[data-theme="light"] .write-meta-grid .m-val {
  color: #0f172a !important;
}

[data-theme="light"] .input-label {
  color: #0f172a !important;
}

[data-theme="light"] .input-inline-wrap {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
}

[data-theme="light"] .input-inline-wrap:focus-within {
  border-color: #0284c7 !important;
  box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15) !important;
}

[data-theme="light"] .write-input {
  color: #0284c7 !important;
}

[data-theme="light"] .modal-footer {
  background: #f8fafc !important;
  border-top: 1px solid #e2e8f0 !important;
}

[data-theme="light"] .btn-cancel {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  color: #475569 !important;
}

[data-theme="light"] .btn-cancel:hover {
  background: #f1f5f9 !important;
  color: #0f172a !important;
}

[data-theme="light"] .btn-send-write {
  background: #0284c7 !important;
  border-color: #0284c7 !important;
  color: #ffffff !important;
}

[data-theme="light"] .btn-send-write:hover {
  background: #0369a1 !important;
}

[data-theme="light"] .pcap-body {
  background: #f8fafc !important;
}

[data-theme="light"] .pcap-row {
  background: #ffffff !important;
  border-color: #e2e8f0 !important;
}

[data-theme="light"] .pcap-time {
  color: #64748b !important;
}

[data-theme="light"] .pcap-fc {
  color: #0f172a !important;
}

[data-theme="light"] .pcap-desc {
  color: #334155 !important;
}

[data-theme="light"] .pcap-hex {
  color: #64748b !important;
}
</style>


<style>
/* ==========================================================================
   UNSCOPED LIGHT MODE STYLES FOR MODBUS TELEMETRY
   ========================================================================== */
[data-theme="light"] .scada-container {
  background: #f1f5f9 !important;
  color: #0f172a !important;
}

[data-theme="light"] .scada-header-ribbon {
  background: #ffffff !important;
  border-bottom: 1px solid #cbd5e1 !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
}

[data-theme="light"] .brand-droplet-badge {
  background: rgba(2, 132, 199, 0.1) !important;
  border-color: rgba(2, 132, 199, 0.3) !important;
}

[data-theme="light"] .brand-droplet-badge svg path {
  fill: #0284c7 !important;
  stroke: #0284c7 !important;
}

[data-theme="light"] .brand-primary {
  color: #0f172a !important;
}

[data-theme="light"] .brand-sub {
  color: #64748b !important;
}

[data-theme="light"] .status-box {
  background: #f8fafc !important;
  border-color: #cbd5e1 !important;
}

[data-theme="light"] .status-box.active-modbus {
  background: rgba(2, 132, 199, 0.08) !important;
  border-color: rgba(2, 132, 199, 0.4) !important;
}

[data-theme="light"] .status-name {
  color: #64748b !important;
}

[data-theme="light"] .status-state {
  color: #334155 !important;
}

[data-theme="light"] .status-state.highlight {
  color: #0284c7 !important;
}

[data-theme="light"] .alarm-banner-box {
  background: #f0fdf4 !important;
  border-color: #bbf7d0 !important;
}

[data-theme="light"] .alarm-banner-label {
  color: #64748b !important;
  border-right-color: #cbd5e1 !important;
}

[data-theme="light"] .alarm-msg {
  color: #15803d !important;
}

[data-theme="light"] .mode-toggle-group {
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
}

[data-theme="light"] .mode-btn {
  color: #64748b !important;
}

[data-theme="light"] .mode-btn:hover {
  color: #0f172a !important;
}

[data-theme="light"] .mode-btn.active {
  background: #0284c7 !important;
  color: #ffffff !important;
}

[data-theme="light"] .profile-avatar-btn {
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
  color: #0284c7 !important;
}

[data-theme="light"] .modbus-conn-ribbon {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
}

[data-theme="light"] .conn-title {
  color: #0284c7 !important;
}

[data-theme="light"] .meta-label {
  color: #64748b !important;
}

[data-theme="light"] .meta-value {
  color: #0f172a !important;
}

[data-theme="light"] .cyan-text {
  color: #0284c7 !important;
}

[data-theme="light"] .green-text {
  color: #059669 !important;
}

[data-theme="light"] .purple-text {
  color: #7c3aed !important;
}

[data-theme="light"] .cyan-blue-text {
  color: #0284c7 !important;
}

[data-theme="light"] .dim-text {
  color: #64748b !important;
}

[data-theme="light"] .dim-cyan-text {
  color: #0369a1 !important;
}

[data-theme="light"] .dim-purple-text {
  color: #6d28d9 !important;
}

[data-theme="light"] .watchdog-pill {
  background: rgba(5, 150, 105, 0.1) !important;
  border-color: rgba(5, 150, 105, 0.3) !important;
  color: #059669 !important;
}

[data-theme="light"] .btn-tool-export {
  background: #f8fafc !important;
  border-color: #cbd5e1 !important;
  color: #334155 !important;
}

[data-theme="light"] .btn-tool-export:hover {
  background: #f1f5f9 !important;
  border-color: #0284c7 !important;
  color: #0284c7 !important;
}

[data-theme="light"] .btn-tool-pcap {
  background: #0284c7 !important;
  border-color: #0284c7 !important;
  color: #ffffff !important;
  box-shadow: 0 2px 6px rgba(2, 132, 199, 0.3) !important;
}

[data-theme="light"] .btn-tool-pcap:hover {
  background: #0369a1 !important;
}

[data-theme="light"] .metric-card {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
}

[data-theme="light"] .metric-title {
  color: #64748b !important;
}

[data-theme="light"] .metric-value {
  color: #0f172a !important;
}

[data-theme="light"] .scada-table-panel {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05) !important;
}

[data-theme="light"] .table-panel-header {
  border-bottom-color: #e2e8f0 !important;
}

[data-theme="light"] .table-icon-badge {
  background: rgba(2, 132, 199, 0.1) !important;
  border-color: rgba(2, 132, 199, 0.3) !important;
  color: #0284c7 !important;
}

[data-theme="light"] .table-title {
  color: #0284c7 !important;
}

[data-theme="light"] .table-sub-info {
  color: #64748b !important;
}

[data-theme="light"] .table-search-box {
  background: #f8fafc !important;
  border-color: #cbd5e1 !important;
}

[data-theme="light"] .table-search-box svg {
  color: #64748b !important;
}

[data-theme="light"] .search-input {
  color: #0f172a !important;
}

[data-theme="light"] .search-input::placeholder {
  color: #94a3b8 !important;
}

[data-theme="light"] .table-tabs-bar {
  background: #f8fafc !important;
  border-bottom-color: #e2e8f0 !important;
}

[data-theme="light"] .tab-pill {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  color: #475569 !important;
}

[data-theme="light"] .tab-pill:hover {
  background: #f1f5f9 !important;
  color: #0f172a !important;
}

[data-theme="light"] .tab-pill.active {
  background: #0284c7 !important;
  border-color: #0284c7 !important;
  color: #ffffff !important;
  box-shadow: 0 2px 6px rgba(2, 132, 199, 0.25) !important;
}

[data-theme="light"] .indicator-text {
  color: #64748b !important;
}

[data-theme="light"] .modbus-table {
  background: #ffffff !important;
}

[data-theme="light"] .modbus-table th {
  background: #f8fafc !important;
  color: #475569 !important;
  border-bottom: 1px solid #cbd5e1 !important;
}

[data-theme="light"] .modbus-table td {
  background: #ffffff !important;
  border-bottom: 1px solid #f1f5f9 !important;
  color: #334155 !important;
}

[data-theme="light"] .modbus-table tbody tr:hover td {
  background: #f8fafc !important;
}

[data-theme="light"] .modbus-table tbody tr.row-flashing td {
  background: rgba(2, 132, 199, 0.1) !important;
}

[data-theme="light"] .addr-cell {
  color: #0284c7 !important;
}

[data-theme="light"] .tag-name {
  color: #0f172a !important;
}

[data-theme="light"] .tag-identifier {
  color: #64748b !important;
}

[data-theme="light"] .dtype-cell {
  color: #0369a1 !important;
}

[data-theme="light"] .raw-cell {
  color: #64748b !important;
}

[data-theme="light"] .scaled-badge.cyan-val {
  color: #0284c7 !important;
}

[data-theme="light"] .scaled-badge.bool-true {
  color: #059669 !important;
  background: rgba(5, 150, 105, 0.1) !important;
  border-color: rgba(5, 150, 105, 0.3) !important;
}

[data-theme="light"] .scaled-badge.bool-false {
  color: #64748b !important;
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
}

[data-theme="light"] .units-cell {
  color: #64748b !important;
}

[data-theme="light"] .scan-cell {
  color: #64748b !important;
}

[data-theme="light"] .btn-write {
  color: #0284c7 !important;
  border-color: #0284c7 !important;
  background: #f0f9ff !important;
}

[data-theme="light"] .btn-write:hover {
  background: #0284c7 !important;
  color: #ffffff !important;
}

[data-theme="light"] .btn-force {
  color: #059669 !important;
  border-color: #059669 !important;
  background: #ecfdf5 !important;
}

[data-theme="light"] .btn-force:hover {
  background: #059669 !important;
  color: #ffffff !important;
}

[data-theme="light"] .btn-force-active {
  background: #059669 !important;
  color: #ffffff !important;
}

[data-theme="light"] .read-only-tag {
  color: #94a3b8 !important;
}

[data-theme="light"] .modal-overlay {
  background: rgba(15, 23, 42, 0.6) !important;
}

[data-theme="light"] .modal-card {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15) !important;
}

[data-theme="light"] .modal-header {
  background: #f8fafc !important;
  border-bottom: 1px solid #e2e8f0 !important;
}

[data-theme="light"] .modal-header h3 {
  color: #0f172a !important;
}

[data-theme="light"] .modal-sub {
  color: #64748b !important;
}

[data-theme="light"] .modal-close-btn {
  color: #64748b !important;
}

[data-theme="light"] .modal-close-btn:hover {
  color: #0f172a !important;
}

[data-theme="light"] .modal-body {
  background: #ffffff !important;
}

[data-theme="light"] .write-meta-grid {
  background: #f8fafc !important;
  border-color: #e2e8f0 !important;
}

[data-theme="light"] .write-meta-grid .m-label {
  color: #64748b !important;
}

[data-theme="light"] .write-meta-grid .m-val {
  color: #0f172a !important;
}

[data-theme="light"] .input-label {
  color: #0f172a !important;
}

[data-theme="light"] .input-inline-wrap {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
}

[data-theme="light"] .input-inline-wrap:focus-within {
  border-color: #0284c7 !important;
  box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15) !important;
}

[data-theme="light"] .write-input {
  color: #0284c7 !important;
}

[data-theme="light"] .modal-footer {
  background: #f8fafc !important;
  border-top: 1px solid #e2e8f0 !important;
}

[data-theme="light"] .btn-cancel {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  color: #475569 !important;
}

[data-theme="light"] .btn-cancel:hover {
  background: #f1f5f9 !important;
  color: #0f172a !important;
}

[data-theme="light"] .btn-send-write {
  background: #0284c7 !important;
  border-color: #0284c7 !important;
  color: #ffffff !important;
}

[data-theme="light"] .btn-send-write:hover {
  background: #0369a1 !important;
}

[data-theme="light"] .pcap-body {
  background: #f8fafc !important;
}

[data-theme="light"] .pcap-row {
  background: #ffffff !important;
  border-color: #e2e8f0 !important;
}

[data-theme="light"] .pcap-time {
  color: #64748b !important;
}

[data-theme="light"] .pcap-fc {
  color: #0f172a !important;
}

[data-theme="light"] .pcap-desc {
  color: #334155 !important;
}

[data-theme="light"] .pcap-hex {
  color: #64748b !important;
}
</style>
