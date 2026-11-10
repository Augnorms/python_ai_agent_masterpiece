import { createRouter, createWebHistory } from 'vue-router'
import AgentOrchestratorView from '../views/AgentOrchestratorView.vue'
import KnowledgeRagView from '../views/KnowledgeRagView.vue'
import SettingsView from '../views/SettingsView.vue'
import OverviewPredictiveView from '../views/OverviewPredictiveView.vue'
import ModbusTelemetryView from '../views/ModbusTelemetryView.vue'
import LoginView from '../views/LoginView.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { title: 'SCADA Operator Gateway Login' }
  },
  {
    path: '/overview',
    name: 'overview',
    component: OverviewPredictiveView,
    meta: { title: 'Overview & Predictive Models' }
  },
  {
    path: '/modbus',
    name: 'modbus',
    component: ModbusTelemetryView,
    meta: { title: 'Modbus TCP Telemetry (PLC)' }
  },
  {
    path: '/orchestrator',
    name: 'orchestrator',
    component: AgentOrchestratorView,
    meta: { title: 'Agent Orchestrator & Cockpit' }
  },
  {
    path: '/knowledge',
    name: 'knowledge',
    component: KnowledgeRagView,
    meta: { title: 'Knowledge & RAG Hub' }
  },
  {
    path: '/settings',
    name: 'settings',
    component: SettingsView,
    meta: { title: 'System & Swarm Settings' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('scada_access_token')
  if (to.path === '/login') {
    if (token) {
      return next('/overview')
    }
    return next()
  }

  if (!token) {
    return next('/login')
  }

  next()
})

export default router
