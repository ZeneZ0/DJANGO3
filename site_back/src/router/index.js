// site_back/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue')
  },
  {
    path: '/reactive',
    name: 'reactive',
    component: () => import('../views/ReactiveView.vue')
  },
  {
    path: '/arrays',
    name: 'arrays',
    component: () => import('../views/ArraysView.vue')
  },
  {
    path: '/data',
    name: 'data',
    component: () => import('../views/BackendDataView.vue')
  },
  
  {
    path: '/component-types',
    name: 'component-types',
    component: () => import('../views/ComponentTypesView.vue')
  },
  {
    path: '/manufacturers',
    name: 'manufacturers',
    component: () => import('../views/ManufacturersView.vue')
  },
  {
    path: '/components',
    name: 'components',
    component: () => import('../views/ComponentsView.vue')
  },
  {
    path: '/configs', 
    name: 'configs',
    component: () => import('../views/PCConfigurationsView.vue')
  },
  {
    path: '/requests',
    name: 'requests',
    component: () => import('../views/BuildRequestsView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router