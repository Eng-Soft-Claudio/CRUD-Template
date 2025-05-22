<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import type { UserPasswordChange } from '@/types/user'; 
import router from '@/router';



const authStore = useAuthStore();

const currentPassword = ref('');
const newPassword = ref('');
const newPasswordConfirm = ref('');

const successMessage = ref<string | null>(null);
const generalError = ref<string | null>(null); 

const clearMessages = () => {
  authStore.setError(null);
  successMessage.value = null;
  generalError.value = null;
};

const handleChangePassword = async () => {
  clearMessages();

  if (!currentPassword.value || !newPassword.value || !newPasswordConfirm.value) {
    generalError.value = 'Todos os campos são obrigatórios.';
    return;
  }

  if (newPassword.value !== newPasswordConfirm.value) {
    generalError.value = 'A nova senha e a confirmação não coincidem.';
    return;
  }

  const passwordData: UserPasswordChange = { 
    current_password: currentPassword.value,
    new_password: newPassword.value,
    new_password_confirm: newPasswordConfirm.value,
  };

  try {
    await authStore.changePassword(passwordData); 
    successMessage.value = 'Senha alterada com sucesso! Você pode precisar fazer login novamente se sua sessão foi invalidada (não é o caso padrão aqui).';
    currentPassword.value = '';
    newPassword.value = '';
    newPasswordConfirm.value = '';
  } catch (error: any) {
    if (!authStore.error) {
        generalError.value = error.message || 'Ocorreu um erro ao tentar alterar a senha.';
    }
    console.error('Erro ao alterar senha no componente:', error);
  }
};
</script>

<template>
  <div class="change-password-container">
    <h2>Alterar Senha</h2>
    <form @submit.prevent="handleChangePassword">
      <div>
        <label for="currentPassword">Senha Atual:</label>
        <input type="password" id="currentPassword" v-model="currentPassword" required />
      </div>
      <div>
        <label for="newPassword">Nova Senha:</label>
        <input type="password" id="newPassword" v-model="newPassword" required />
      </div>
      <div>
        <label for="newPasswordConfirm">Confirmar Nova Senha:</label>
        <input type="password" id="newPasswordConfirm" v-model="newPasswordConfirm" required />
      </div>

      <button type="submit" :disabled="authStore.loading">
        {{ authStore.loading ? 'Alterando...' : 'Alterar Senha' }}
      </button>

      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
      <p v-if="authStore.error" class="error-message">{{ authStore.error }}</p>
      <p v-if="generalError" class="error-message">{{ generalError }}</p>
    </form>
  </div>
</template>

<style scoped>
.change-password-container {
  max-width: 450px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}
.change-password-container div {
  margin-bottom: 15px;
}
.change-password-container label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}
.change-password-container input {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  border: 1px solid #ddd;
  border-radius: 4px;
}
button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}
button:disabled {
  background-color: #ccc;
}
button:not(:disabled):hover {
  background-color: #0056b3;
}
.error-message {
  color: red;
  margin-top: 10px;
  font-size: 0.9em;
}
.success-message {
  color: green;
  margin-top: 10px;
  font-size: 0.9em;
}
</style>