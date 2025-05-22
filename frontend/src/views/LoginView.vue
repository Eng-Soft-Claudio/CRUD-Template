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
    <p>
      <router-link to="/forgot-password">Esqueci minha senha</router-link> 
    </p>
    <p>
      Não tem uma conta? <router-link to="/register">Registre-se</router-link>
    </p>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.login-container div {
  margin-bottom: 15px;
}
.login-container label {
  display: block;
  margin-bottom: 5px;
}
.login-container input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
.error-message {
  color: red;
  margin-top: 10px;
}
</style>