<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { onMounted } from 'vue';

const authStore = useAuthStore();

onMounted(async () => {
  // Tenta carregar o usuário se um token existir no localStorage
  // Isso é útil para manter o usuário logado após refresh da página
  await authStore.tryAutoLogin();
});

const handleLogout = () => {
  authStore.logout();
};
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
        <template v-if="!authStore.isAuthenticated">
          <RouterLink to="/login">Login</RouterLink>
          <RouterLink to="/register">Registrar</RouterLink>
        </template>
        <template v-else>
          <span>Olá, {{ authStore.user?.email }}!</span>
          <button @click="handleLogout">Logout</button>
        </template>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
  border-bottom: 1px solid #ccc;
  margin-bottom: 20px;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 1rem;
  padding-bottom: 1rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

nav span, nav button {
  padding: 0 1rem;
  display: inline-block;
}
nav button {
  background: none;
  border: none;
  color: var(--color-link);
  cursor: pointer;
  font-size: 12px;
  text-decoration: underline;
}
nav button:hover {
  text-decoration: none;
}

/* Ajuste para telas maiores se necessário, o padrão do create-vue já tem isso */
@media (min-width: 1024px) {
  /* ... */
}
</style>