<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import { Form, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';

const authStore = useAuthStore();
const router = useRouter();

const isDev = import.meta.env.DEV;

const validationSchema = yup.object({
  email: yup.string().required('O email é obrigatório').email('Formato de email inválido'),
});

const initialValues = {
  email: '',
};

const successInfoMessage = ref<string | null>(null);

const handleRequestRecovery = async (values: Record<string, any>, { setErrors, resetForm }: any) => {
  successInfoMessage.value = null;
  authStore.setError(null);

  try {
    await authStore.requestPasswordRecovery(values.email);
    successInfoMessage.value = 'Solicitação enviada! Para desenvolvimento, verifique os logs do seu backend para obter o token de recuperação. Você será redirecionado em breve...';
    resetForm();

    if (isDev) {
      setTimeout(() => {
        router.push('/reset-password');
      }, 4000);
    }
  } catch (error: any) {
    if (authStore.error) {
        setErrors({ apiError: authStore.error });
    } else if (error.message) {
        setErrors({ apiError: error.message });
    } else {
        setErrors({ apiError: 'Falha ao solicitar recuperação. Tente novamente.' });
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
    <Form :validation-schema="validationSchema" :initial-values="initialValues" @submit="handleRequestRecovery" v-slot="{ errors, isSubmitting, meta }">
      <div class="form-group">
        <label for="email-recovery">Email:</label>
        <Field name="email" type="email" id="email-recovery" class="form-control" :class="{'is-invalid': errors.email }" placeholder="seuemail@exemplo.com" />
        <ErrorMessage name="email" class="invalid-feedback" />
      </div>

      <div v-if="successInfoMessage && !errors.apiError" class="info-message">
        {{ successInfoMessage }}
      </div>
      <div v-if="errors.apiError" class="api-error-message">
        {{ errors.apiError }}
      </div>
      <div v-else-if="authStore.error && !meta.dirty && meta.touched && !errors.apiError" class="api-error-message">
        {{ authStore.error }}
      </div>

      <button type="submit" :disabled="isSubmitting || authStore.loading || !meta.valid && meta.touched" class="btn-submit">
        {{ (isSubmitting || authStore.loading) ? 'Enviando...' : 'Solicitar Recuperação' }}
      </button>
    </Form>
    <hr class="divider"/>
    <p class="login-link">
      Lembrou sua senha? <router-link to="/login">Faça login</router-link>
    </p>
    <div v-if="isDev" class="dev-instructions">
      <p>
        <strong>Fluxo de Desenvolvimento:</strong>
        Após solicitar, você será redirecionado para a página de redefinição.
        Pegue o token nos logs do seu container backend e cole-o no campo apropriado na próxima tela.
      </p>
    </div>
  </div>
</template>

<style scoped>
.request-recovery-container {
  max-width: 480px;
  margin: 50px auto;
  padding: 30px;
  background-color: #f9fafb;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
.request-recovery-container h2 {
  text-align: center;
  margin-bottom: 20px;
  font-size: 1.8em;
  color: #1f2937;
  font-weight: 600;
}
.request-recovery-container > p {
  text-align: center;
  margin-bottom: 25px;
  line-height: 1.6;
  font-size: 0.95em;
  color: #4b5563;
}
.form-group {
  margin-bottom: 20px;
}
.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #374151;
}
.form-control {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 1em;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.form-control:focus {
  border-color: var(--primary-color, #3b82f6);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25);
  outline: none;
}
.form-control.is-invalid {
  border-color: var(--danger-color, #ef4444);
}
.invalid-feedback {
  display: block;
  color: var(--danger-color, #ef4444);
  font-size: 0.875em;
  margin-top: 6px;
}
.info-message {
  color: #055160;
  background-color: #cff4fc;
  border: 1px solid #b6effb;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 20px;
  text-align: center;
  font-size: 0.9em;
}
.api-error-message {
  color: var(--danger-color, #ef4444);
  background-color: #fee2e2;
  border: 1px solid #fca5a5;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 20px;
  text-align: center;
  font-size: 0.9em;
}
.btn-submit {
  width: 100%;
  background-color: var(--primary-color, #2563eb);
  color: white;
  padding: 12px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  font-size: 1em;
  cursor: pointer;
  transition: background-color 0.2s;
}
.btn-submit:hover:not(:disabled) {
  background-color: var(--primary-hover-color, #1e40af);
}
.btn-submit:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}
.divider {
  margin-top: 25px;
  margin-bottom: 25px;
  border: 0;
  border-top: 1px solid #e5e7eb;
}
.login-link {
  text-align: center;
  font-size: 0.9em;
}
.login-link a {
  color: var(--primary-color, #10b981);
  text-decoration: none;
  font-weight: 500;
}
.login-link a:hover {
  text-decoration: underline;
}
.dev-instructions {
  margin-top: 25px;
  padding: 12px;
  background-color: #fffbeb;
  border: 1px solid #fef3c7;
  color: #78350f;
  border-radius: 6px;
  font-size: 0.85em;
  text-align: left;
}
.dev-instructions strong {
  font-weight: 600;
}
</style>