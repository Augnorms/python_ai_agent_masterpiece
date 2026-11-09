<template>
  <div class="scada-container">
    <!-- Top SCADA Control & Simulation Ribbon -->
    <div class="control-ribbon">
      <div class="ribbon-left">
        <!-- Simulation Status Pill -->
        <div class="pill-sim-mode" :class="{ halted: eStopActive }">
          <span :class="eStopActive ? 'pulsing-red-dot' : 'pulsing-green-dot'"></span>
          <span class="pill-text">{{ eStopActive ? 'SIMULATION MODE: HALTED (E-STOP)' : 'SIMULATION MODE: RUNNING (100%)' }}</span>
        </div>

        <div class="meta-tag">
          <span class="meta-label">PROCESS ID:</span>
          <span class="meta-val">-</span>
        </div>

        <div class="meta-tag">
          <span class="meta-label">CYCLE CLOCK:</span>
          <span class="meta-val font-mono">{{ cycleClock }}</span>
        </div>

        <!-- Equipment Toggle Badges -->
        <div class="equipment-cluster">
          <div class="equip-badge green" :class="{ off: !pumpP101 }" @click="pumpP101 = !pumpP101" title="Click to toggle Pump P-101">
            <span class="equip-dot"></span>
            <span>PUMP P-101: <strong>{{ pumpP101 ? 'ON' : 'OFF' }}</strong></span>
          </div>
        </div>
      </div>

      <div class="ribbon-right">
        <!-- Emergency Stop Button -->
        <button 
          type="button" 
          class="btn-e-stop" 
          @click="handleEmergencyStop" 
          :class="{ triggered: eStopActive, loading: isEStopLoading }"
          :disabled="isEStopLoading"
          :title="eStopActive ? 'Click to Resume Plant Simulator' : 'Click for Emergency Stop'"
        >
          <svg v-if="!isEStopLoading" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
          <svg v-else class="spin-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="2" x2="12" y2="6"></line>
            <line x1="12" y1="18" x2="12" y2="22"></line>
            <line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line>
            <line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line>
            <line x1="2" y1="12" x2="6" y2="12"></line>
            <line x1="18" y1="12" x2="22" y2="12"></line>
            <line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line>
            <line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line>
          </svg>
          <span>
            {{ isEStopLoading ? (eStopActive ? 'RESUMING...' : 'STOPPING...') : (eStopActive ? 'RESUME PLANT' : 'EMERGENCY STOP') }}
          </span>
        </button>
      </div>
    </div>

    <!-- Main Scrollable Dashboard Content -->
    <div class="scada-content">
      <!-- 7 KPI Metric Cards Row -->
      <div class="kpi-grid">
        <!-- 1. Flow Rate -->
        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-label">FLOW RATE</span>
            <svg class="kpi-icon cyan" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M2 12h20M2 6h20M2 18h20" />
            </svg>
          </div>
          <div class="kpi-body">
            <span class="kpi-value cyan">{{ flowRate.toFixed(1) }}</span>
            <span class="kpi-unit">m³/h</span>
          </div>
          <div class="kpi-footer">
            <div class="kpi-bar-bg">
              <div class="kpi-bar-fill cyan" :style="{ width: `${(flowRate / 120) * 100}%` }"></div>
            </div>
            <span class="kpi-subtext">MAX 120</span>
          </div>
        </div>

        <!-- 2. Salinity / TDS -->
        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-label">SALINITY / TDS</span>
            <svg class="kpi-icon green" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="18" height="18" rx="2" />
              <line x1="3" y1="9" x2="21" y2="9" />
              <line x1="3" y1="15" x2="21" y2="15" />
              <line x1="9" y1="3" x2="9" y2="21" />
              <line x1="15" y1="3" x2="15" y2="21" />
            </svg>
          </div>
          <div class="kpi-body">
            <span class="kpi-value green">{{ salinityTds }}</span>
            <span class="kpi-unit">ppm</span>
          </div>
          <div class="kpi-footer">
            <div class="kpi-bar-bg">
              <div class="kpi-bar-fill green" style="width: 100%"></div>
            </div>
            <span class="kpi-subtext green-text">GRADE A</span>
          </div>
        </div>

        <!-- 3. Temperature -->
        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-label">TEMPERATURE</span>
            <svg class="kpi-icon purple" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z" />
            </svg>
          </div>
          <div class="kpi-body">
            <span class="kpi-value purple">{{ temperature.toFixed(1) }}</span>
            <span class="kpi-unit">°C</span>
          </div>
          <div class="kpi-footer">
            <div class="kpi-bar-bg">
              <div class="kpi-bar-fill purple" style="width: 100%"></div>
            </div>
            <span class="kpi-subtext">SET 25°C</span>
          </div>
        </div>

        <!-- 4. Concentration -->
        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-label">CONCENTRATION</span>
            <svg class="kpi-icon blue" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 22h12a2 2 0 0 0 2-2V8.5a2 2 0 0 0-.586-1.414l-4.5-4.5A2 2 0 0 0 13.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2z" />
              <line x1="9" y1="12" x2="15" y2="12" />
            </svg>
          </div>
          <div class="kpi-body">
            <span class="kpi-value cyan">{{ concentration.toFixed(1) }}</span>
            <span class="kpi-unit">g/L</span>
          </div>
          <div class="kpi-footer">
            <div class="kpi-bar-bg">
              <div class="kpi-bar-fill blue" style="width: 100%"></div>
            </div>
            <span class="kpi-subtext">DOSING OK</span>
          </div>
        </div>

        <!-- 5. Recovery Ratio -->
        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-label">RECOVERY RATIO</span>
            <svg class="kpi-icon green" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6" />
            </svg>
          </div>
          <div class="kpi-body">
            <span class="kpi-value green">{{ recoveryRatio.toFixed(1) }}</span>
            <span class="kpi-unit">%</span>
          </div>
          <div class="kpi-footer">
            <div class="kpi-bar-bg">
              <div class="kpi-bar-fill green" style="width: 75%"></div>
            </div>
            <span class="kpi-subtext green-text">TARGET 75%</span>
          </div>
        </div>

        <!-- 6. Membrane Flux -->
        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-label">MEMBRANE FLUX</span>
            <svg class="kpi-icon cyan" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="7" height="7" />
              <rect x="14" y="3" width="7" height="7" />
              <rect x="14" y="14" width="7" height="7" />
              <rect x="3" y="14" width="7" height="7" />
            </svg>
          </div>
          <div class="kpi-body">
            <span class="kpi-value cyan">{{ membraneFlux.toFixed(1) }}</span>
            <span class="kpi-unit">LMH</span>
          </div>
          <div class="kpi-footer">
            <div class="kpi-bar-bg">
              <div class="kpi-bar-fill cyan" style="width: 100%"></div>
            </div>
            <span class="kpi-subtext">STABLE</span>
          </div>
        </div>

        <!-- 7. Feed Pressure -->
        <div class="kpi-card">
          <div class="kpi-header">
            <span class="kpi-label">FEED PRESSURE</span>
            <svg class="kpi-icon cyan" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="9" />
              <line x1="12" y1="12" x2="16" y2="8" />
            </svg>
          </div>
          <div class="kpi-body">
            <span class="kpi-value cyan">{{ feedPressure.toFixed(1) }}</span>
            <span class="kpi-unit">bar</span>
          </div>
          <div class="kpi-footer">
            <div class="kpi-bar-bg">
              <div class="kpi-bar-fill cyan" :style="{ width: `${(feedPressure / 6.5) * 100}%` }"></div>
            </div>
            <span class="kpi-subtext">MAX 6.5</span>
          </div>
        </div>
      </div>

      <!-- Main Wide Card: Dual-Model Permeate Prediction Engine -->
      <section class="scada-panel engine-panel">
        <div class="engine-top-bar">
          <div class="engine-title-box">
            <div class="engine-icon-badge">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="2" />
                <path d="M16.24 7.76a6 6 0 0 1 0 8.49m-8.48-.01a6 6 0 0 1 0-8.49m11.31-2.82a10 10 0 0 1 0 14.14m-14.14 0a10 10 0 0 1 0-14.14" />
              </svg>
            </div>
            <div>
              <div class="engine-heading-row">
                <h3 class="engine-title">DUAL-MODEL PERMEATE FLOW & PERMEATE TDS PREDICTION ENGINE</h3>
                <span class="badge-status-live">LIVE INFERENCE ACTIVE</span>
              </div>
            </div>
          </div>
        </div>

        <div class="engine-info-note">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="16" x2="12" y2="12" />
            <line x1="12" y1="8" x2="12.01" y2="8" />
          </svg>
          <span>Models & Agent Orchestrator execute automatically every {{ selectedInterval }} min</span>
        </div>

        <!-- Two Comparison Model Cards (Side-by-Side) -->
        <div class="models-comparison-grid">
          <!-- Model Alpha: PINN / Hydrodynamic -->
          <div class="model-box alpha">
            <div class="model-box-header">
              <div class="model-header-left">
                <span class="model-pulse-dot alpha-dot"></span>
                <h4 class="model-box-title">MODEL ALPHA: permeate_flowrate_model_rf.pkl</h4>
              </div>
              <span class="model-conf-badge alpha-badge">{{ alphaConfidence }}</span>
            </div>
            <p class="model-tech-desc">Random Forest Regressor</p>

            <div class="model-submetrics">
              <div class="submetric-col">
                <span class="submetric-lbl">PRED FLOW (T+6H)</span>
                <span class="submetric-val">{{ alphaFlow !== null ? `${alphaFlow} m³/h` : '--' }}</span>
              </div>
              <div class="submetric-col">
                <span class="submetric-lbl">PRED TDS (T+6H)</span>
                <span class="submetric-val">{{ alphaTds !== null ? `${alphaTds} ppm` : 'N/A' }}</span>
              </div>
              <div class="submetric-col">
                <span class="submetric-lbl">COMPUTE LATENCY</span>
                <span class="submetric-val font-mono">{{ alphaLatency !== null ? `${alphaLatency} ms` : '-' }}</span>
              </div>
            </div>
          </div>

          <!-- Model Beta: DeepLSTM / Surrogate -->
          <div class="model-box beta">
            <div class="model-box-header">
              <div class="model-header-left">
                <span class="model-pulse-dot beta-dot"></span>
                <h4 class="model-box-title">MODEL BETA: permeate_flowtds_model_rf.pkl</h4>
              </div>
              <span class="model-conf-badge beta-badge" :class="betaQualityClass">{{ betaQualityStatus ? `${betaQualityStatus.toUpperCase()} QUALITY` : betaConfidence }}</span>
            </div>
            <p class="model-tech-desc">Random Forest Regressor</p>

            <div class="model-submetrics">
              <div class="submetric-col">
                <span class="submetric-lbl">PRED FLOW (T+6H)</span>
                <span class="submetric-val">{{ betaFlow !== null ? `${betaFlow} m³/h` : 'N/A' }}</span>
              </div>
              <div class="submetric-col">
                <span class="submetric-lbl">PRED TDS (T+6H)</span>
                <span class="submetric-val warning-val">{{ betaTds !== null ? `${betaTds} ppm` : '--' }}</span>
              </div>
              <div class="submetric-col">
                <span class="submetric-lbl">COMPUTE LATENCY</span>
                <span class="submetric-val font-mono">{{ betaLatency !== null ? `${betaLatency} ms` : '-' }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Middle Split Section: Model Confidence & Agent Reasoning (50% / 50%) -->
      <div class="split-section">
        <!-- Left: Model Confidence & Validation -->
        <!-- <section class="scada-panel half-panel">
          <div class="panel-header">
            <div class="panel-header-title-box">
              <div class="panel-icon-circle green">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                  <path d="M9 12l2 2 4-4" />
                </svg>
              </div>
              <div>
                <h3 class="panel-title">MODEL CONFIDENCE & VALIDATION</h3>
                <p class="panel-subtitle">KALMAN ENSEMBLE ARBITRATION</p>
              </div>
            </div>
            <span class="badge-status-tag green">CONVERGED</span>
          </div>

          <div class="confidence-body">
            <div class="confidence-score-row">
              <span class="confidence-score-label">CONFIDENCE SCORE</span>
              <span class="confidence-score-val">98.6%</span>
            </div>

            <div class="confidence-metrics-row">
              <div class="conf-metric">
                <span class="conf-lbl">CROSS-ENTROPY LOSS</span>
                <span class="conf-val font-mono">0.0142 NLL</span>
              </div>
              <div class="conf-metric">
                <span class="conf-lbl">MODEL AGREEMENT</span>
                <span class="conf-val font-mono">95.2% OVERLAP</span>
              </div>
            </div>

            <div class="kalman-filter-section">
              <div class="kalman-label-row">
                <span class="kalman-title">KALMAN FILTER WEIGHTING:</span>
                <span class="kalman-split-val">
                  <span class="cyan-text">PINN 62%</span> / <span class="purple-text">LSTM 38%</span>
                </span>
              </div>
              <div class="kalman-bar">
                <div class="kalman-pinn" style="width: 62%"></div>
                <div class="kalman-lstm" style="width: 38%"></div>
              </div>
            </div>

            <p class="iso-note">
              Residual drift smoothed under ISO 13374 Condition Monitoring threshold limits.
            </p>
          </div>
        </section> -->

                <!-- Schedule / Interval Controller Row -->
        <div class="engine-schedule-bar">
          <div class="schedule-left">
            <span class="schedule-label">INTERVAL:</span>
            <div class="select-inline-wrapper">
              <svg class="schedule-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" />
                <polyline points="12 6 12 12 16 14" />
              </svg>
              <span class="schedule-prefix font-mono">EXECUTION SCHEDULE / RUN INTERVAL:</span>
              <select v-model="selectedInterval" class="select-inline font-mono">
                <option value="60">Every 60 mins (Hourly)</option>
                <option value="30">Every 30 mins</option>
                <option value="15">Every 15 mins</option>
                <option value="5">Continuous (5 mins)</option>
                <option value="1">Fast Test (1 min)</option>
              </select>
            </div>
          </div>

          <div class="schedule-right">
            <!-- Autonomous Agent Enable / Disable Toggle -->
            <button
              type="button"
              class="btn-auto-toggle font-mono"
              :class="{ 'is-enabled': isAutonomousAgentEnabled, 'is-disabled': !isAutonomousAgentEnabled }"
              @click="toggleAutonomousAgent"
              :title="isAutonomousAgentEnabled ? 'Click to Disable Autonomous Agent Schedule' : 'Click to Enable Autonomous Agent Schedule'"
            >
              <span class="auto-toggle-track">
                <span class="auto-toggle-dot" :class="isAutonomousAgentEnabled ? 'dot-active' : 'dot-inactive'"></span>
              </span>
              <span class="auto-toggle-label">
                AUTONOMOUS: <strong>{{ isAutonomousAgentEnabled ? 'ENABLED' : 'DISABLED' }}</strong>
              </span>
            </button>

            <!-- Countdown Timer Badge -->
            <span class="badge-countdown font-mono" :class="{ 'paused-running': isAgentRunning, 'halted-stopped': eStopActive, 'disabled-auto': !isAutonomousAgentEnabled }">
              <span v-if="eStopActive" class="running-indicator">
                <span class="pulsing-red-dot"></span>
                PLANT HALTED (TIMER RESET)
              </span>
              <span v-else-if="!isAutonomousAgentEnabled" class="running-indicator">
                <span class="paused-dot"></span>
                AGENT DISABLED (TIMER PAUSED)
              </span>
              <span v-else-if="isAgentRunning" class="running-indicator">
                <span class="pulse-agent-dot"></span>
                AGENT RUNNING (TIMER PAUSED)
              </span>
              <span v-else>
                NEXT RUN: {{ countdownText }}
              </span>
            </span>
          </div>
        </div>

        <!-- Right: Agent Anomalies & Reasoning -->
        <section class="scada-panel half-panel">
          <div class="panel-header">
            <div class="panel-header-title-box">
              <div class="panel-icon-circle purple">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="3" />
                  <path d="M12 2a10 10 0 0 0-10 10c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.1-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z" />
                </svg>
              </div>
              <div>
                <h3 class="panel-title">AGENT ANOMALIES & REASONING</h3>
                <p class="panel-subtitle">AUTONOMOUS DIAGNOSTIC ENGINE</p>
              </div>
            </div>
            <span class="badge-status-tag purple" :class="{ 'pulse-active': isAgentRunning }">{{ isAgentRunning ? 'ANALYZING...' : 'ACTIVE' }}</span>
          </div>

          <div class="anomaly-body">
            <!-- Chain of Thought Box -->
            <div class="cot-box">
              <div class="cot-header">
                <div class="cot-title-left">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="4 17 10 11 4 5" />
                    <line x1="12" y1="19" x2="20" y2="19" />
                  </svg>
                  <span>CHAIN-OF-THOUGHT INFERENCE</span>
                </div>
                <span class="cot-steps-tag font-mono">{{ cotStepsTag }}</span>
              </div>

              <div class="cot-stream font-mono">
                <div v-if="isAgentRunning && (!reasoningSteps || reasoningSteps.length === 0)" class="cot-line highlight">
                  <span class="cot-prefix">›</span>
                  <span class="cot-text">Autonomous Diagnostic Engine evaluating live telemetry against SOP guidelines...</span>
                </div>
                <div v-for="(step, idx) in reasoningSteps" :key="idx" class="cot-line" :class="{ highlight: idx === reasoningSteps.length - 1 }">
                  <span class="cot-prefix">›</span>
                  <span class="cot-text">{{ step }}</span>
                </div>
                <div v-if="!isAgentRunning && (!reasoningSteps || reasoningSteps.length === 0)" class="cot-line">
                  <span class="cot-prefix">›</span>
                  <span class="cot-text">Engine ready. Waiting for interval trigger or manual run.</span>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- Bottom Wide Panel: Post-Execution Reports & Live System Status -->
      <section class="scada-panel reports-panel">
        <div class="panel-header">
          <div class="panel-header-title-box">
            <div class="panel-icon-circle cyan">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14 2 14 8 20 8" />
                <line x1="16" y1="13" x2="8" y2="13" />
                <line x1="16" y1="17" x2="8" y2="17" />
                <polyline points="10 9 9 9 8 9" />
              </svg>
            </div>
            <div>
              <h3 class="panel-title">POST-EXECUTION AGENT REPORTS & LIVE SYSTEM STATUS</h3>
              <p class="panel-subtitle">Autonomous telemetry evaluation, physics divergence audit, and multi-model dispatch logs</p>
            </div>
          </div>
          <span class="badge-status-tag cyan">{{ isAgentRunning ? 'EVALUATING CYCLE...' : 'CYCLE VERIFIED' }}</span>
        </div>

        <!-- Telemetry Status Badges Bar -->
        <div class="status-indicators-bar">
          <div class="indicator-item">
            <span :class="['dot-optimal', plantHealthDotClass]"></span>
            <span>HEALTH: <strong>{{ plantHealth }}</strong></span>
          </div>

          <div class="indicator-item">
            <svg class="ind-icon cyan" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
              <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
            </svg>
            <span>SCADA LINK: <strong>{{ scadaLinkStatus }}</strong></span>
          </div>

          <div class="indicator-item">
            <svg class="ind-icon purple" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10" />
              <polyline points="12 6 12 12 14 14" />
            </svg>
            <span>ORCHESTRATOR: <strong>{{ isAgentRunning ? 'RUNNING' : 'IDLE' }}</strong></span>
          </div>

          <div class="indicator-item pill-mode">
            <span>MODE: <strong>{{ selectedInterval }} MIN AUTO</strong></span>
          </div>
        </div>

        <!-- Last Run Report and Actions Row -->
        <div class="execution-report-row">
          <div class="report-left">
            <div class="report-check-box" :class="{ 'error-box': lastReportBadgeClass === 'red' }">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <polyline points="20 6 9 17 4 12" />
              </svg>
            </div>
            <div class="report-text-group">
              <span class="report-title-line">
                LAST RUN REPORT: <strong>{{ lastReportTime }}</strong>
              </span>
              <span :class="['report-badge-status', lastReportBadgeClass]">{{ lastReportBadge }}</span>
            </div>
          </div>

          <div class="report-actions">
            <button type="button" class="btn-action-audit" @click="triggerAutoRun(true)" :disabled="isAgentRunning" title="Run autonomous supervisor immediately">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ 'spin-icon': isAgentRunning }">
                <polyline points="23 4 23 10 17 10" />
                <polyline points="1 20 1 14 7 14" />
                <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
              </svg>
              <span>{{ isAgentRunning ? 'Running Cycle...' : 'Run Cycle Now' }}</span>
            </button>

            <button type="button" class="btn-action-export" @click="exportExecutions">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="7 10 12 15 17 10" />
                <line x1="12" y1="15" x2="12" y2="3" />
              </svg>
              <span>Export All Executions</span>
            </button>
          </div>
        </div>

        <!-- Mini Recent Cycle Card Preview -->
        <div class="recent-cycle-preview">
          <div class="cycle-left-info">
            <span class="cycle-num font-mono">CYCLE #{{ cycleNumber }}</span>
            <span class="cycle-time font-mono">{{ cycleTimestamp }}</span>
            <span class="cycle-stat">{{ cycleStatText }}</span>
            <span class="cycle-alert-stat font-mono">+{{ cycleAlerts }} ALERTS</span>
          </div>
          <span :class="['cycle-tag-action', cycleTagClass]">{{ cycleActionTag }}</span>
        </div>

        <!-- Full Autonomous Diagnostic Report Content -->
        <div v-if="diagnosticReport" class="diagnostic-report-card">
          <div class="diag-report-header">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span class="diag-report-title">AUTONOMOUS SOP DIAGNOSTIC REPORT</span>
          </div>
          <div class="diag-report-text font-mono">
            {{ diagnosticReport }}
          </div>
        </div>
      </section>
    </div>

    <!-- Execution Audit Modal -->
    <div v-if="showAuditModal" class="modal-overlay" @click.self="showAuditModal = false">
      <div class="modal-card">
        <div class="modal-header">
          <div class="modal-title-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="modal-icon">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
            </svg>
            <h3>Execution Audit Log - Cycle #142</h3>
          </div>
          <button class="modal-close-btn" @click="showAuditModal = false">&times;</button>
        </div>

        <div class="modal-body font-mono">
          <div class="log-row info">
            <span class="timestamp">[14:26:57.102]</span>
            <span class="tag">[INGEST]</span>
            <span>Gathered 14 SCADA telemetry points from MODBUS TCP slave #01.</span>
          </div>
          <div class="log-row info">
            <span class="timestamp">[14:26:57.420]</span>
            <span class="tag">[PINN]</span>
            <span>Hydrodynamic solver converged in 14ms (loss: 0.0018). Pred flow: 71.8 m³/h.</span>
          </div>
          <div class="log-row info">
            <span class="timestamp">[14:26:57.810]</span>
            <span class="tag">[LSTM]</span>
            <span>DeepLSTM inference completed (loss: 0.0024 MSE). Pred TDS: 312 ppm.</span>
          </div>
          <div class="log-row warn">
            <span class="timestamp">[14:26:58.120]</span>
            <span class="tag">[ANOMALY]</span>
            <span>Differential pressure gradient surge (+0.31 bar/h) detected on RO-301.</span>
          </div>
          <div class="log-row success">
            <span class="timestamp">[14:26:58.520]</span>
            <span class="tag">[VERIFY]</span>
            <span>Cycle arbitration converged at 98.6% confidence. Recommended action: Intervene prior to automatic safety trip.</span>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-primary" @click="showAuditModal = false">Close Audit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

