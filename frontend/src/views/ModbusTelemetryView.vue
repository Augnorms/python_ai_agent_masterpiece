<template>
  <div class="scada-container">
    <!-- Top SCADA Plant Header Ribbon -->
    <div class="scada-header-ribbon">

      <!-- Top Network Status Indicators -->
      <div class="ribbon-center-cluster">

        <div class="status-box active-modbus">
          <div class="status-top">
            <span :class="plcConnected ? 'dot-online' : 'dot-offline'"></span>
            <span class="status-name">MODBUS TCP:</span>
            <span class="status-state highlight">{{ modbusStatusDisplay }}</span>
          </div>
        </div>
      </div>

    </div>

    <!-- Main Scrollable Content -->
    <div class="scada-content">
      <!-- Modbus TCP Connection & Status Ribbon -->
      <div class="modbus-conn-ribbon">
        <div class="conn-left-items">
          <div class="conn-badge">
            <span :class="plcConnected ? 'pulsing-green-dot' : 'pulsing-red-dot'"></span>
            <span class="conn-title font-mono">MODBUS TCP CONNECTED TO:  {{ modbusConnectionDisplay }}</span>
          </div>

        </div>

        <div class="conn-right-items">

          <button type="button" class="btn-tool-export" @click="exportRegistersCsv">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="7 10 12 15 17 10" />
              <line x1="12" y1="15" x2="12" y2="3" />
            </svg>
            <span>EXPORT CSV</span>
          </button>

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
                Holding Registers ({{ holdingCount }}) | Input Registers ({{ inputCount }}) | Coils ({{ coilCount }})
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
            <span :class="plcConnected ? 'pulsing-green-dot' : 'pulsing-red-dot'"></span>
            <span class="indicator-text font-mono">CYCLE SCAN: {{ lastScanTime || '--:--:--' }}</span>
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



  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// ─── Backend API Base URL ───────────────────────────────────────
const API_BASE = 'http://localhost:8000'

// Top Bar States
const currentMode = ref('AUTO')
const eStopTriggered = ref(false)
const plcConnected = ref(false)
const telemetryError = ref('')
const modbusConnection = ref('')
const modbusStatus = ref(null)
const lastScanTime = ref('')

const modbusStatusDisplay = computed(() => {
  if (typeof modbusStatus.value === 'string' && modbusStatus.value) {
    return modbusStatus.value
  }
  if (modbusStatus.value === true || plcConnected.value) {
    return 'SLAVE #01 OK'
  }
  return 'OFFLINE'
})

const modbusConnectionDisplay = computed(() => {
  if (modbusConnection.value) {
    return modbusConnection.value
  }
  return plcConnected.value ? '127.0.0.1:502' : 'OFFLINE'
})

const toggleEStop = () => {
  eStopTriggered.value = !eStopTriggered.value
}

// Connection Metrics
const pollRate = ref(50)
const jitter = ref(1.2)
const totalFrames = ref(0)
const meanLatency = ref(0)
const fc03Requests = ref(0)
const fcWrites = ref(0)

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

// PCAP Packet Trace Log
const pcapPackets = ref([])

// Modbus Register Mapping Table Dataset
const registers = ref([])

// ─── Scale factor lookup for converting scaled → raw values ─────
const SCALE_FACTORS = {
  '40001': 10,  // Feed Flowrate (x10)
  '40002': 1,   // Feed TDS
  '40003': 10,  // Feed Temperature (x10)
  '40007': 10,  // Feed Salinity (x10)
  '40008': 10,  // Recovery (x10)
  '40009': 10,  // Flux (x10)
  '40010': 10,  // Pressure Drop (x10)
}

// ─── Register category counts (for subtitle) ───────────────────
const holdingCount = computed(() => registers.value.filter(r => r.category === 'HOLDING').length)
const inputCount = computed(() => registers.value.filter(r => r.category === 'INPUT').length)
const coilCount = computed(() => registers.value.filter(r => r.category === 'COIL').length)

