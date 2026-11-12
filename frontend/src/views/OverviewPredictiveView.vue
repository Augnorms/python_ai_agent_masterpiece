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

        <!-- Agent Execution Pipeline & Chain-of-Thought Flow -->
        <section class="scada-panel pipeline-panel">
          <div class="panel-header pipeline-header">
            <div class="pipeline-header-left">
              <div class="pipeline-icon-box">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="2" y="5" width="5" height="5" rx="1" />
                  <rect x="17" y="2" width="5" height="5" rx="1" />
                  <rect x="17" y="16" width="5" height="5" rx="1" />
                  <path d="M7 7.5h5a2 2 0 0 1 2 2v5a2 2 0 0 0 2 2h1" />
                  <path d="M12 7.5v-3a2 2 0 0 1 2-2h3" />
                </svg>
              </div>
              <div>
                <h3 class="pipeline-title font-mono">AGENT EXECUTION PIPELINE & CHAIN-OF-THOUGHT FLOW</h3>
              </div>
            </div>

            <div class="pipeline-header-right">
              <!-- Stop / Terminate Button -->
              <button
                v-if="isAgentRunning"
                type="button"
                class="btn-cot-terminate font-mono"
                @click="terminateAgentRun"
                title="Terminate running agent cycle"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <rect x="6" y="6" width="12" height="12" rx="1.5" />
                </svg>
                <span>STOP</span>
              </button>

              <!-- Step Ratio & Status Badge -->
              <div class="pipeline-step-box font-mono" :class="{ 'is-running': isAgentRunning }">
                <span class="step-ratio-text">{{ isAgentRunning ? pipelineStepRatio : 'IDLE' }}</span>
                <span class="step-status-row">
                  <span class="step-dot" :class="isAgentRunning ? 'pulse-cyan' : (eStopActive ? 'dot-red' : 'dot-idle')"></span>
                  <span class="step-status-label">{{ isAgentRunning ? 'RUNNING' : (eStopActive ? 'HALTED' : 'STANDBY') }}</span>
                </span>
              </div>

              <!-- Active Pointer Box -->
              <div class="pipeline-pointer-box font-mono">
                <span class="pointer-label">ACTIVE POINTER:</span>
                <span class="pointer-value">{{ activePointerName }}</span>
              </div>
            </div>
          </div>

          <!-- 1. When Agent is actively running and steps have arrived: display dynamic step cards -->
          <div v-if="isAgentRunning && pipelineCards.length > 0" class="pipeline-cards-container">
            <div class="pipeline-cards-grid">
              <div
                v-for="(card, idx) in pipelineCards"
                :key="card.id || idx"
                class="pipeline-card-wrapper"
              >
                <div
                  class="pipeline-step-card"
                  :class="{
                    'is-running': card.status === 'running',
                    'is-completed': card.status === 'completed',
                    'is-error': card.status === 'error'
                  }"
                >
                  <div class="step-card-header">
                    <span class="step-card-tag font-mono">{{ card.tag }}</span>
                    <div class="step-card-status-indicator">
                      <!-- Running Spinner -->
                      <span v-if="card.status === 'running'" class="step-card-spinner"></span>
                      <!-- Error / Terminated Icon -->
                      <svg v-else-if="card.status === 'error'" class="step-icon-error" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <circle cx="12" cy="12" r="10" />
                        <line x1="12" y1="8" x2="12" y2="12" />
                        <line x1="12" y1="16" x2="12.01" y2="16" />
                      </svg>
                      <!-- Completed Checkmark Icon -->
                      <svg v-else class="step-icon-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <circle cx="12" cy="12" r="10" />
                        <polyline points="8 12 11 15 16 9" />
                      </svg>
                    </div>
                  </div>

                  <div class="step-card-body font-mono" :title="card.fullBody || card.body">
                    {{ card.body }}
                  </div>

                  <div
                    class="step-card-footer font-mono"
                    :class="{ 'footer-running': card.status === 'running', 'footer-error': card.status === 'error' }"
                  >
                    {{ card.footer }}
                  </div>
                </div>

                <!-- Connector Arrow (hidden on 6th card of each row & last card) -->
                <span class="card-connector-arrow">→</span>
              </div>
            </div>
          </div>

          <!-- 2. When Agent has just started running but first step hasn't arrived yet -->
          <div v-else-if="isAgentRunning && pipelineCards.length === 0" class="pipeline-idle-box font-mono">
            <div class="pipeline-idle-content">
              <span class="step-card-spinner"></span>
              <span class="pipeline-idle-text">Initializing autonomous diagnostic cycle... Ingesting telemetry & SOP compliance rules...</span>
            </div>
          </div>

          <!-- 3. When Nothing is Running: Display idle state message -->
          <div v-else class="pipeline-idle-box font-mono">
            <div class="pipeline-idle-content">
              <span class="pipeline-idle-prefix">›</span>
              <span class="pipeline-idle-text">Autonomous Diagnostic Agent is <strong>IDLE</strong>. Engine ready. Waiting for interval trigger or manual run.</span>
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
            <button
              v-if="!isAgentRunning"
              type="button"
              class="btn-action-audit"
              @click="triggerAutoRun(true)"
              title="Run autonomous supervisor immediately"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="23 4 23 10 17 10" />
                <polyline points="1 20 1 14 7 14" />
                <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
              </svg>
              <span>Run Cycle Now</span>
            </button>

            <button
              v-else
              type="button"
              class="btn-action-terminate"
              @click="terminateAgentRun"
              title="Terminate running agent cycle"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <rect x="6" y="6" width="12" height="12" rx="1.5" />
              </svg>
              <span>Terminate Agent</span>
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
const API_BASE = 'http://127.0.0.1:8000'

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