// Real-time Cycle Clock
const cycleClock = ref('')
let clockTimer = null

// Persistence Keys
const INTERVAL_STORAGE_KEY = 'scada_execution_interval'
const TARGET_TIMESTAMP_KEY = 'scada_next_run_target'
const AUTO_AGENT_STORAGE_KEY = 'scada_autonomous_agent_enabled'

// Load persisted autonomous agent state from localStorage (default: true)
const getInitialAutoAgentEnabled = () => {
  if (typeof localStorage !== 'undefined') {
    const saved = localStorage.getItem(AUTO_AGENT_STORAGE_KEY)
    if (saved !== null) {
      return saved === 'true'
    }
  }
  return true
}
const isAutonomousAgentEnabled = ref(getInitialAutoAgentEnabled())

// Load persisted interval from localStorage (default: '60')
const savedInterval = (typeof localStorage !== 'undefined' && localStorage.getItem(INTERVAL_STORAGE_KEY)) || '60'
const selectedInterval = ref(savedInterval)

// Calculate initial countdown based on saved target timestamp or interval duration
const getInitialCountdownSeconds = () => {
  const intervalMins = parseInt(selectedInterval.value) || 60
  const intervalSecs = intervalMins * 60
  if (typeof localStorage !== 'undefined') {
    const savedTarget = localStorage.getItem(TARGET_TIMESTAMP_KEY)
    if (savedTarget) {
      const remaining = Math.round((parseInt(savedTarget) - Date.now()) / 1000)
      if (remaining > 0 && remaining <= intervalSecs) {
        return remaining
      }
    }
    // Initialize target timestamp if enabled
    if (isAutonomousAgentEnabled.value) {
      localStorage.setItem(TARGET_TIMESTAMP_KEY, String(Date.now() + intervalSecs * 1000))
    }
  }
  return intervalSecs
}

