<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const email = ref('');
const password = ref('');

const handleLogin = async () => {
  if (!email.value || !password.value) {
    authStore.setError('Email e senha são obrigatórios.');
    return;
  }
  await authStore.login({ username: email.value, password: password.value });
  if (authStore.isAuthenticated) {
    router.push('/'); 
  }
};
</script>

<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div>
        <label for="password">Senha:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit" :disabled="authStore.loading">
        {{ authStore.loading ? 'Entrando...' : 'Entrar' }}
      </button>
      <p v-if="authStore.error" class="error-message">{{ authStore.error }}</p>
    </form>
    <p class="forgot-password">
      <router-link to="/forgot-password">Esqueci minha senha</router-link> 
    </p>
    <p class="register">
      Não tem uma conta? <router-link to="/register">Registre-se</router-link>
    </p>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 60px auto;
  padding: 30px;
  background-color: #f1f2f3;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.login-container h2 {
  text-align: center;
  margin-bottom: 24px;
  font-size: 24px;
  color: #111827;
}

.login-container div {
  margin-bottom: 20px;
}

.login-container label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  color: #374151;
}

.login-container input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  background-color: #fefce8;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.login-container input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
  outline: none;
}
.forgot-password{
  text-align: center;
  padding-top: 8%;
}
.register{
  text-align: center;
  padding-top: 8%;
}

button[type="submit"] {
  width: 100%;
  background-color: #2563eb;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

button[type="submit"]:hover {
  background-color: #1e40af;
}

button[type="submit"]:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.error-message {
  color: #dc2626;
  font-size: 14px;
  margin-top: 12px;
  text-align: center;
}

a {
  color: #10b981;
  text-decoration: none;
  font-weight: 500;
}

a:hover {
  text-decoration: underline;
}
</style>