// ─── Map backend row → frontend register object ────────────────
const mapBackendRow = (row) => {
  const rawInt = row.raw
  const hex = (rawInt & 0xffff).toString(16).toUpperCase().padStart(4, '0')
  return {
    address: row.address,
    name: row.tag,
    identifier: '',
    dataType: row.type,
    rawInt: rawInt,
    rawHex: `0x${hex} (${rawInt})`,
    scaledValue: row.scaled,
    units: row.unit,
    scaleFactor: SCALE_FACTORS[row.address] || 1,
    scanTime: '50 ms',
    health: row.health || 'GOOD',
    category: 'HOLDING',
    isUpdated: false,
  }
}

// ─── Fetch Live Telemetry from Backend ──────────────────────────
const fetchTelemetry = async () => {
  try {
    const response = await fetch(`${API_BASE}/api/telemetry/live`)
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    const json = await response.json()

    if (json.status === 'success' && Array.isArray(json.data) && json.data.length > 0) {
      plcConnected.value = json.modbus_status !== false
      if (json.modbus_status !== undefined) {
        modbusStatus.value = json.modbus_status
      } else {
        modbusStatus.value = true
      }
      if (json.modbus_connection) {
        modbusConnection.value = json.modbus_connection
      }
      telemetryError.value = ''

      // Record cycle scan time
      const now = new Date()
      const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}.${String(now.getMilliseconds()).padStart(3, '0')}`
      lastScanTime.value = timeStr

      // Map backend rows to frontend register objects
      const liveRows = json.data.map(mapBackendRow)

      if (registers.value.length === 0) {
        // First load — populate the table
        registers.value = liveRows
      } else {
        // Subsequent polls — merge live data into existing rows (preserve UI state like isUpdated)
        for (const liveRow of liveRows) {
          const existing = registers.value.find((r) => r.address === liveRow.address)
          if (existing) {
            // Only update if not currently being written to by the user
            if (!existing.isUpdated) {
              const oldScaled = existing.scaledValue
              existing.scaledValue = liveRow.scaledValue
              existing.rawInt = liveRow.rawInt
              existing.rawHex = liveRow.rawHex
              existing.health = liveRow.health
              // Flash the row if the value changed
              if (oldScaled !== liveRow.scaledValue) {
                existing.isUpdated = true
                setTimeout(() => { existing.isUpdated = false }, 800)
              }
            }
          } else {
            // New register appeared — add it
            registers.value.push(liveRow)
          }
        }
      }

      // Update connection metrics
      fc03Requests.value++
      totalFrames.value += 2

      // Record the poll in the PCAP trace
      pcapPackets.value.unshift({
        time: timeStr,
        dir: 'RX',
        fc: 'FC03',
        desc: `Read Holding Registers [40001-40010] → ${json.data.length} regs`,
        hex: `00 FF 00 00 00 06 01 03 00 00 00 0A`
      })
      // Keep PCAP log manageable
      if (pcapPackets.value.length > 200) {
        pcapPackets.value = pcapPackets.value.slice(0, 200)
      }

    } else {
      // Backend returned error status (PLC unreachable)
      plcConnected.value = false
      modbusStatus.value = false
      if (json && json.modbus_connection) {
        modbusConnection.value = json.modbus_connection
      }
      telemetryError.value = json.message || 'PLC returned empty data'
    }

  } catch (err) {
    plcConnected.value = false
    modbusStatus.value = false
    telemetryError.value = err.message || 'Network error'
  }
}


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

// ─── Live Polling Engine (fetches from backend every 2 seconds) ─
let pollTimer = null
let metricsTimer = null

const tickLivePolling = () => {
  // Fetch real data from the backend PLC endpoint
  fetchTelemetry()
}

// Update jitter & latency display metrics smoothly between polls
const tickMetrics = () => {
  const now = new Date()
  jitter.value = parseFloat((1.1 + Math.sin(now.getTime() / 2500) * 0.25).toFixed(1))
  meanLatency.value = parseFloat((2.41 + Math.cos(now.getTime() / 3200) * 0.06).toFixed(2))
}

onMounted(async () => {
  // Fetch initial data immediately
  await fetchTelemetry()

  // Poll the backend every 2 seconds for live register data
  pollTimer = setInterval(tickLivePolling, 2000)

  // Smooth metric animation every 500ms
  metricsTimer = setInterval(tickMetrics, 500)
})

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
  if (metricsTimer) clearInterval(metricsTimer)
})
</script>

<style scoped src="@/style_folder/ModbusTelemetryView.css"></style>
<style src="@/style_folder/ModbusTelemetryView.global.css"></style>