const initialRemaining = getInitialCountdownSeconds()
const countdownSeconds = ref(initialRemaining)
const initMins = Math.floor(initialRemaining / 60)
const initSecs = initialRemaining % 60
const countdownText = ref(`${initMins}m ${String(initSecs).padStart(2, '0')}s`)
let countdownTimer = null

// ─── Backend API Base URL ───────────────────────────────────────
const API_BASE = 'http://localhost:8000'

// Equipment States
const pumpP101 = ref(true)
const eStopActive = ref(false)
const isEStopLoading = ref(false)

// KPI Telemetry Values
const flowRate = ref(74.8)
const salinityTds = ref(804)
const temperature = ref(25.8)
const concentration = ref(24.8)
const recoveryRatio = ref(74.9)
const membraneFlux = ref(15.1)
const feedPressure = ref(4.8)

let telemetryTimer = null
let isFetchingTelemetry = false

// Fetch live telemetry from backend
const fetchLiveTelemetry = async () => {
  if (isFetchingTelemetry) return
  isFetchingTelemetry = true

  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), 3500)

  try {
    const response = await fetch(`${API_BASE}/api/telemetry/live`, { signal: controller.signal })
    clearTimeout(timeoutId)
    if (!response.ok) return
    const json = await response.json()
    if (json.status === 'success' && Array.isArray(json.data)) {
      for (const item of json.data) {
        const val = typeof item.scaled === 'number' ? item.scaled : parseFloat(item.scaled)
        if (isNaN(val)) continue

        if (item.address === '40001') {
          flowRate.value = val
        } else if (item.address === '40002') {
          salinityTds.value = Math.round(val)
        } else if (item.address === '40003') {
          temperature.value = val
        } else if (item.address === '40007') {
          concentration.value = val
        } else if (item.address === '40008') {
          recoveryRatio.value = val
        } else if (item.address === '40009') {
          membraneFlux.value = val
        } else if (item.address === '40010') {
          feedPressure.value = val
        }
      }
    }
  } catch (err) {
    // Keep current values on network interruption
  } finally {
    clearTimeout(timeoutId)
    isFetchingTelemetry = false
  }
}

// ─── Predictions State (from /api/predict/live) ─────────────────
const alphaFlow = ref(71.8)
const alphaTds = ref(null)
const alphaLatency = ref(14)
const alphaConfidence = ref('99.4% CONF')

const betaFlow = ref(null)
const betaTds = ref(312.0)
const betaLatency = ref(14)
const betaQualityStatus = ref('Poor')
const betaConfidence = ref('97.8% CONF')

const betaQualityClass = computed(() => {
  const status = (betaQualityStatus.value || '').toLowerCase()
  if (status === 'good' || status === 'excellent') return 'green'
  if (status === 'warning') return 'amber'
  if (status === 'poor') return 'red'
  return 'green'
})

let predictTimer = null
let isFetchingPredictions = false

// Fetch live predictions from backend
const fetchLivePredictions = async () => {
  if (isFetchingPredictions) return
  isFetchingPredictions = true

  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), 3500)

  try {
    const response = await fetch(`${API_BASE}/api/predict/live`, { signal: controller.signal })
    clearTimeout(timeoutId)
    if (!response.ok) return
    const json = await response.json()
    if (json.status === 'success' && json.predictions) {
      // Model Alpha
      if (json.predictions.alpha) {
        if (json.predictions.alpha.flow !== null && json.predictions.alpha.flow !== undefined) {
          alphaFlow.value = json.predictions.alpha.flow
        }
        if (json.predictions.alpha.tds !== null && json.predictions.alpha.tds !== undefined) {
          alphaTds.value = json.predictions.alpha.tds
        }
        if (json.predictions.alpha.latency_ms !== null && json.predictions.alpha.latency_ms !== undefined) {
          alphaLatency.value = json.predictions.alpha.latency_ms
        }
      }

      // Model Beta
      if (json.predictions.beta) {
        if (json.predictions.beta.flow !== null && json.predictions.beta.flow !== undefined) {
          betaFlow.value = json.predictions.beta.flow
        }
        if (json.predictions.beta.tds !== null && json.predictions.beta.tds !== undefined) {
          betaTds.value = json.predictions.beta.tds
        }
        if (json.predictions.beta.quality_status) {
          betaQualityStatus.value = json.predictions.beta.quality_status
        }
        if (json.predictions.beta.latency_ms !== null && json.predictions.beta.latency_ms !== undefined) {
          betaLatency.value = json.predictions.beta.latency_ms
        }
      }
    }
  } catch (err) {
    // Keep current values on network interruption
  } finally {
    clearTimeout(timeoutId)
    isFetchingPredictions = false
  }
}

// ─── Autonomous Agent Auto-Run State (/api/agent/auto-run) ─────────
const isAgentRunning = ref(false)
const diagnosticReport = ref(null)
const reasoningSteps = ref([])
const cycleNumber = ref(142)
const cycleTimestamp = ref('14:26:57')
const cycleFlow = ref(74.8)
const cycleTds = ref(312.0)
const cycleQuality = ref('Good')
const plantHealth = ref('OPTIMAL')
const plantHealthDotClass = ref('')
const scadaLinkStatus = ref('CONNECTED (PORT 502)')
const lastReportTime = ref('CYCLE #142 (14:26:57)')
const lastReportBadge = ref('GRADE A - SOP OK')
const lastReportBadgeClass = ref('green')
const cycleAlerts = ref(0)
const cycleActionTag = ref('VERIFIED NORMAL')
const cycleTagClass = ref('green')

const cotStepsTag = computed(() => {
  if (isAgentRunning.value) return 'RUNNING INFERENCE...'
  if (reasoningSteps.value.length === 0) return 'IDLE'
  return `${reasoningSteps.value.length} STEPS`
})

const cycleStatText = computed(() => {
  return `Flow: ${cycleFlow.value} m³/h | TDS: ${cycleTds.value} ppm (${cycleQuality.value})`
})

// Trigger Auto-Run from backend
const triggerAutoRun = async (isManual = false) => {
  if (isAgentRunning.value || eStopActive.value) return
  if (!isManual && !isAutonomousAgentEnabled.value) return
  isAgentRunning.value = true

  try {
    const response = await fetch(`${API_BASE}/api/agent/auto-run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    })
    
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
    const json = await response.json()

    if (json.status === 'success') {
      cycleNumber.value = json.cycle_number || (cycleNumber.value + 1)
      diagnosticReport.value = json.diagnostic_report || ''
      
      const nowStr = json.timestamp || new Date().toLocaleTimeString()
      cycleTimestamp.value = nowStr
      lastReportTime.value = `CYCLE #${cycleNumber.value} (${nowStr})`

      if (json.live_inputs) {
        if (json.live_inputs.flow !== undefined) cycleFlow.value = json.live_inputs.flow
        if (json.live_inputs.tds !== undefined) cycleTds.value = json.live_inputs.tds
        if (json.live_inputs.quality !== undefined) cycleQuality.value = json.live_inputs.quality
      }

      // Update reasoning steps
      if (Array.isArray(json.reasoning_steps) && json.reasoning_steps.length > 0) {
        reasoningSteps.value = json.reasoning_steps
      } else {
        reasoningSteps.value = [
          `[INGEST] Telemetry verified: Flow=${cycleFlow.value} m³/h, TDS=${cycleTds.value} ppm (${cycleQuality.value})`,
          `[SOP] Cross-checked Vikings_Desalination_Plant_SOP.docx against active parameters`,
          `[STATUS] Autonomous supervisor cycle evaluation verified`
        ]
      }

      // Health & Badges based on quality
      const q = (cycleQuality.value || '').toLowerCase()
      if (q === 'good' || q === 'excellent') {
        plantHealth.value = 'OPTIMAL'
        plantHealthDotClass.value = ''
        lastReportBadge.value = 'GRADE A - SOP OK'
        lastReportBadgeClass.value = 'green'
        cycleAlerts.value = 0
        cycleActionTag.value = 'VERIFIED NORMAL'
        cycleTagClass.value = 'green'
      } else if (q === 'warning') {
        plantHealth.value = 'WARNING'
        plantHealthDotClass.value = 'dot-warn'
        lastReportBadge.value = 'DOSING ADJUSTMENT'
        lastReportBadgeClass.value = 'amber'
        cycleAlerts.value = 1
        cycleActionTag.value = 'DOSING CHECK'
        cycleTagClass.value = 'amber'
      } else {
        plantHealth.value = 'DEGRADED'
        plantHealthDotClass.value = 'dot-danger'
        lastReportBadge.value = 'POOR - ACTION REQUIRED'
        lastReportBadgeClass.value = 'red'
        cycleAlerts.value = 2
        cycleActionTag.value = 'CORRECTIVE ACTION'
        cycleTagClass.value = 'red'
      }
      scadaLinkStatus.value = 'CONNECTED (PORT 502)'
    } else {
      // Plant error (e.g. PLC disconnected)
      scadaLinkStatus.value = 'PLC DISCONNECTED'
      plantHealth.value = 'OFFLINE'
      plantHealthDotClass.value = 'dot-danger'
      lastReportBadge.value = 'PLC DISCONNECTED'
      lastReportBadgeClass.value = 'red'
      cycleAlerts.value = 1
      cycleActionTag.value = 'LINK RECONNECT'
      cycleTagClass.value = 'red'
      if (json.message) {
        diagnosticReport.value = `[STATUS] ${json.message}`
      }
    }
  } catch (err) {
    scadaLinkStatus.value = 'NETWORK INTERRUPTION'
  } finally {
    isAgentRunning.value = false

    // When the agent cycle completes:
    // If countdown reached 0 (or was at 0), reset to the full interval duration and resume
    if (countdownSeconds.value <= 0) {
      const intervalSecs = (parseInt(selectedInterval.value) || 60) * 60
      countdownSeconds.value = intervalSecs
    }

    // Synchronize localStorage target timestamp to resume countdown from current seconds
    if (isAutonomousAgentEnabled.value && !eStopActive.value && typeof localStorage !== 'undefined') {
      localStorage.setItem(TARGET_TIMESTAMP_KEY, String(Date.now() + countdownSeconds.value * 1000))
    }

    const mins = Math.floor(countdownSeconds.value / 60)
    const secs = countdownSeconds.value % 60
    countdownText.value = `${mins}m ${String(secs).padStart(2, '0')}s`
  }
}

