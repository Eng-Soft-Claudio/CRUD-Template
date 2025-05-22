<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();
const email = ref('');
const successInfoMessage = ref<string | null>(null);
const generalError = ref<string | null>(null); // Erros que não vêm do store auth

// Determina se está em ambiente de desenvolvimento
const isDev = import.meta.env.DEV;

const clearMessages = () => {
  authStore.setError(null);
  successInfoMessage.value = null;
  generalError.value = null;
};

const handleRequestRecovery = async () => {
  clearMessages();

  if (!email.value) {
    authStore.setError('O campo email é obrigatório.'); // Usa o erro do store
    return;
  }

  console.log('FRONTEND (RequestPasswordRecoveryView): Tentando solicitar recuperação para:', email.value);

  try {
    await authStore.requestPasswordRecovery(email.value);
    console.log('FRONTEND (RequestPasswordRecoveryView): Solicitação de recuperação enviada ao store.');

    successInfoMessage.value = 'Solicitação enviada! Para desenvolvimento, verifique os logs do seu backend para obter o token de recuperação. Você será redirecionado em breve...';
    email.value = ''; // Limpa o campo

    if (isDev) {
        // Apenas em DEV: Redireciona para a página de reset-password após um delay
        setTimeout(() => {
          router.push('/reset-password'); // Redireciona SEM o token na URL
        }, 4000); // Aumentei um pouco o delay para dar tempo de ler a mensagem
    }

  } catch (error: any) {
    // A ação do store deve idealmente tratar e setar o authStore.error
    if (!authStore.error) {
      // Fallback se o store não setou um erro
      generalError.value = error.message || 'Falha ao solicitar recuperação. Tente novamente mais tarde.';
    }
    console.error("FRONTEND (RequestPasswordRecoveryView): Erro na solicitação de recuperação de senha:", error);
  }
};
</script>

<template>
  <div class="request-recovery-container">
    <h2>Esqueci Minha Senha</h2>
    <p>
      Insira seu endereço de email. Se uma conta estiver associada, instruções para redefinir
      sua senha serão enviadas (em desenvolvimento, o token aparecerá nos logs do backend).
    </p>
    <form @submit.prevent="handleRequestRecovery">
      <div>
        <label for="email-recovery">Email:</label>
        <input type="email" id="email-recovery" v-model="email" required placeholder="seuemail@exemplo.com" />
      </div>
      <button type="submit" :disabled="authStore.loading">
        {{ authStore.loading ? 'Enviando...' : 'Solicitar Recuperação' }}
      </button>

      <p v-if="successInfoMessage" class="info-message">{{ successInfoMessage }}</p>
      <p v-if="generalError && !authStore.error" class="error-message">{{ generalError }}</p>
      <p v-if="authStore.error" class="error-message">{{ authStore.error }}</p>
    </form>
    <hr />
    <p>
      Lembrou sua senha? <router-link to="/login">Faça login</router-link>
    </p>
    <div v-if="isDev" class="dev-info">
      <p>
        <strong>Fluxo de Desenvolvimento:</strong>
        Após solicitar, você será redirecionado para a página de redefinição.
        Pegue o token nos logs do seu container backend e cole-o no campo apropriado na próxima tela.
      </p>
    </div>
  </div>
</template>

<style scoped>
/* Estilos mantidos da sua última versão do request-recovery-container */
.request-recovery-container {
  max-width: 450px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.request-recovery-container h2 {
  text-align: center;
  margin-bottom: 20px;
}
.request-recovery-container p {
  margin-bottom: 15px;
  line-height: 1.6;
  font-size: 0.95em;
  color: #555;
}
/* Ajuste para div do formulário não pegar estilo global de .request-recovery-container div se for genérico */
.request-recovery-container form div {
  margin-bottom: 15px;
}
.request-recovery-container label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}
.request-recovery-container input[type="email"] {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  border: 1px solid #ddd;
  border-radius: 4px;
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
.info-message {
  color: #004085;
  background-color: #cce5ff;
  border: 1px solid #b8daff;
  padding: 10px;
  border-radius: 4px;
  margin-top: 15px;
  font-size: 0.9em;
}
.error-message {
  color: #D8000C;
  background-color: #FFD2D2;
  border: 1px solid #FFB8B8;
  padding: 10px;
  border-radius: 4px;
  margin-top: 15px;
  font-size: 0.9em;
}
hr {
  margin-top: 20px;
  margin-bottom: 20px;
  border: 0;
  border-top: 1px solid #eee;
}
/* Para os links como "Faça login" */
.request-recovery-container > p a {
  color: #007bff;
  text-decoration: none;
}
.request-recovery-container > p a:hover {
  text-decoration: underline;
}
.dev-info {
  margin-top: 20px;
  padding: 10px;
  background-color: #fff3cd;
  border: 1px solid #ffeeba;
  color: #856404;
  border-radius: 4px;
  font-size: 0.9em;
}
.dev-info a {
  font-weight: bold;
}
</style>