const cotStreamRef = ref(null)

const scrollCotToBottom = async () => {
  await nextTick()
  if (cotStreamRef.value) {
    cotStreamRef.value.scrollTop = cotStreamRef.value.scrollHeight
  }
}

watch(reasoningSteps, () => {
  scrollCotToBottom()
}, { deep: true })

const cycleStatText = computed(() => {
  return `Flow: ${cycleFlow.value} m³/h | TDS: ${cycleTds.value} ppm (${cycleQuality.value})`
})

// ─── Pipeline Step Cards Parsing (Horizontal 6-per-row) ─────────────────
const parseStepToCard = (rawStep, index, totalSteps, isLastRunning) => {
  const step = String(rawStep).trim()
  let tag = `STEP ${index + 1}`
  let body = step
  let footer = 'DONE'
  let status = isLastRunning ? 'running' : 'completed'

  if (step.includes('[INGEST]')) {
    tag = 'INGEST'
    footer = isLastRunning ? 'INGESTING...' : 'VERIFIED'
    const flowMatch = step.match(/Flow=([0-9.]+)/i)
    const tdsMatch = step.match(/TDS=([0-9.]+)/i)
    if (flowMatch && tdsMatch) {
      body = `Flow ${flowMatch[1]} m³/h, TDS ${tdsMatch[1]} ppm`
    } else {
      body = step.replace(/\[INGEST\]\s*/i, '').trim()
    }
  } else if (step.includes('[SUPERVISOR]')) {
    tag = 'SUPERVISOR'
    footer = isLastRunning ? 'AUDITING...' : 'DONE'
    body = 'Start water quality & SOP compliance audit'
  } else if (step.includes('[Orchestrator Config]') || step.includes('Orchestrator Config')) {
    tag = 'CONFIG'
    footer = 'READY'
    const modelMatch = step.match(/Model:\s*([^|]+)/i)
    const tempMatch = step.match(/Temp:\s*([^|]+)/i)
    const stepsMatch = step.match(/MaxSteps:\s*([0-9]+)/i)
    const model = modelMatch ? modelMatch[1].trim().replace(/^openai\//, '') : 'gpt-oss-20b'
    const temp = tempMatch ? tempMatch[1].trim() : '0.2'
    const steps = stepsMatch ? stepsMatch[1].trim() : '10'
    body = `${model} | T:${temp} | Steps:${steps}`
  } else if (step.includes('ask_rag_agent') || step.includes('[RAG]')) {
    tag = `STEP ${index} RAG`
    footer = isLastRunning ? 'QUERYING...' : 'RESOLVED'
    body = 'ask_rag_agent'
  } else if (step.includes('ask_email_agent') || step.includes('[EMAIL]')) {
    tag = 'EMAIL AGENT'
    footer = isLastRunning ? 'DISPATCHING...' : 'RESOLVED'
    body = 'ask_email_agent'
  } else if (step.includes('[reflection]')) {
    tag = 'REFLECTION'
    footer = isLastRunning ? 'AUDITING...' : 'VERIFIED'
    body = 'Reviewing telemetry SOP compliance'
  } else if (step.includes('[ORCHESTRATOR]')) {
    tag = 'ORCHESTRATOR'
    footer = 'VERIFIED'
    body = 'Autonomous diagnostic cycle completed'
  } else if (step.includes('[TERMINATED]')) {
    tag = 'TERMINATED'
    footer = 'STOPPED'
    status = 'error'
    body = 'Agent cycle terminated by operator'
  } else if (step.startsWith('[') && step.includes(']')) {
    const endBracket = step.indexOf(']')
    tag = step.slice(1, endBracket).toUpperCase()
    body = step.slice(endBracket + 1).trim()
    footer = isLastRunning ? 'RUNNING' : 'DONE'
  }

  // Truncate long body text to keep card size compact (matching ~140 chars / 7-8 lines)
  const fullBody = body
  if (body.length > 140) {
    const truncated = body.slice(0, 140)
    const lastSpace = truncated.lastIndexOf(' ')
    body = (lastSpace > 100 ? truncated.slice(0, lastSpace) : truncated).trim() + '...'
  }

  return {
    id: index,
    tag,
    body,
    fullBody,
    footer,
    status
  }
}

const pipelineCards = computed(() => {
  if (!reasoningSteps.value || reasoningSteps.value.length === 0) {
    return []
  }
  const total = reasoningSteps.value.length
  return reasoningSteps.value.map((step, idx) => {
    const isLast = idx === total - 1
    return parseStepToCard(step, idx, total, isLast && isAgentRunning.value)
  })
})

const pipelineStepRatio = computed(() => {
  if (!isAgentRunning.value) return 'IDLE'
  const count = pipelineCards.value.length
  const total = Math.max(count, 8)
  return `STEP ${count} / ${total}`
})

const activePointerName = computed(() => {
  if (!isAgentRunning.value) {
    if (eStopActive.value) return 'HALTED'
    return 'IDLE'
  }
  const cards = pipelineCards.value
  if (!cards || cards.length === 0) return 'INITIALIZING'
  const activeCard = cards[cards.length - 1]
  const tag = (activeCard.tag || '').toUpperCase()
  if (tag.includes('RAG') || tag.includes('TOOL')) return 'TOOL EXEC'
  if (tag.includes('EMAIL')) return 'EMAIL DISPATCH'
  if (tag.includes('SUPERVISOR')) return 'SUPERVISOR AUDIT'
  if (tag.includes('CONFIG')) return 'CONFIG LOAD'
  if (tag.includes('INGEST')) return 'TELEMETRY INGEST'
  return tag || 'TOOL EXEC'
})

const fetchLastAgentRun = async () => {
  try {
    const token = localStorage.getItem('scada_access_token')
    const response = await fetch(`${API_BASE}/api/agent/auto-run?run_now=false`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
      }
    })
    if (!response.ok) return
    const json = await response.json()
    if (json && Array.isArray(json.reasoning_steps) && json.reasoning_steps.length > 0) {
      reasoningSteps.value = json.reasoning_steps
    }
    if (json && json.cycle_number) {
      cycleNumber.value = json.cycle_number
    }
  } catch (err) {
    // Keep defaults
  }
}