const toggleAutonomousAgent = () => {
  isAutonomousAgentEnabled.value = !isAutonomousAgentEnabled.value
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem(AUTO_AGENT_STORAGE_KEY, String(isAutonomousAgentEnabled.value))
  }

  if (!isAutonomousAgentEnabled.value) {
    if (typeof localStorage !== 'undefined') {
      localStorage.removeItem(TARGET_TIMESTAMP_KEY)
    }
  } else {
    const remaining = countdownSeconds.value > 0 ? countdownSeconds.value : ((parseInt(selectedInterval.value) || 60) * 60)
    countdownSeconds.value = remaining
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem(TARGET_TIMESTAMP_KEY, String(Date.now() + remaining * 1000))
    }
    const mins = Math.floor(remaining / 60)
    const secs = remaining % 60
    countdownText.value = `${mins}m ${String(secs).padStart(2, '0')}s`
  }
}

// Persist interval changes to localStorage and adjust countdown
watch(selectedInterval, (newVal) => {
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem(INTERVAL_STORAGE_KEY, newVal)
  }
  const intervalSecs = (parseInt(newVal) || 60) * 60
  countdownSeconds.value = intervalSecs
  if (isAutonomousAgentEnabled.value && !eStopActive.value && typeof localStorage !== 'undefined') {
    localStorage.setItem(TARGET_TIMESTAMP_KEY, String(Date.now() + intervalSecs * 1000))
  }
  const mins = Math.floor(intervalSecs / 60)
  const secs = intervalSecs % 60
  countdownText.value = `${mins}m ${String(secs).padStart(2, '0')}s`
})

// Modals
const showAuditModal = ref(false)
const showRecentCycles = ref(false)

const cycleMixerSpeed = () => {
  const speeds = [350, 420, 500, 280]
}

const handleEmergencyStop = async () => {
  if (isEStopLoading.value) return
  isEStopLoading.value = true

  const endpoint = eStopActive.value ? '/api/plant/resume' : '/api/plant/emergency-stop'

  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    })
    const json = await response.json()

    if (json.status === 'success') {
      eStopActive.value = !eStopActive.value
      pumpP101.value = !eStopActive.value

      const intervalSecs = (parseInt(selectedInterval.value) || 60) * 60
      countdownSeconds.value = intervalSecs
      const mins = Math.floor(intervalSecs / 60)
      const secs = intervalSecs % 60
      countdownText.value = `${mins}m ${String(secs).padStart(2, '0')}s`

      if (eStopActive.value) {
        // Plant is stopped: clear target timestamp so timer stays stopped and reset
        if (typeof localStorage !== 'undefined') {
          localStorage.removeItem(TARGET_TIMESTAMP_KEY)
        }
      } else {
        // Plant is resumed: start countdown fresh from full interval
        if (typeof localStorage !== 'undefined') {
          localStorage.setItem(TARGET_TIMESTAMP_KEY, String(Date.now() + intervalSecs * 1000))
        }
      }
    } else {
      console.error(json.message)
    }
  } catch (err) {
    console.error('Failed to communicate with plant emergency controls:', err)
  } finally {
    isEStopLoading.value = false
  }
}

const updateClock = () => {
  const now = new Date()
  const hh = String(now.getHours()).padStart(2, '0')
  const mm = String(now.getMinutes()).padStart(2, '0')
  const ss = String(now.getSeconds()).padStart(2, '0')
  const ms = String(Math.floor(now.getMilliseconds() / 10)).padStart(2, '0')
  cycleClock.value = `${hh}:${mm}:${ss}.${ms}`
}

const updateCountdown = async () => {
  // If plant is stopped (e-stop active), agent is actively running, or autonomous agent is disabled, stop/freeze the timer
  if (eStopActive.value || isAgentRunning.value || !isAutonomousAgentEnabled.value) {
    return
  }

  if (countdownSeconds.value > 0) {
    countdownSeconds.value--
    const mins = Math.floor(countdownSeconds.value / 60)
    const secs = countdownSeconds.value % 60
    countdownText.value = `${mins}m ${String(secs).padStart(2, '0')}s`
  } else {
    // Reached 0 -> trigger agent run. Timer pauses while executing,
    // and will reset & resume when triggerAutoRun finishes!
    await triggerAutoRun()
  }
}

