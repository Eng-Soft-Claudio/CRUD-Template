<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { onMounted, computed } from 'vue';

const authStore = useAuthStore();

const userDisplayName = computed(() => {
  if (authStore.currentUser) {
    return authStore.currentUser.full_name || authStore.currentUser.email;
  }
  return '';
});

onMounted(async () => {
  await authStore.tryAutoLogin();
});

const handleLogout = () => {
  authStore.logout();
};
</script>
<template>
  <div class="app-layout">
    <header class="app-header">
      <div class="nav-container">
        <div class="logo-area">
          <RouterLink to="/" class="project-name">CRUD Template</RouterLink>
        </div>
        <nav class="main-navigation">
          <RouterLink to="/">Home</RouterLink>
          <RouterLink to="/about">About</RouterLink>
        </nav>
        <div class="user-actions-area">
          <nav class="user-navigation">
            <template v-if="!authStore.isAuthenticated">
              <RouterLink to="/login">Login</RouterLink>
              <RouterLink to="/register">Registrar</RouterLink>
            </template>
            <template v-else>
              <span class="user-greeting">Olá, {{ userDisplayName }}!</span>
              <RouterLink to="/profile">Meu Perfil</RouterLink>
              <button @click="handleLogout" class="logout-button">Logout</button>
            </template>
          </nav>
        </div>
      </div>
    </header>

    <main class="main-content">
      <RouterView v-slot="{ Component }">
        <transition name="route-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </RouterView>
    </main>

    <footer class="app-footer">
      <p>© {{ new Date().getFullYear() }} CRUD Template. Todos os direitos reservados.</p>
    </footer>
  </div>
</template>

<style scoped>
:root {
  --header-height: 60px;
  --footer-height: 60px;
  --content-max-width: 1140px;
  --primary-color: #007bff;
  --primary-hover-color: #0056b3;
  --text-color-primary: #212529;
  --text-color-secondary: #6c757d;
  --text-on-dark-bg: #ffffff;
  --bg-light: #f8f9fa;
  --bg-dark: #343a40;
  --border-color: #dee2e6;
  --danger-color: #dc3545;
  --link-hover-bg: #e9ecef;
  --padding-sm: 8px;
  --padding-md: 12px;
  --padding-lg: 16px;
  --mobile-padding: 15px;
  --desktop-padding: 30px;
}

.app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #ffffff;
}

.app-header {
  background-color: var(--bg-light);
  border-bottom: 1px solid var(--border-color);
  width: 100%;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  line-height: 1.5;
}

.nav-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--padding-md) var(--mobile-padding);
  min-height: var(--header-height);
}

.logo-area {
  margin-bottom: var(--padding-md);
}

.project-name {
  font-size: 1.5em;
  font-weight: 700;
  color: var(--text-color-primary);
  text-decoration: none;
}

.main-navigation,
.user-navigation {
  display: flex;
  align-items: center;
  gap: var(--padding-sm);
  flex-wrap: wrap;
  justify-content: center;
}

.main-navigation {
  margin-bottom: var(--padding-md);
}

.user-actions-area {
  display: flex;
  align-items: center;
}

.main-navigation a,
.user-navigation a,
.user-navigation .user-greeting,
.user-navigation .logout-button {
  padding: var(--padding-sm) var(--padding-md);
  text-decoration: none;
  color: var(--primary-color);
  border-radius: 4px;
  transition: background-color 0.2s ease, color 0.2s ease;
  font-size: 0.95em;
  white-space: nowrap;
}

.main-navigation a:hover,
.user-navigation a:hover,
.user-navigation .logout-button:hover {
  background-color: var(--link-hover-bg);
  color: var(--primary-hover-color);
}

.main-navigation a.router-link-exact-active {
  background-color: var(--primary-color);
  color: white;
  font-weight: 600;
}
.main-navigation a.router-link-exact-active:hover {
  background-color: var(--primary-hover-color);
}

.user-greeting {
  color: var(--text-color-secondary);
  margin-right: var(--padding-sm);
  cursor: default;
  padding: var(--padding-sm) var(--padding-md);
}

.logout-button {
  background: none;
  border: 1px solid var(--danger-color);
  color: var(--danger-color);
  cursor: pointer;
}
.logout-button:hover {
  background-color: var(--danger-color) !important;
  color: white !important;
}

.main-content {
  width: 100%;
  max-width: var(--content-max-width);
  margin: 25px auto;
  padding: 0 var(--mobile-padding);
  flex-grow: 1;
}

.route-fade-enter-active,
.route-fade-leave-active {
  transition: opacity 0.15s ease;
}
.route-fade-enter-from,
.route-fade-leave-to {
  opacity: 0;
}

.app-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  text-align: center;
  padding: var(--padding-lg) var(--mobile-padding);
  background-color: var(--bg-dark);
  color: var(--text-on-dark-bg);
  font-size: 0.875em;
  width: 100%;
}

@media (min-width: 768px) {
  .nav-container {
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    max-width: var(--content-max-width);
    margin: 0 auto;
    padding: 0 var(--desktop-padding);
  }
  .logo-area {
    margin-bottom: 0;
    margin-right: 25px;
  }
  .main-navigation {
    margin-bottom: 0;
    margin-right: auto;
    gap: var(--padding-md);
  }
  .user-actions-area {
    margin-left: 20px;
  }
  .user-navigation {
    margin-bottom: 0;
    justify-content: flex-end;
  }
  .main-content {
    padding: 0;
    margin-top: 30px;
    margin-bottom: 30px;
  }
}

@media (min-width: 992px) {
  :root {
    --content-max-width: 960px;
  }
  .project-name {
    font-size: 1.7em;
  }
  .main-navigation a,
  .user-navigation a,
  .user-navigation .user-greeting,
  .user-navigation .logout-button {
    font-size: 1em;
  }
}

@media (min-width: 1200px) {
  :root {
    --content-max-width: 1140px;
  }
}

@media (min-width: 1400px) {
  :root {
    --content-max-width: 1320px;
    --desktop-padding: 40px;
  }
  .project-name {
    font-size: 1.8em;
  }
   nav a, nav .user-greeting, nav .logout-button {
    padding: 10px 16px;
  }
}
</style>