// Trigger Auto-Run from backend via SSE Streaming
let autoRunAbortController = null

const terminateAgentRun = async () => {
  if (autoRunAbortController) {
    try {
      autoRunAbortController.abort()
    } catch (e) {}
    autoRunAbortController = null
  }

  try {
    const token = localStorage.getItem('scada_access_token')
    await fetch(`${API_BASE}/api/agent/terminate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
      }
    })
  } catch (err) {
    console.warn('Backend terminate call:', err)
  }

  isAgentRunning.value = false
  reasoningSteps.value.push('[TERMINATED] Agent cycle terminated by operator.')
  scrollCotToBottom()

  const intervalSecs = (parseInt(selectedInterval.value) || 60) * 60
  countdownSeconds.value = intervalSecs
  if (isAutonomousAgentEnabled.value && !eStopActive.value && typeof localStorage !== 'undefined') {
    localStorage.setItem(TARGET_TIMESTAMP_KEY, String(Date.now() + countdownSeconds.value * 1000))
  }
  const mins = Math.floor(intervalSecs / 60)
  const secs = intervalSecs % 60
  countdownText.value = `${mins}m ${String(secs).padStart(2, '0')}s`
}

const triggerAutoRun = async (isManual = false) => {
  if (isAgentRunning.value || eStopActive.value) return
  if (!isManual && !isAutonomousAgentEnabled.value) return
  isAgentRunning.value = true
  reasoningSteps.value = []

  autoRunAbortController = new AbortController()

  try {
    const token = localStorage.getItem('scada_access_token')
    const response = await fetch(`${API_BASE}/api/agent/auto-run`, {
      method: 'POST',
      signal: autoRunAbortController.signal,
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
      }
    })
    
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
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
        if (!trimmed.startsWith('data: ')) continue

        const raw = trimmed.slice(6)
        let payload
        try {
          payload = JSON.parse(raw)
        } catch {
          continue
        }

        if (!payload || !payload.type) continue

        // 1. Initial snapshot event
        if (payload.type === 'init' && payload.data) {
          if (payload.data.flow !== undefined) cycleFlow.value = payload.data.flow
          if (payload.data.tds !== undefined) cycleTds.value = payload.data.tds
          if (payload.data.quality !== undefined) cycleQuality.value = payload.data.quality
          if (payload.data.cycle_number !== undefined) {
            cycleNumber.value = payload.data.cycle_number
            lastReportTime.value = `CYCLE #${payload.data.cycle_number} (${payload.data.timestamp || new Date().toLocaleTimeString()})`
          }
        }
        // 2. Live Chain-of-Thought reasoning steps
        else if (payload.type === 'step') {
          reasoningSteps.value.push(payload.data)
          scrollCotToBottom()
        }
        // 3. Final execution result
        else if (payload.type === 'result') {
          const json = payload.data
          cycleNumber.value = json.cycle_number || cycleNumber.value
          diagnosticReport.value = json.diagnostic_report || ''
          
          const nowStr = json.timestamp || new Date().toLocaleTimeString()
          cycleTimestamp.value = nowStr
          lastReportTime.value = `CYCLE #${cycleNumber.value} (${nowStr})`

          if (json.live_inputs) {
            if (json.live_inputs.flow !== undefined) cycleFlow.value = json.live_inputs.flow
            if (json.live_inputs.tds !== undefined) cycleTds.value = json.live_inputs.tds
            if (json.live_inputs.quality !== undefined) cycleQuality.value = json.live_inputs.quality
          }

          if (Array.isArray(json.reasoning_steps) && json.reasoning_steps.length > 0) {
            reasoningSteps.value = json.reasoning_steps
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
        }
        // 4. Plant/PLC error event
        else if (payload.type === 'error') {
          scadaLinkStatus.value = 'PLC DISCONNECTED'
          plantHealth.value = 'OFFLINE'
          plantHealthDotClass.value = 'dot-danger'
          lastReportBadge.value = 'PLC DISCONNECTED'
          lastReportBadgeClass.value = 'red'
          cycleAlerts.value = 1
          cycleActionTag.value = 'LINK RECONNECT'
          cycleTagClass.value = 'red'
          if (payload.data && payload.data.message) {
            diagnosticReport.value = `[STATUS] ${payload.data.message}`
          }
        }
        // 5. Terminated event
        else if (payload.type === 'terminated') {
          reasoningSteps.value.push('[TERMINATED] Execution terminated by operator.')
          scrollCotToBottom()
        }
      }
    }
  } catch (err) {
    if (err.name === 'AbortError') {
      console.log('SSE auto-run stream aborted by operator.')
    } else {
      console.error('SSE auto-run error:', err)
      scadaLinkStatus.value = 'NETWORK INTERRUPTION'
    }
  } finally {
    autoRunAbortController = null
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
    const token = localStorage.getItem('scada_access_token')
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
      }
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

<style scoped src="@/style_folder/OverviewPredictiveView.css"></style>
<style src="@/style_folder/OverviewPredictiveView.global.css"></style>