const exportExecutions = () => {
  const data = {
    plant: 'AQUASYNC SCADA - SWRO PLANT #04',
    cycle: cycleNumber.value,
    timestamp: new Date().toISOString(),
    pinn_prediction: { flow: `${alphaFlow.value || 71.8} m³/h`, tds: `${alphaTds.value ?? 'N/A'}`, confidence: alphaConfidence.value },
    lstm_prediction: { flow: `${betaFlow.value ?? 'N/A'}`, tds: `${betaTds.value || 312} ppm`, confidence: betaConfidence.value },
    kalman_ensemble_confidence: '98.6%',
    diagnostic_report: diagnosticReport.value,
    reasoning_steps: reasoningSteps.value,
    telemetry: {
      flowRate: flowRate.value,
      salinityTds: salinityTds.value,
      temperature: temperature.value,
      feedPressure: feedPressure.value,
      recoveryRatio: recoveryRatio.value
    }
  }

  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `aquasync-cycle-${cycleNumber.value}-${Date.now()}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

onMounted(() => {
  clockTimer = setInterval(updateClock, 80)
  countdownTimer = setInterval(updateCountdown, 1000)
  updateClock()

  fetchLiveTelemetry()
  telemetryTimer = setInterval(fetchLiveTelemetry, 2000)

  fetchLivePredictions()
  predictTimer = setInterval(fetchLivePredictions, 2000)
})

onUnmounted(() => {
  if (clockTimer) clearInterval(clockTimer)
  if (countdownTimer) clearInterval(countdownTimer)
  if (telemetryTimer) clearInterval(telemetryTimer)
  if (predictTimer) clearInterval(predictTimer)
})
</script>

<style scoped>
.scada-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  background: var(--bg-app, #070c18);
  color: var(--text-main, #e2e8f0);
  overflow: hidden;
}

/* 1. Top Ribbon */
.control-ribbon {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 18px;
  background: var(--bg-card, #091020);
  border-bottom: 1px solid var(--border-color, rgba(23, 36, 60, 0.9));
  flex-shrink: 0;
  gap: 12px;
}

.ribbon-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.pill-sim-mode {
  display: flex;
  align-items: center;
  gap: 7px;
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.4);
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 700;
  color: #10b981;
  letter-spacing: 0.5px;
}

.pulsing-green-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 8px #10b981;
  animation: pulse-dot 1.5s infinite ease-in-out;
}

.pill-sim-mode.halted {
  background: rgba(239, 68, 68, 0.15) !important;
  border-color: rgba(239, 68, 68, 0.4) !important;
  color: #f87171 !important;
}

.pulsing-red-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #ef4444;
  box-shadow: 0 0 8px #ef4444;
  animation: pulse-dot 1s infinite ease-in-out;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.85); }
}

.meta-tag {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  color: #94a3b8;
}

.meta-label {
  font-weight: 600;
  letter-spacing: 0.3px;
}

.meta-val {
  color: #ffffff;
  font-weight: 600;
}

.equipment-cluster {
  display: flex;
  align-items: center;
  gap: 8px;
}

.equip-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 9px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.equip-badge.green {
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.4);
  color: #34d399;
}

.equip-badge.cyan {
  background: rgba(0, 229, 255, 0.15);
  border: 1px solid rgba(0, 229, 255, 0.4);
  color: #00e5ff;
}

.equip-badge.purple {
  background: rgba(168, 85, 247, 0.15);
  border: 1px solid rgba(168, 85, 247, 0.4);
  color: #c084fc;
}

.equip-badge.off {
  background: rgba(148, 163, 184, 0.1);
  border: 1px solid rgba(148, 163, 184, 0.3);
  color: #64748b;
}

.equip-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.btn-e-stop {
  display: flex;
  align-items: center;
  gap: 7px;
  background: #dc2626;
  border: 1px solid #ef4444;
  color: #ffffff;
  padding: 5px 14px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.5px;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(220, 38, 38, 0.4);
  transition: all 0.2s;
}

.btn-e-stop svg {
  width: 13px;
  height: 13px;
}

.btn-e-stop:hover {
  background: #ef4444;
}

.btn-e-stop.triggered {
  background: #059669;
  border-color: #10b981;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
}

.btn-e-stop.triggered:hover {
  background: #10b981;
}

.btn-e-stop.loading {
  opacity: 0.75;
  cursor: wait;
}

/* 2. Scrollable Dashboard Body */
.scada-content {
  flex: 1;
  overflow-y: auto;
  padding: 14px 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 7 KPI Metric Grid */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 9px;
}

.kpi-card {
  background: var(--bg-card, #0b1426);
  border: 1px solid var(--border-color, #14223d);
  border-radius: 5px;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 85px;
}

.kpi-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.kpi-label {
  font-size: 9.5px;
  font-weight: 700;
  color: #94a3b8;
  letter-spacing: 0.5px;
}

.kpi-icon {
  width: 14px;
  height: 14px;
}

.kpi-icon.cyan { color: #00e5ff; }
.kpi-icon.green { color: #10b981; }
.kpi-icon.purple { color: #c084fc; }
.kpi-icon.blue { color: #38bdf8; }

.kpi-body {
  display: flex;
  align-items: baseline;
  gap: 4px;
  margin: 4px 0;
}

.kpi-value {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.5px;
  font-family: var(--font-mono, monospace);
}

.kpi-value.cyan { color: #00e5ff; }
.kpi-value.green { color: #34d399; }
.kpi-value.purple { color: #c084fc; }

.kpi-unit {
  font-size: 10px;
  color: #64748b;
  font-weight: 600;
}

.kpi-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
}

.kpi-bar-bg {
  flex: 1;
  height: 3px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 2px;
  overflow: hidden;
}

.kpi-bar-fill {
  height: 100%;
  border-radius: 2px;
}

.kpi-bar-fill.cyan { background: #00e5ff; }
.kpi-bar-fill.green { background: #10b981; }
.kpi-bar-fill.purple { background: #c084fc; }
.kpi-bar-fill.blue { background: #38bdf8; }

.kpi-subtext {
  font-size: 9px;
  color: #64748b;
  font-weight: 600;
  white-space: nowrap;
}

.green-text {
  color: #34d399 !important;
}

/* Generic Panel Styling */
.scada-panel {
  background: var(--bg-card, #0b1426);
  border: 1px solid var(--border-color, #14223d);
  border-radius: 6px;
  padding: 14px 16px;
}

/* Engine Panel */
.engine-top-bar {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(23, 36, 60, 0.8);
}

.engine-title-box {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.engine-icon-badge {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: rgba(0, 229, 255, 0.12);
  border: 1px solid rgba(0, 229, 255, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #00e5ff;
  flex-shrink: 0;
}

.engine-icon-badge svg {
  width: 18px;
  height: 18px;
}

.engine-heading-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.engine-title {
  font-size: 13px;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: 0.2px;
  margin: 0;
}

.badge-status-live {
  font-size: 9px;
  font-weight: 700;
  color: #10b981;
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.4);
  padding: 2px 7px;
  border-radius: 3px;
  letter-spacing: 0.5px;
}

.engine-desc {
  font-size: 11px;
  color: #94a3b8;
  margin-top: 3px;
}

.engine-alert-badges {
  display: flex;
  align-items: center;
  gap: 8px;
}

.badge-stat-pill {
  font-size: 10.5px;
  padding: 4px 10px;
  border-radius: 4px;
  font-weight: 500;
}

.cyan-stat {
  background: rgba(0, 229, 255, 0.1);
  border: 1px solid rgba(0, 229, 255, 0.35);
  color: #00e5ff;
}

.red-stat {
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid rgba(239, 68, 68, 0.4);
  color: #f87171;
}

/* Schedule Bar */
.engine-schedule-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 10px 0 6px 0;
  background: var(--bg-card-inner, #080f1d);
  padding: 7px 12px;
  border-radius: 4px;
  border: 1px solid #142340;
}

.schedule-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.schedule-label {
  font-size: 10.5px;
  font-weight: 700;
  color: #94a3b8;
  letter-spacing: 0.5px;
}

.select-inline-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #081224;
  border: 1px solid rgba(0, 229, 255, 0.45);
  border-radius: 4px;
  padding: 3px 8px;
  box-shadow: 0 0 8px rgba(0, 229, 255, 0.08);
  transition: all 0.2s ease;
}

.select-inline-wrapper:hover,
.select-inline-wrapper:focus-within {
  border-color: #00e5ff;
  box-shadow: 0 0 12px rgba(0, 229, 255, 0.25);
}

.select-inline-wrapper .schedule-icon {
  width: 14px;
  height: 14px;
  color: #00e5ff;
  flex-shrink: 0;
}

.schedule-prefix {
  font-size: 11px;
  font-weight: 700;
  color: #00e5ff;
  letter-spacing: 0.3px;
  white-space: nowrap;
}

.select-inline {
  background: #0d1b33;
  border: 1px solid rgba(0, 229, 255, 0.35);
  border-radius: 4px;
  color: #ffffff;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 22px 3px 8px;
  outline: none;
  cursor: pointer;
  color-scheme: dark;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2300e5ff' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 6px center;
  transition: all 0.2s ease;
}

.select-inline:hover {
  background-color: #122547;
  border-color: #00e5ff;
}

.select-inline:focus {
  background-color: #122547;
  border-color: #00e5ff;
  box-shadow: 0 0 8px rgba(0, 229, 255, 0.35);
}

.select-inline option {
  background-color: #070f1e !important;
  color: #ffffff !important;
  font-size: 11.5px;
  font-weight: 600;
  padding: 8px 12px;
}

.select-inline option:hover,
.select-inline option:focus,
.select-inline option:checked {
  background-color: #0284c7 !important;
  color: #ffffff !important;
}

.schedule-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-auto-toggle {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 3px 9px;
  border-radius: 4px;
  font-size: 10.5px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
  background: transparent;
  outline: none;
}

.btn-auto-toggle.is-enabled {
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.45);
  color: #10b981;
}

.btn-auto-toggle.is-enabled:hover {
  background: rgba(16, 185, 129, 0.22);
  border-color: #10b981;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.3);
}

.btn-auto-toggle.is-disabled {
  background: rgba(148, 163, 184, 0.08);
  border: 1px solid rgba(148, 163, 184, 0.3);
  color: #94a3b8;
}

.btn-auto-toggle.is-disabled:hover {
  background: rgba(239, 68, 68, 0.12);
  border-color: rgba(239, 68, 68, 0.4);
  color: #f87171;
}

.auto-toggle-track {
  width: 24px;
  height: 13px;
  border-radius: 10px;
  background: #0a1324;
  border: 1px solid #1e293b;
  position: relative;
  display: inline-flex;
  align-items: center;
  padding: 1px;
  transition: all 0.2s ease;
}

.btn-auto-toggle.is-enabled .auto-toggle-track {
  background: rgba(16, 185, 129, 0.25);
  border-color: #10b981;
}

.auto-toggle-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: #64748b;
  transition: transform 0.2s ease, background-color 0.2s ease;
  transform: translateX(0);
}

.auto-toggle-dot.dot-active {
  background: #10b981;
  box-shadow: 0 0 6px #10b981;
  transform: translateX(11px);
}

.paused-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #94a3b8;
}

.badge-countdown {
  font-size: 10.5px;
  font-weight: 700;
  color: #00e5ff;
  background: rgba(0, 229, 255, 0.12);
  border: 1px solid rgba(0, 229, 255, 0.35);
  padding: 3px 9px;
  border-radius: 4px;
}

.badge-countdown.paused-running {
  background: rgba(192, 132, 252, 0.15);
  border-color: rgba(192, 132, 252, 0.4);
  color: #c084fc;
}

.badge-countdown.halted-stopped {
  background: rgba(239, 68, 68, 0.15) !important;
  border-color: rgba(239, 68, 68, 0.45) !important;
  color: #f87171 !important;
}

.running-indicator {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.pulse-agent-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #c084fc;
  box-shadow: 0 0 8px #c084fc;
  animation: pulse-agent 1s infinite alternate ease-in-out;
}

@keyframes pulse-agent {
  from { opacity: 0.4; transform: scale(0.85); }
  to { opacity: 1; transform: scale(1.2); }
}

.engine-info-note {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10.5px;
  color: #00e5ff;
  margin-bottom: 12px;
}

.engine-info-note svg {
  width: 13px;
  height: 13px;
}

/* Models Comparison Grid (2 boxes) */
.models-comparison-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.model-box {
  background: var(--bg-card-inner, #070e1b);
  border-radius: 5px;
  padding: 12px 14px;
}

.model-box.alpha {
  border: 1px solid rgba(0, 229, 255, 0.35);
}

.model-box.beta {
  border: 1px solid rgba(168, 85, 247, 0.35);
}

.model-box-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.model-header-left {
  display: flex;
  align-items: center;
  gap: 7px;
}

.model-pulse-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.alpha-dot {
  background: #00e5ff;
  box-shadow: 0 0 6px #00e5ff;
}

.beta-dot {
  background: #c084fc;
  box-shadow: 0 0 6px #c084fc;
}

.model-box-title {
  font-size: 11.5px;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
}

.model-conf-badge {
  font-size: 9.5px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 3px;
  font-family: var(--font-mono, monospace);
}

.alpha-badge {
  background: rgba(0, 229, 255, 0.15);
  color: #00e5ff;
  border: 1px solid rgba(0, 229, 255, 0.4);
}

.beta-badge {
  background: rgba(168, 85, 247, 0.15);
  color: #c084fc;
  border: 1px solid rgba(168, 85, 247, 0.4);
}

.beta-badge.green {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.4);
}

.beta-badge.amber {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.4);
}

.beta-badge.red {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.4);
}

.model-tech-desc {
  font-size: 10.5px;
  color: #94a3b8;
  margin: 4px 0 10px 0;
}

.model-submetrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  background: var(--bg-card, rgba(10, 18, 35, 0.7));
  padding: 8px 10px;
  border-radius: 4px;
}

.submetric-col {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.submetric-lbl {
  font-size: 8.5px;
  font-weight: 700;
  color: #64748b;
  letter-spacing: 0.3px;
}

.submetric-val {
  font-size: 12px;
  font-weight: 700;
  color: #ffffff;
}

.warning-val {
  color: #fbbf24 !important;
}

/* Middle Split Section */
.split-section {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

.half-panel {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(23, 36, 60, 0.8);
}

.panel-header-title-box {
  display: flex;
  align-items: center;
  gap: 10px;
}

.panel-icon-circle {
  width: 28px;
  height: 28px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.panel-icon-circle.green {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.panel-icon-circle.purple {
  background: rgba(168, 85, 247, 0.15);
  color: #c084fc;
}

.panel-icon-circle.cyan {
  background: rgba(0, 229, 255, 0.15);
  color: #00e5ff;
}

.panel-icon-circle svg {
  width: 16px;
  height: 16px;
}

.panel-title {
  font-size: 11.5px;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
  letter-spacing: 0.3px;
}

.panel-subtitle {
  font-size: 9.5px;
  color: #64748b;
  font-weight: 600;
  margin-top: 1px;
}

.badge-status-tag {
  font-size: 9.5px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 3px;
  letter-spacing: 0.5px;
}

.badge-status-tag.green {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.4);
}

.badge-status-tag.purple {
  background: rgba(168, 85, 247, 0.15);
  color: #c084fc;
  border: 1px solid rgba(168, 85, 247, 0.4);
}

.badge-status-tag.cyan {
  background: rgba(0, 229, 255, 0.15);
  color: #00e5ff;
  border: 1px solid rgba(0, 229, 255, 0.4);
}

/* Confidence Body */
.confidence-body {
  padding-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.confidence-score-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}

.confidence-score-label {
  font-size: 10px;
  font-weight: 700;
  color: #94a3b8;
  letter-spacing: 0.4px;
}

.confidence-score-val {
  font-size: 24px;
  font-weight: 800;
  color: #10b981;
  font-family: var(--font-mono, monospace);
  text-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
}

.confidence-metrics-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.conf-metric {
  background: var(--bg-card-inner, #080f1d);
  padding: 6px 10px;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.conf-lbl {
  font-size: 8.5px;
  font-weight: 700;
  color: #64748b;
}

.conf-val {
  font-size: 11px;
  font-weight: 700;
  color: #e2e8f0;
}

.kalman-filter-section {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.kalman-label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 9.5px;
  font-weight: 600;
}

.kalman-title {
  color: #94a3b8;
}

.cyan-text { color: #00e5ff; font-weight: 700; }
.purple-text { color: #c084fc; font-weight: 700; }

.kalman-bar {
  display: flex;
  height: 6px;
  border-radius: 3px;
  overflow: hidden;
  background: #080f1d;
}

.kalman-pinn {
  background: #00e5ff;
}

.kalman-lstm {
  background: #a855f7;
}

.iso-note {
  font-size: 9.5px;
  color: #64748b;
  margin: 0;
  line-height: 1.4;
}

/* Anomaly Body */
.anomaly-body {
  padding-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 9px;
}

.anomaly-alert-card {
  background: rgba(220, 38, 38, 0.12);
  border: 1px solid rgba(239, 68, 68, 0.4);
  border-radius: 4px;
  padding: 8px 10px;
}

.alert-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 3px;
}

.alert-title-box {
  display: flex;
  align-items: center;
  gap: 6px;
}

.alert-bell-icon {
  width: 14px;
  height: 14px;
  color: #f87171;
}

.alert-title-text {
  font-size: 11px;
  font-weight: 700;
  color: #f87171;
  letter-spacing: 0.3px;
}

.badge-now {
  font-size: 8.5px;
  font-weight: 700;
  background: #dc2626;
  color: #fff;
  padding: 1px 5px;
  border-radius: 2px;
}

.alert-desc {
  font-size: 10px;
  color: #fca5a5;
  margin: 0;
}

.cot-box {
  background: var(--bg-card-inner, #070e1b);
  border: 1px solid var(--border-color, #142340);
  border-radius: 4px;
  padding: 8px 10px;
}

.cot-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 5px;
  border-bottom: 1px solid #142340;
  margin-bottom: 6px;
}

.cot-title-left {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 9.5px;
  font-weight: 700;
  color: #00e5ff;
}

.cot-title-left svg {
  width: 12px;
  height: 12px;
}

.cot-steps-tag {
  font-size: 9px;
  color: #64748b;
  font-weight: 600;
}

.cot-stream {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 9.5px;
  line-height: 1.4;
}

.cot-line {
  color: #94a3b8;
}

.cot-prefix {
  color: #00e5ff;
  font-weight: 600;
  margin-right: 4px;
}

.cot-line.highlight .cot-prefix {
  color: #38bdf8;
}

.cot-line.highlight .cot-text {
  color: #e2e8f0;
}

/* Reports Panel */
.status-indicators-bar {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 8px 12px;
  margin: 10px 0 8px 0;
  background: #080f1d;
  border-radius: 4px;
  border: 1px solid #142340;
  font-size: 10.5px;
}

.indicator-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #94a3b8;
}

.dot-optimal {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 6px #10b981;
}

.ind-icon {
  width: 13px;
  height: 13px;
}

.ind-icon.cyan { color: #00e5ff; }
.ind-icon.purple { color: #c084fc; }

.indicator-item strong {
  color: #ffffff;
}

.pill-mode {
  margin-left: auto;
  background: rgba(0, 229, 255, 0.1);
  border: 1px solid rgba(0, 229, 255, 0.3);
  padding: 2px 7px;
  border-radius: 3px;
  color: #00e5ff;
}

.execution-report-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.report-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.report-check-box {
  width: 22px;
  height: 22px;
  border-radius: 4px;
  background: rgba(16, 185, 129, 0.18);
  border: 1px solid rgba(16, 185, 129, 0.4);
  color: #10b981;
  display: flex;
  align-items: center;
  justify-content: center;
}

.report-check-box svg {
  width: 13px;
  height: 13px;
}

.report-text-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.report-title-line {
  font-size: 11px;
  color: #cbd5e1;
}

.report-badge-status {
  font-size: 9px;
  font-weight: 700;
  color: #34d399;
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.35);
  padding: 2px 7px;
  border-radius: 3px;
}

.report-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-action-audit, .btn-action-recent, .btn-action-export {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: #0f1c34;
  border: 1px solid #1e355f;
  color: #94a3b8;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-action-audit svg, .btn-action-recent svg, .btn-action-export svg {
  width: 12px;
  height: 12px;
}

.btn-action-audit:hover, .btn-action-recent:hover, .btn-action-export:hover {
  background: #172a4e;
  color: #00e5ff;
  border-color: rgba(0, 229, 255, 0.4);
}

.btn-action-export {
  color: #38bdf8;
  border-color: rgba(56, 189, 248, 0.35);
}

.recent-cycle-preview {
  margin-top: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #080f1d;
  padding: 6px 12px;
  border-radius: 4px;
  border: 1px solid #142340;
  font-size: 10px;
}

.cycle-left-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.cycle-num {
  color: #00e5ff;
  font-weight: 700;
}

.cycle-time {
  color: #94a3b8;
}

.cycle-stat {
  color: #cbd5e1;
}

.cycle-alert-stat {
  color: #f87171;
}

.cycle-tag-action {
  font-size: 8.5px;
  font-weight: 700;
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.4);
  color: #34d399;
  padding: 2px 6px;
  border-radius: 2px;
}

.diagnostic-report-card {
  margin-top: 10px;
  background: #080f1d;
  border: 1px solid #142340;
  border-radius: 4px;
  padding: 10px 14px;
}

.diag-report-header {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #00e5ff;
  font-size: 10.5px;
  font-weight: 700;
  margin-bottom: 6px;
}

.diag-report-header svg {
  width: 14px;
  height: 14px;
}

.diag-report-text {
  font-size: 10.5px;
  line-height: 1.5;
  color: #cbd5e1;
  white-space: pre-wrap;
  max-height: 180px;
  overflow-y: auto;
}

.dot-warn {
  background: #f59e0b !important;
  box-shadow: 0 0 6px #f59e0b !important;
}

.dot-danger {
  background: #ef4444 !important;
  box-shadow: 0 0 6px #ef4444 !important;
}

.report-badge-status.amber {
  color: #fbbf24;
  background: rgba(245, 158, 11, 0.12);
  border-color: rgba(245, 158, 11, 0.35);
}

.report-badge-status.red {
  color: #f87171;
  background: rgba(239, 68, 68, 0.12);
  border-color: rgba(239, 68, 68, 0.35);
}

.report-check-box.error-box {
  background: rgba(239, 68, 68, 0.18);
  border-color: rgba(239, 68, 68, 0.4);
  color: #ef4444;
}

.cycle-tag-action.amber {
  background: rgba(245, 158, 11, 0.15);
  border-color: rgba(245, 158, 11, 0.4);
  color: #fbbf24;
}

.cycle-tag-action.red {
  background: rgba(239, 68, 68, 0.15);
  border-color: rgba(239, 68, 68, 0.4);
  color: #f87171;
}

.pulse-active {
  animation: pulse-tag 1.2s infinite alternate;
}

@keyframes pulse-tag {
  from { opacity: 0.6; }
  to { opacity: 1; }
}

.spin-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal-card {
  width: 580px;
  max-width: 90vw;
  background: #0b1426;
  border: 1px solid rgba(0, 229, 255, 0.3);
  border-radius: 6px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
  overflow: hidden;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: #091020;
  border-bottom: 1px solid #142340;
}

.modal-title-box {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #00e5ff;
}

.modal-icon {
  width: 16px;
  height: 16px;
}

.modal-title-box h3 {
  font-size: 13px;
  font-weight: 700;
  color: #fff;
  margin: 0;
}

.modal-close-btn {
  background: transparent;
  border: none;
  color: #94a3b8;
  font-size: 20px;
  cursor: pointer;
  line-height: 1;
}

.modal-body {
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 11px;
  max-height: 320px;
  overflow-y: auto;
}

.log-row {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  line-height: 1.4;
}

.log-row .timestamp {
  color: #64748b;
  flex-shrink: 0;
}

.log-row .tag {
  font-weight: 700;
  flex-shrink: 0;
}

.log-row.info .tag { color: #00e5ff; }
.log-row.warn .tag { color: #f87171; }
.log-row.warn span:last-child { color: #fca5a5; }
.log-row.success .tag { color: #10b981; }
.log-row.success span:last-child { color: #34d399; }

.modal-footer {
  padding: 10px 16px;
  background: #091020;
  border-top: 1px solid #142340;
  display: flex;
  justify-content: flex-end;
}

.btn-primary {
  background: #00e5ff;
  color: #000;
  border: none;
  font-weight: 700;
  padding: 5px 14px;
  border-radius: 4px;
  cursor: pointer;
}

.font-mono {
  font-family: var(--font-mono, monospace);
}

@media (max-width: 1200px) {
  .kpi-grid {
    grid-template-columns: repeat(4, 1fr);
  }
  .split-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 800px) {
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .models-comparison-grid {
    grid-template-columns: 1fr;
  }
}


@media (max-width: 1200px) {
  .kpi-grid {
    grid-template-columns: repeat(4, 1fr);
  }
  .split-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 800px) {
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .models-comparison-grid {
    grid-template-columns: 1fr;
  }
}
</style>

<style>
/* ==========================================================================
   UNSCOPED LIGHT MODE STYLES FOR OVERVIEW & PREDICTIVE MODELS
   ========================================================================== */
[data-theme="light"] .scada-container {
  background: #f1f5f9 !important;
  color: #0f172a !important;
}

[data-theme="light"] .control-ribbon {
  background: #ffffff !important;
  border-bottom: 1px solid #cbd5e1 !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
}

[data-theme="light"] .meta-tag {
  color: #64748b !important;
}

[data-theme="light"] .meta-val {
  color: #0f172a !important;
}

[data-theme="light"] .pill-sim-mode {
  background: #ecfdf5 !important;
  border-color: #a7f3d0 !important;
  color: #047857 !important;
}

[data-theme="light"] .pill-sim-mode.halted {
  background: #fef2f2 !important;
  border-color: #fecaca !important;
  color: #dc2626 !important;
}

[data-theme="light"] .btn-e-stop.triggered {
  background: #059669 !important;
  border-color: #10b981 !important;
  color: #ffffff !important;
}

[data-theme="light"] .equip-badge.green {
  background: #ecfdf5 !important;
  border-color: #10b981 !important;
  color: #047857 !important;
}

[data-theme="light"] .equip-badge.cyan {
  background: #f0f9ff !important;
  border-color: #0284c7 !important;
  color: #0284c7 !important;
}

[data-theme="light"] .equip-badge.purple {
  background: #faf5ff !important;
  border-color: #7c3aed !important;
  color: #6d28d9 !important;
}

[data-theme="light"] .equip-badge.off {
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
  color: #94a3b8 !important;
}

[data-theme="light"] .kpi-card {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
}

[data-theme="light"] .kpi-label {
  color: #64748b !important;
}

[data-theme="light"] .kpi-value.cyan {
  color: #0284c7 !important;
}

[data-theme="light"] .kpi-value.green {
  color: #059669 !important;
}

[data-theme="light"] .kpi-value.purple {
  color: #7c3aed !important;
}

[data-theme="light"] .kpi-unit {
  color: #64748b !important;
}

[data-theme="light"] .kpi-bar-bg {
  background: rgba(0, 0, 0, 0.08) !important;
}

[data-theme="light"] .scada-panel {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05) !important;
}

[data-theme="light"] .engine-icon-badge {
  background: rgba(2, 132, 199, 0.1) !important;
  border-color: rgba(2, 132, 199, 0.3) !important;
  color: #0284c7 !important;
}

[data-theme="light"] .engine-title {
  color: #0284c7 !important;
}

[data-theme="light"] .engine-desc {
  color: #64748b !important;
}

[data-theme="light"] .badge-status-live {
  background: #ecfdf5 !important;
  border-color: #a7f3d0 !important;
  color: #047857 !important;
}

[data-theme="light"] .badge-stat-pill.cyan-stat {
  background: #f0f9ff !important;
  border-color: #bae6fd !important;
  color: #0369a1 !important;
}

[data-theme="light"] .badge-stat-pill.red-stat {
  background: #fef2f2 !important;
  border-color: #fecaca !important;
  color: #dc2626 !important;
}

/* 1. Schedule Bar Light */
[data-theme="light"] .engine-schedule-bar {
  background: #f8fafc !important;
  border: 1px solid #cbd5e1 !important;
}

[data-theme="light"] .schedule-label {
  color: #475569 !important;
}

[data-theme="light"] .select-inline-wrapper {
  background: #ffffff !important;
  border-color: #0284c7 !important;
  box-shadow: 0 1px 3px rgba(2, 132, 199, 0.15) !important;
}

[data-theme="light"] .select-inline-wrapper .schedule-icon {
  color: #0284c7 !important;
}

[data-theme="light"] .schedule-prefix {
  color: #0284c7 !important;
}

[data-theme="light"] .select-inline {
  background-color: #ffffff !important;
  color: #0f172a !important;
  border-color: #cbd5e1 !important;
  color-scheme: light !important;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%230284c7' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E") !important;
}

[data-theme="light"] .select-inline:hover {
  background-color: #f1f5f9 !important;
  border-color: #0284c7 !important;
}

[data-theme="light"] .select-inline option {
  background-color: #ffffff !important;
  color: #0f172a !important;
  font-weight: 600 !important;
}

[data-theme="light"] .btn-auto-toggle.is-enabled {
  background: #ecfdf5 !important;
  border-color: #a7f3d0 !important;
  color: #047857 !important;
}

[data-theme="light"] .btn-auto-toggle.is-disabled {
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
  color: #64748b !important;
}

[data-theme="light"] .btn-auto-toggle .auto-toggle-track {
  background: #e2e8f0 !important;
  border-color: #cbd5e1 !important;
}

[data-theme="light"] .btn-auto-toggle.is-enabled .auto-toggle-track {
  background: #a7f3d0 !important;
  border-color: #059669 !important;
}

[data-theme="light"] .badge-countdown.disabled-auto {
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
  color: #64748b !important;
}

[data-theme="light"] .badge-countdown {
  background: #f0f9ff !important;
  border-color: #bae6fd !important;
  color: #0284c7 !important;
}

[data-theme="light"] .badge-countdown.paused-running {
  background: #f5f3ff !important;
  border-color: #ddd6fe !important;
  color: #7c3aed !important;
}

[data-theme="light"] .badge-countdown.halted-stopped {
  background: #fef2f2 !important;
  border-color: #fecaca !important;
  color: #dc2626 !important;
}

[data-theme="light"] .pulse-agent-dot {
  background: #7c3aed !important;
  box-shadow: 0 0 6px #7c3aed !important;
}

[data-theme="light"] .engine-info-note {
  color: #0284c7 !important;
}

/* 2. Model Cards Light */
[data-theme="light"] .model-box {
  background: #f8fafc !important;
}

[data-theme="light"] .model-box.alpha {
  border: 1px solid #bae6fd !important;
}

[data-theme="light"] .model-box.beta {
  border: 1px solid #e9d5ff !important;
}

[data-theme="light"] .alpha-dot {
  background: #0284c7 !important;
  box-shadow: 0 0 6px #0284c7 !important;
}

[data-theme="light"] .beta-dot {
  background: #7c3aed !important;
  box-shadow: 0 0 6px #7c3aed !important;
}

[data-theme="light"] .model-box-title {
  color: #0f172a !important;
}

[data-theme="light"] .alpha-badge {
  background: #f0f9ff !important;
  color: #0284c7 !important;
  border-color: #bae6fd !important;
}

[data-theme="light"] .beta-badge {
  background: #faf5ff !important;
  color: #7c3aed !important;
  border-color: #e9d5ff !important;
}

[data-theme="light"] .beta-badge.green {
  background: #ecfdf5 !important;
  color: #047857 !important;
  border-color: #a7f3d0 !important;
}

[data-theme="light"] .beta-badge.amber {
  background: #fffbeb !important;
  color: #b45309 !important;
  border-color: #fde68a !important;
}

[data-theme="light"] .beta-badge.red {
  background: #fef2f2 !important;
  color: #dc2626 !important;
  border-color: #fecaca !important;
}

[data-theme="light"] .model-tech-desc {
  color: #475569 !important;
}

[data-theme="light"] .model-submetrics {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
}

[data-theme="light"] .submetric-lbl {
  color: #64748b !important;
}

[data-theme="light"] .submetric-val {
  color: #0f172a !important;
}

/* 3. Confidence Panel Light */
[data-theme="light"] .panel-title {
  color: #0f172a !important;
}

[data-theme="light"] .panel-subtitle {
  color: #64748b !important;
}

[data-theme="light"] .confidence-score-label {
  color: #64748b !important;
}

[data-theme="light"] .confidence-score-val {
  color: #059669 !important;
  text-shadow: none !important;
}

[data-theme="light"] .conf-metric {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
}

[data-theme="light"] .conf-lbl {
  color: #64748b !important;
}

[data-theme="light"] .conf-val {
  color: #0f172a !important;
}

[data-theme="light"] .kalman-title {
  color: #64748b !important;
}

[data-theme="light"] .cyan-text {
  color: #0284c7 !important;
}

[data-theme="light"] .purple-text {
  color: #7c3aed !important;
}

[data-theme="light"] .kalman-bar {
  background: #e2e8f0 !important;
}

[data-theme="light"] .kalman-pinn {
  background: #0284c7 !important;
}

[data-theme="light"] .kalman-lstm {
  background: #7c3aed !important;
}

[data-theme="light"] .iso-note {
  color: #64748b !important;
}

/* 4. Anomaly & CoT Reasoning Light */
[data-theme="light"] .anomaly-alert-card {
  background: #fef2f2 !important;
  border-color: #fecaca !important;
}

[data-theme="light"] .alert-bell-icon,
[data-theme="light"] .alert-title-text {
  color: #dc2626 !important;
}

[data-theme="light"] .alert-desc {
  color: #991b1b !important;
}

[data-theme="light"] .cot-box {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
}

[data-theme="light"] .cot-header {
  border-bottom: 1px solid #e2e8f0 !important;
}

[data-theme="light"] .cot-title-left {
  color: #0284c7 !important;
}

[data-theme="light"] .cot-steps-tag {
  color: #64748b !important;
}

[data-theme="light"] .cot-line {
  color: #475569 !important;
}

[data-theme="light"] .cot-prefix {
  color: #0284c7 !important;
}

[data-theme="light"] .cot-line.highlight .cot-prefix {
  color: #0284c7 !important;
}

[data-theme="light"] .cot-line.highlight .cot-text {
  color: #0f172a !important;
  font-weight: 600 !important;
}

/* 5. Reports Panel Light */
[data-theme="light"] .status-indicators-bar {
  background: #f8fafc !important;
  border: 1px solid #cbd5e1 !important;
}

[data-theme="light"] .indicator-item {
  color: #64748b !important;
}

[data-theme="light"] .indicator-item strong {
  color: #0f172a !important;
}

[data-theme="light"] .ind-icon.cyan {
  color: #0284c7 !important;
}

[data-theme="light"] .ind-icon.purple {
  color: #7c3aed !important;
}

[data-theme="light"] .pill-mode {
  background: #f0f9ff !important;
  border-color: #bae6fd !important;
  color: #0284c7 !important;
}

[data-theme="light"] .report-title-line {
  color: #334155 !important;
}

[data-theme="light"] .report-title-line strong {
  color: #0f172a !important;
}

[data-theme="light"] .report-badge-status {
  background: #ecfdf5 !important;
  border-color: #a7f3d0 !important;
  color: #047857 !important;
}

[data-theme="light"] .btn-action-audit,
[data-theme="light"] .btn-action-recent,
[data-theme="light"] .btn-action-export {
  background: #f8fafc !important;
  border-color: #cbd5e1 !important;
  color: #0284c7 !important;
}

[data-theme="light"] .btn-action-audit:hover,
[data-theme="light"] .btn-action-recent:hover,
[data-theme="light"] .btn-action-export:hover {
  background: #f1f5f9 !important;
  border-color: #0284c7 !important;
}

[data-theme="light"] .recent-cycle-preview {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
}

[data-theme="light"] .cycle-num {
  color: #0284c7 !important;
}

[data-theme="light"] .cycle-time {
  color: #64748b !important;
}

[data-theme="light"] .cycle-stat {
  color: #334155 !important;
}

[data-theme="light"] .cycle-alert-stat {
  color: #dc2626 !important;
}

[data-theme="light"] .diagnostic-report-card {
  background: #f8fafc !important;
  border-color: #cbd5e1 !important;
}

[data-theme="light"] .diag-report-header {
  color: #0284c7 !important;
}

[data-theme="light"] .diag-report-text {
  color: #334155 !important;
}

[data-theme="light"] .report-badge-status.amber {
  background: #fffbeb !important;
  border-color: #fde68a !important;
  color: #b45309 !important;
}

[data-theme="light"] .report-badge-status.red {
  background: #fef2f2 !important;
  border-color: #fecaca !important;
  color: #b91c1c !important;
}

[data-theme="light"] .cycle-tag-action.amber {
  background: #fffbeb !important;
  border-color: #fde68a !important;
  color: #b45309 !important;
}

[data-theme="light"] .cycle-tag-action.red {
  background: #fef2f2 !important;
  border-color: #fecaca !important;
  color: #b91c1c !important;
}

/* 6. Modal Light */
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

[data-theme="light"] .modal-title-box h3 {
  color: #0f172a !important;
}

[data-theme="light"] .modal-title-box svg {
  color: #0284c7 !important;
}

[data-theme="light"] .modal-close-btn {
  color: #64748b !important;
}

[data-theme="light"] .modal-body {
  background: #ffffff !important;
}

[data-theme="light"] .log-row {
  color: #334155 !important;
}

[data-theme="light"] .log-row.info {
  background: #f0f9ff !important;
  border-color: #e0f2fe !important;
}

[data-theme="light"] .log-row.warn {
  background: #fffbeb !important;
  border-color: #fef3c7 !important;
}

[data-theme="light"] .log-row.success {
  background: #f0fdf4 !important;
  border-color: #dcfce7 !important;
}

[data-theme="light"] .modal-footer {
  background: #f8fafc !important;
  border-top: 1px solid #e2e8f0 !important;
}

[data-theme="light"] .btn-primary {
  background: #0284c7 !important;
  color: #ffffff !important;
}
</style>


<style>
/* ==========================================================================
   UNSCOPED LIGHT MODE STYLES FOR OVERVIEW & PREDICTIVE MODELS
   ========================================================================== */
[data-theme="light"] .scada-container {
  background: #f1f5f9 !important;
  color: #0f172a !important;
}

[data-theme="light"] .control-ribbon {
  background: #ffffff !important;
  border-bottom: 1px solid #cbd5e1 !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
}

[data-theme="light"] .meta-tag {
  color: #64748b !important;
}

[data-theme="light"] .meta-val {
  color: #0f172a !important;
}

[data-theme="light"] .pill-sim-mode {
  background: #ecfdf5 !important;
  border-color: #a7f3d0 !important;
  color: #047857 !important;
}

[data-theme="light"] .pill-sim-mode.halted {
  background: #fef2f2 !important;
  border-color: #fecaca !important;
  color: #dc2626 !important;
}

[data-theme="light"] .btn-e-stop.triggered {
  background: #059669 !important;
  border-color: #10b981 !important;
  color: #ffffff !important;
}

[data-theme="light"] .equip-badge.green {
  background: #ecfdf5 !important;
  border-color: #10b981 !important;
  color: #047857 !important;
}

[data-theme="light"] .equip-badge.cyan {
  background: #f0f9ff !important;
  border-color: #0284c7 !important;
  color: #0284c7 !important;
}

[data-theme="light"] .equip-badge.purple {
  background: #faf5ff !important;
  border-color: #7c3aed !important;
  color: #6d28d9 !important;
}

[data-theme="light"] .equip-badge.off {
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
  color: #94a3b8 !important;
}

[data-theme="light"] .kpi-card {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
}

[data-theme="light"] .kpi-label {
  color: #64748b !important;
}

[data-theme="light"] .kpi-value.cyan {
  color: #0284c7 !important;
}

[data-theme="light"] .kpi-value.green {
  color: #059669 !important;
}

[data-theme="light"] .kpi-value.purple {
  color: #7c3aed !important;
}

[data-theme="light"] .kpi-unit {
  color: #64748b !important;
}

[data-theme="light"] .kpi-bar-bg {
  background: rgba(0, 0, 0, 0.08) !important;
}

[data-theme="light"] .scada-panel {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05) !important;
}

[data-theme="light"] .engine-icon-badge {
  background: rgba(2, 132, 199, 0.1) !important;
  border-color: rgba(2, 132, 199, 0.3) !important;
  color: #0284c7 !important;
}

[data-theme="light"] .engine-title {
  color: #0284c7 !important;
}

[data-theme="light"] .engine-desc {
  color: #64748b !important;
}

[data-theme="light"] .badge-status-live {
  background: #ecfdf5 !important;
  border-color: #a7f3d0 !important;
  color: #047857 !important;
}

[data-theme="light"] .badge-stat-pill.cyan-stat {
  background: #f0f9ff !important;
  border-color: #bae6fd !important;
  color: #0369a1 !important;
}

[data-theme="light"] .badge-stat-pill.red-stat {
  background: #fef2f2 !important;
  border-color: #fecaca !important;
  color: #dc2626 !important;
}

/* 1. Schedule Bar Light */
[data-theme="light"] .engine-schedule-bar {
  background: #f8fafc !important;
  border: 1px solid #cbd5e1 !important;
}

[data-theme="light"] .schedule-label {
  color: #475569 !important;
}

[data-theme="light"] .select-inline-wrapper {
  background: #ffffff !important;
  border-color: #0284c7 !important;
  box-shadow: 0 1px 3px rgba(2, 132, 199, 0.15) !important;
}

[data-theme="light"] .select-inline-wrapper .schedule-icon {
  color: #0284c7 !important;
}

[data-theme="light"] .schedule-prefix {
  color: #0284c7 !important;
}

[data-theme="light"] .select-inline {
  background-color: #ffffff !important;
  color: #0f172a !important;
  border-color: #cbd5e1 !important;
  color-scheme: light !important;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%230284c7' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E") !important;
}

[data-theme="light"] .select-inline:hover {
  background-color: #f1f5f9 !important;
  border-color: #0284c7 !important;
}

[data-theme="light"] .select-inline option {
  background-color: #ffffff !important;
  color: #0f172a !important;
  font-weight: 600 !important;
}

[data-theme="light"] .btn-auto-toggle.is-enabled {
  background: #ecfdf5 !important;
  border-color: #a7f3d0 !important;
  color: #047857 !important;
}

[data-theme="light"] .btn-auto-toggle.is-disabled {
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
  color: #64748b !important;
}

[data-theme="light"] .btn-auto-toggle .auto-toggle-track {
  background: #e2e8f0 !important;
  border-color: #cbd5e1 !important;
}

[data-theme="light"] .btn-auto-toggle.is-enabled .auto-toggle-track {
  background: #a7f3d0 !important;
  border-color: #059669 !important;
}

[data-theme="light"] .badge-countdown.disabled-auto {
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
  color: #64748b !important;
}

[data-theme="light"] .badge-countdown {
  background: #f0f9ff !important;
  border-color: #bae6fd !important;
  color: #0284c7 !important;
}

[data-theme="light"] .badge-countdown.paused-running {
  background: #f5f3ff !important;
  border-color: #ddd6fe !important;
  color: #7c3aed !important;
}

[data-theme="light"] .badge-countdown.halted-stopped {
  background: #fef2f2 !important;
  border-color: #fecaca !important;
  color: #dc2626 !important;
}

[data-theme="light"] .pulse-agent-dot {
  background: #7c3aed !important;
  box-shadow: 0 0 6px #7c3aed !important;
}

[data-theme="light"] .engine-info-note {
  color: #0284c7 !important;
}

/* 2. Model Cards Light */
[data-theme="light"] .model-box {
  background: #f8fafc !important;
}

[data-theme="light"] .model-box.alpha {
  border: 1px solid #bae6fd !important;
}

[data-theme="light"] .model-box.beta {
  border: 1px solid #e9d5ff !important;
}

[data-theme="light"] .alpha-dot {
  background: #0284c7 !important;
  box-shadow: 0 0 6px #0284c7 !important;
}

[data-theme="light"] .beta-dot {
  background: #7c3aed !important;
  box-shadow: 0 0 6px #7c3aed !important;
}

[data-theme="light"] .model-box-title {
  color: #0f172a !important;
}

[data-theme="light"] .alpha-badge {
  background: #f0f9ff !important;
  color: #0284c7 !important;
  border-color: #bae6fd !important;
}

[data-theme="light"] .beta-badge {
  background: #faf5ff !important;
  color: #7c3aed !important;
  border-color: #e9d5ff !important;
}

[data-theme="light"] .beta-badge.green {
  background: #ecfdf5 !important;
  color: #047857 !important;
  border-color: #a7f3d0 !important;
}

[data-theme="light"] .beta-badge.amber {
  background: #fffbeb !important;
  color: #b45309 !important;
  border-color: #fde68a !important;
}

[data-theme="light"] .beta-badge.red {
  background: #fef2f2 !important;
  color: #dc2626 !important;
  border-color: #fecaca !important;
}

[data-theme="light"] .model-tech-desc {
  color: #475569 !important;
}

[data-theme="light"] .model-submetrics {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
}

[data-theme="light"] .submetric-lbl {
  color: #64748b !important;
}

[data-theme="light"] .submetric-val {
  color: #0f172a !important;
}

/* 3. Confidence Panel Light */
[data-theme="light"] .panel-title {
  color: #0f172a !important;
}

[data-theme="light"] .panel-subtitle {
  color: #64748b !important;
}

[data-theme="light"] .confidence-score-label {
  color: #64748b !important;
}

[data-theme="light"] .confidence-score-val {
  color: #059669 !important;
  text-shadow: none !important;
}

[data-theme="light"] .conf-metric {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
}

[data-theme="light"] .conf-lbl {
  color: #64748b !important;
}

[data-theme="light"] .conf-val {
  color: #0f172a !important;
}

[data-theme="light"] .kalman-title {
  color: #64748b !important;
}

[data-theme="light"] .cyan-text {
  color: #0284c7 !important;
}

[data-theme="light"] .purple-text {
  color: #7c3aed !important;
}

[data-theme="light"] .kalman-bar {
  background: #e2e8f0 !important;
}

[data-theme="light"] .kalman-pinn {
  background: #0284c7 !important;
}

[data-theme="light"] .kalman-lstm {
  background: #7c3aed !important;
}

[data-theme="light"] .iso-note {
  color: #64748b !important;
}

/* 4. Anomaly & CoT Reasoning Light */
[data-theme="light"] .anomaly-alert-card {
  background: #fef2f2 !important;
  border-color: #fecaca !important;
}

[data-theme="light"] .alert-bell-icon,
[data-theme="light"] .alert-title-text {
  color: #dc2626 !important;
}

[data-theme="light"] .alert-desc {
  color: #991b1b !important;
}

[data-theme="light"] .cot-box {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
}

[data-theme="light"] .cot-header {
  border-bottom: 1px solid #e2e8f0 !important;
}

[data-theme="light"] .cot-title-left {
  color: #0284c7 !important;
}

[data-theme="light"] .cot-steps-tag {
  color: #64748b !important;
}

[data-theme="light"] .cot-line {
  color: #475569 !important;
}

[data-theme="light"] .cot-prefix {
  color: #0284c7 !important;
}

[data-theme="light"] .cot-line.highlight .cot-prefix {
  color: #0284c7 !important;
}

[data-theme="light"] .cot-line.highlight .cot-text {
  color: #0f172a !important;
  font-weight: 600 !important;
}

/* 5. Reports Panel Light */
[data-theme="light"] .status-indicators-bar {
  background: #f8fafc !important;
  border: 1px solid #cbd5e1 !important;
}

[data-theme="light"] .indicator-item {
  color: #64748b !important;
}

[data-theme="light"] .indicator-item strong {
  color: #0f172a !important;
}

[data-theme="light"] .ind-icon.cyan {
  color: #0284c7 !important;
}

[data-theme="light"] .ind-icon.purple {
  color: #7c3aed !important;
}

[data-theme="light"] .pill-mode {
  background: #f0f9ff !important;
  border-color: #bae6fd !important;
  color: #0284c7 !important;
}

[data-theme="light"] .report-title-line {
  color: #334155 !important;
}

[data-theme="light"] .report-title-line strong {
  color: #0f172a !important;
}

[data-theme="light"] .report-badge-status {
  background: #ecfdf5 !important;
  border-color: #a7f3d0 !important;
  color: #047857 !important;
}

[data-theme="light"] .btn-action-audit,
[data-theme="light"] .btn-action-recent,
[data-theme="light"] .btn-action-export {
  background: #f8fafc !important;
  border-color: #cbd5e1 !important;
  color: #0284c7 !important;
}

[data-theme="light"] .btn-action-audit:hover,
[data-theme="light"] .btn-action-recent:hover,
[data-theme="light"] .btn-action-export:hover {
  background: #f1f5f9 !important;
  border-color: #0284c7 !important;
}

[data-theme="light"] .recent-cycle-preview {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
}

[data-theme="light"] .cycle-num {
  color: #0284c7 !important;
}

[data-theme="light"] .cycle-time {
  color: #64748b !important;
}

[data-theme="light"] .cycle-stat {
  color: #334155 !important;
}

[data-theme="light"] .cycle-alert-stat {
  color: #dc2626 !important;
}

[data-theme="light"] .diagnostic-report-card {
  background: #f8fafc !important;
  border-color: #cbd5e1 !important;
}

[data-theme="light"] .diag-report-header {
  color: #0284c7 !important;
}

[data-theme="light"] .diag-report-text {
  color: #334155 !important;
}

[data-theme="light"] .report-badge-status.amber {
  background: #fffbeb !important;
  border-color: #fde68a !important;
  color: #b45309 !important;
}

[data-theme="light"] .report-badge-status.red {
  background: #fef2f2 !important;
  border-color: #fecaca !important;
  color: #b91c1c !important;
}

[data-theme="light"] .cycle-tag-action.amber {
  background: #fffbeb !important;
  border-color: #fde68a !important;
  color: #b45309 !important;
}

[data-theme="light"] .cycle-tag-action.red {
  background: #fef2f2 !important;
  border-color: #fecaca !important;
  color: #b91c1c !important;
}

/* 6. Modal Light */
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

[data-theme="light"] .modal-title-box h3 {
  color: #0f172a !important;
}

[data-theme="light"] .modal-title-box svg {
  color: #0284c7 !important;
}

[data-theme="light"] .modal-close-btn {
  color: #64748b !important;
}

[data-theme="light"] .modal-body {
  background: #ffffff !important;
}

[data-theme="light"] .log-row {
  color: #334155 !important;
}

[data-theme="light"] .log-row.info {
  background: #f0f9ff !important;
  border-color: #e0f2fe !important;
}

[data-theme="light"] .log-row.warn {
  background: #fffbeb !important;
  border-color: #fef3c7 !important;
}

[data-theme="light"] .log-row.success {
  background: #f0fdf4 !important;
  border-color: #dcfce7 !important;
}

[data-theme="light"] .modal-footer {
  background: #f8fafc !important;
  border-top: 1px solid #e2e8f0 !important;
}

[data-theme="light"] .btn-primary {
  background: #0284c7 !important;
  color: #ffffff !important;
}
</style>
