<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
import { RouterLink } from 'vue-router';
const authStore = useAuthStore();
</script>

<template>
  <main class="home-container">
    <h1 class="home-title">Bem-vindo à Home Page!</h1>

    <div v-if="authStore.isAuthenticated && authStore.user" class="user-info">
      <p><strong>Email:</strong> {{ authStore.user.email }}</p>
      <p><strong>ID:</strong> {{ authStore.user.id }}</p>
      <p><strong>Nome:</strong> {{ authStore.user.full_name || 'Não informado' }}</p>
      <p><strong>Ativo:</strong> {{ authStore.user.is_active ? 'Sim' : 'Não' }}</p>
      <p><strong>Superuser:</strong> {{ authStore.user.is_superuser ? 'Sim' : 'Não' }}</p>
      <p class="link-action">
        <RouterLink to="/change-password">Alterar minha senha</RouterLink>
      </p>
    </div>

    <div v-else class="unauth-message">
      <p>Por favor, faça login para ver mais.</p>
    </div>
  </main>
</template>

<style scoped>
.home-container {
  min-height: 60vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  max-width: 400px;
  margin: 60px auto;
  padding: 30px;
  background-color: #f1f2f3;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.home-title {
  font-size: 28px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 32px;
}

.user-info p,
.unauth-message p {
  font-size: 16px;
  margin-bottom: 12px;
  color: #374151;
}

.link-action a {
  color: #2563eb;
  text-decoration: none;
  font-weight: 600;
}

.link-action a:hover {
  text-decoration: underline;
}
</style>
