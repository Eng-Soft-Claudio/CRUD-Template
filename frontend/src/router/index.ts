import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import { useAuthStore } from '@/stores/auth'; // Importe o store

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true } // Rota protegida
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'), // lazy-load
      meta: { requiresAuth: true } // Exemplo de outra rota protegida
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { guestOnly: true } // Apenas para usuários não logados
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { guestOnly: true } // Apenas para usuários não logados
    }
  ]
});

// Navigation Guard
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  // Tenta carregar o usuário se houver um token (ex: após refresh da página)
  // mas só se o usuário ainda não foi carregado.
  // Evita chamadas desnecessárias se já navegou e o usuário está no store.
  if (authStore.token && !authStore.user) {
    await authStore.tryAutoLogin();
  }
  
  const isAuthenticated = authStore.isAuthenticated;

  if (to.meta.requiresAuth && !isAuthenticated) {
    // Se a rota requer autenticação e o usuário não está logado, redireciona para login
    next({ name: 'login' });
  } else if (to.meta.guestOnly && isAuthenticated) {
    // Se a rota é apenas para convidados (login, register) e o usuário está logado, redireciona para home
    next({ name: 'home' });
  }
  else {
    // Caso contrário, permite a navegação
    next();
  }
});

export default router;