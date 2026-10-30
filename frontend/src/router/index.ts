import { createRouter, createWebHistory } from 'vue-router'
import AgentOrchestratorView from '../views/AgentOrchestratorView.vue'
import KnowledgeRagView from '../views/KnowledgeRagView.vue'
import SettingsView from '../views/SettingsView.vue'

const routes = [
  {
    path: '/',
    redirect: '/orchestrator'
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

export default router
