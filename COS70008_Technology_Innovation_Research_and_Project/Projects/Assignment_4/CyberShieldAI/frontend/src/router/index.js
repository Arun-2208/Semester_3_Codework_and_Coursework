

import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from '../views/LandingPage.vue';
import Register from '../views/Register.vue';
import Login from '../views/Login.vue';
import Dashboard from '../views/Dashboard.vue';
import ScanFile from '../views/ScanFile.vue';
import ScanHistory from '../views/ScanHistory.vue';
import UpdateModel from '../views/UpdateModel.vue';
import Analytics from '../views/Analytics.vue';

const routes = [
  { path: '/', component: LandingPage },
  { path: '/register', component: Register },
  { path: '/login', component: Login },
  {
    path: '/dashboard',
    component: Dashboard,
    children: [
      { path: 'scan', component: ScanFile },
      { path: 'history', component: ScanHistory },
      { path: 'update-model', component: UpdateModel },
      { path: 'analytics', component: Analytics }
    ]
  }
];

export default createRouter({
  history: createWebHistory(),
  routes
});
