<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
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
    </div>
    <div v-else>
      <p>Por favor, faça login para ver mais.</p>
    </div>
  </main>
</template>