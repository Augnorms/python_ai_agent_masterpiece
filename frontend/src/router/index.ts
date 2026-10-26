import { createRouter, createWebHistory } from 'vue-router'
import AgentOrchestratorView from '../views/AgentOrchestratorView.vue'
import KnowledgeRagView from '../views/KnowledgeRagView.vue'

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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
