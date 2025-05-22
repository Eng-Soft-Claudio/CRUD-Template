<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
import { RouterLink } from 'vue-router';
const authStore = useAuthStore();
</script>

<template>
  <main>
    <h1>Bem-vindo à Home Page!</h1>
    <div v-if="authStore.isAuthenticated && authStore.user">
      <p>Você está logado como: {{ authStore.user.email }}</p>
      <p>ID: {{ authStore.user.id }}</p>
      <p>Nome: {{ authStore.user.full_name || 'Não informado' }}</p>
      <p>Ativo: {{ authStore.user.is_active }}</p>
      <p>Superuser: {{ authStore.user.is_superuser }}</p>
      <p>
        <!-- LINK PARA MUDAR SENHA -->
        <RouterLink to="/change-password">Alterar minha senha</RouterLink>
      </p>

    </div>
    <div v-else>
      <p>Por favor, faça login para ver mais.</p>
    </div>
  </main>
</template>

<style scoped>
  main p a {
    margin-top: 10px;
    display: inline-block;
    color: var(--color-link);
    text-decoration: underline;
  }
  main p a:hover {
    text-decoration: none;
  }
</style>