import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import ChangePasswordView from '../views/ChangePasswordView.vue';
import RequestPasswordRecoveryView from '../views/RequestPasswordRecoveryView.vue';
import ResetPasswordView from '../views/ResetPasswordView.vue';
import UserProfileView from '../views/UserProfileView.vue'; 
import { useAuthStore } from '@/stores/auth'; 

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true } 
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'), 
      meta: { requiresAuth: true } 
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { guestOnly: true } 
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { guestOnly: true } 
    },
    { 
      path: '/change-password',
      name: 'change-password',
      component: ChangePasswordView,
      meta: { requiresAuth: true } 
    },
    { 
      path: '/forgot-password',
      name: 'forgot-password',
      component: RequestPasswordRecoveryView,
      meta: { guestOnly: true } 
    },
    { 
      path: '/reset-password',
      name: 'reset-password',
      component: ResetPasswordView,
      meta: { guestOnly: true }
    },
    { 
      path: '/profile',
      name: 'profile',
      component: UserProfileView,
      meta: { requiresAuth: true } 
    }
  ]
});

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  if (authStore.token && !authStore.user) {
    await authStore.tryAutoLogin();
  }
  
  const isAuthenticated = authStore.isAuthenticated;

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login' });
  } else if (to.meta.guestOnly && isAuthenticated) {
    next({ name: 'home' });
  }
  else {
    next();
  }
});

export default router;