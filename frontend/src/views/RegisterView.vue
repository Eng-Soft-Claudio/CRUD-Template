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
    <p class="login-redirect">
      Já tem uma conta? <router-link to="/login">Faça login</router-link>
    </p>
  </div>
</template>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 60px auto;
  padding: 30px;
  background-color: #f1f2f3;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.register-container h2 {
  text-align: center;
  margin-bottom: 24px;
  font-size: 24px;
  color: #111827;
}

.register-container div {
  margin-bottom: 20px;
}

.register-container label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  color: #374151;
}

.register-container input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  background-color: #fefce8;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.register-container input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
  outline: none;
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

.login-redirect {
  text-align: center;
  padding-top: 8%;
  font-size: 14px;
}

a {
  color: #10b981;
  text-decoration: none;
  font-weight: 500;
}

a:hover {
  text-decoration: underline;
}

/* Responsivo */
@media (max-width: 480px) {
  .register-container {
    margin: 20px;
    padding: 24px 18px;
  }

  .register-container h2 {
    font-size: 20px;
  }

  button[type="submit"] {
    font-size: 14px;
    padding: 10px;
  }
}
</style>
