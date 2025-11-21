
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
  path: '/backend-data',
  name: 'backend-data',
  component: () => import('../views/BackendDataView.vue')
  },
  {
  path: '/manage-data',
  name: 'manage-data',
  component: () => import('../views/ManageDataView.vue')
  },
  {
  path: '/manage/component-types',
  name: 'component-types',
  component: () => import('../views/ComponentTypesView.vue')
  },
  {
  path: '/manage/manufacturers', 
  name: 'manufacturers',
  component: () => import('../views/ManufacturersView.vue')
  },
  {
  path: '/manage/components',
  name: 'components',
  component: () => import('../views/ComponentsView.vue')
  },
  {
  path: '/manage/configurations',
  name: 'configurations', 
  component: () => import('../views/PCConfigurationsView.vue')
  },
  {
  path: '/manage/build-requests',
  name: 'build-requests',
  component: () => import('../views/BuildRequestsView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router