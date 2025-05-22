<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import type { PasswordResetForm } from '@/types/user';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const tokenFromQuery = ref('');
const inputToken = ref(''); // v-model para o campo de input do token
const newPassword = ref('');
const newPasswordConfirm = ref('');

const successMessage = ref<string | null>(null);
const generalError = ref<string | null>(null);
const showForm = ref(true); // Sempre mostrar o formulário nesta view

const clearMessages = () => {
  authStore.setError(null);
  successMessage.value = null;
  generalError.value = null;
};

onMounted(() => {
  const queryToken = route.query.token;
  if (typeof queryToken === 'string' && queryToken) {
    tokenFromQuery.value = queryToken; // Guarda o token da URL se vier
    inputToken.value = queryToken;    // Preenche o campo do formulário com ele
  }
  // O formulário será exibido independentemente para o usuário colar, se necessário
});

// Atualiza o token do input se a query da rota mudar
watch(() => route.query.token, (newTokenValue) => {
    clearMessages();
    const newTokenString = Array.isArray(newTokenValue) ? newTokenValue[0] : newTokenValue; // Lida com array de query params
    if (typeof newTokenString === 'string' && newTokenString) {
        tokenFromQuery.value = newTokenString;
        inputToken.value = newTokenString;
    }
});


const handleResetPassword = async () => {
  clearMessages();

  if (!inputToken.value) {
    generalError.value = 'O token de redefinição é obrigatório.';
    return;
  }
  if (!newPassword.value || !newPasswordConfirm.value) {
    generalError.value = 'Nova senha e confirmação são obrigatórias.';
    return;
  }
  if (newPassword.value !== newPasswordConfirm.value) {
    generalError.value = 'As senhas não coincidem.';
    return;
  }

  const resetData: PasswordResetForm = {
    token: inputToken.value,
    new_password: newPassword.value,
    new_password_confirm: newPasswordConfirm.value,
  };

  try {
    await authStore.resetPassword(resetData);
    // A store já lida com o alert e redirecionamento para login.
  } catch (error: any) {
     if (!authStore.error) {
        generalError.value = error.message || 'Ocorreu um erro ao redefinir a senha. Verifique o token e os dados.';
    }
    console.error('Erro ao redefinir senha no componente:', error);
  }
};
</script>

<template>
  <div class="reset-password-container">
    <h2>Redefinir Senha</h2>

    <p v-if="generalError && !authStore.error" class="error-message">{{ generalError }}</p>
    <p v-if="authStore.error" class="error-message">{{ authStore.error }}</p>
    <p v-if="successMessage" class="success-message">{{ successMessage }}</p>

    <!-- O formulário sempre é exibido; a validação se o token existe é feita no submit -->
    <form @submit.prevent="handleResetPassword">
      <div>
        <label for="inputToken">Token de Recuperação:</label>
        <input type="text" id="inputToken" v-model="inputToken" required placeholder="Cole o token dos logs do backend aqui" />
         <small>
           Se o token veio na URL, ele será preenchido. Caso contrário, cole o token dos logs do backend aqui.
         </small>
      </div>
      <div>
        <label for="newPassword">Nova Senha:</label>
        <input type="password" id="newPassword" v-model="newPassword" required />
      </div>
      <div>
        <label for="newPasswordConfirm">Confirmar Nova Senha:</label>
        <input type="password" id="newPasswordConfirm" v-model="newPasswordConfirm" required />
      </div>
      <button type="submit" :disabled="authStore.loading || !inputToken">
        {{ authStore.loading ? 'Redefinindo...' : 'Redefinir Senha' }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.reset-password-container {
  max-width: 450px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.reset-password-container h2 {
  text-align: center;
  margin-bottom: 20px;
}
.reset-password-container form div { 
  margin-bottom: 15px;
}
.reset-password-container label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}
.reset-password-container input {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.reset-password-container input:disabled {
  background-color: #eee;
}
.error-message, .success-message, .info-message {
  margin-top: 15px; /* Aumentei um pouco a margem */
  padding: 10px;
  border-radius: 4px;
  font-size: 0.9em;
  border-width: 1px;
  border-style: solid;
}
.error-message { color: #D8000C; background-color: #FFD2D2; border-color: #FFB8B8; }
.success-message { color: green; background-color: #d4edda; border-color: #c3e6cb;}
.info-message { color: #004085; background-color: #cce5ff; border-color: #b8daff;}
small {
    font-size: 0.8em;
    color: #666;
    display: block;
    margin-top: 5px;
}
button {
  width: 100%;
  padding: 12px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
  font-size: 1em;
}
button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
button:not(:disabled):hover {
  background-color: #0056b3;
}
</style>