<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import type { UserCreate } from '@/types/user'; // Ajuste o caminho se necessário

const authStore = useAuthStore();

const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const fullName = ref(''); // Opcional

const passwordMismatch = ref(false);

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    passwordMismatch.value = true;
    authStore.setError('As senhas não coincidem.');
    return;
  }
  passwordMismatch.value = false;
  authStore.setError(null);

  const userData: UserCreate = {
    email: email.value,
    password: password.value,
    full_name: fullName.value || null, // Envia null se vazio
  };

  try {
    await authStore.register(userData);
    // O store auth já redireciona para login após registro bem-sucedido
  } catch (error) {
    // Erro já é tratado no store, mas pode adicionar lógica extra aqui se precisar
    console.error('Falha no registro do componente:', error);
  }
};
</script>

<template>
  <div class="register-container">
    <h2>Registrar</h2>
    <form @submit.prevent="handleRegister">
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div>
        <label for="fullName">Nome Completo (Opcional):</label>
        <input type="text" id="fullName" v-model="fullName" />
      </div>
      <div>
        <label for="password">Senha:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <div>
        <label for="confirmPassword">Confirmar Senha:</label>
        <input type="password" id="confirmPassword" v-model="confirmPassword" required />
      </div>
      <button type="submit" :disabled="authStore.loading">
        {{ authStore.loading ? 'Registrando...' : 'Registrar' }}
      </button>
      <p v-if="passwordMismatch" class="error-message">As senhas não coincidem.</p>
      <p v-if="authStore.error && !passwordMismatch" class="error-message">{{ authStore.error }}</p>
    </form>
     <p>
      Já tem uma conta? <router-link to="/login">Faça login</router-link>
    </p>
  </div>
</template>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.register-container div {
  margin-bottom: 15px;
}
.register-container label {
  display: block;
  margin-bottom: 5px;
}
.register-container input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
.error-message {
  color: red;
  margin-top: 10px;
}
</style>