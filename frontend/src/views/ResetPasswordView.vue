<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import type { LocationQueryValue } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import type { PasswordResetForm } from '@/types/user';
import { Form, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';

const route = useRoute();
const authStore = useAuthStore();

const validationSchema = yup.object({
  inputToken: yup.string().required('O token de recuperação é obrigatório'),
  newPassword: yup.string()
    .required('A nova senha é obrigatória')
    .min(8, 'A nova senha deve ter pelo menos 8 caracteres'),
  newPasswordConfirm: yup.string()
    .required('A confirmação da nova senha é obrigatória')
    .oneOf([yup.ref('newPassword')], 'As novas senhas não coincidem'),
});

const formValues = ref({
  inputToken: '',
  newPassword: '',
  newPasswordConfirm: '',
});

const updateTokenFromQuery = (queryParam: LocationQueryValue | LocationQueryValue[] | null | undefined) => {
  let extractedString: string | null = null;

  if (Array.isArray(queryParam)) {
    extractedString = queryParam[0];
  } else if (queryParam !== undefined) { 
    extractedString = queryParam; 
  }

  if (typeof extractedString === 'string' && extractedString) {
    formValues.value.inputToken = extractedString;
  } else {
    formValues.value.inputToken = ''; 
  }
};

onMounted(() => {
  updateTokenFromQuery(route.query.token);
});

watch(() => route.query.token, (newToken) => {
  authStore.setError(null);
  updateTokenFromQuery(newToken);
});

const handleResetPassword = async (values: Record<string, any>, { setErrors }: any) => {
  authStore.setError(null);

  const resetData: PasswordResetForm = {
    token: values.inputToken,
    new_password: values.newPassword,
    new_password_confirm: values.newPasswordConfirm,
  };

  try {
    await authStore.resetPassword(resetData);
  } catch (error: any) {
    if (authStore.error) {
      setErrors({ apiError: authStore.error });
    } else if (error.response?.data?.detail) {
      const detail = error.response.data.detail;
      if (typeof detail === 'string') {
        setErrors({ apiError: detail });
      } else if (Array.isArray(detail) && detail[0]?.msg) {
        setErrors({ apiError: detail[0].msg });
      } else {
        setErrors({ apiError: 'Falha ao redefinir a senha.' });
      }
    } else {
      setErrors({ apiError: 'Ocorreu um erro desconhecido ao tentar redefinir a senha.' });
    }
    console.error('Erro ao redefinir senha no componente:', error);
  }
};
</script>

<template>
  <div class="reset-password-container">
    <h2>Redefinir Senha</h2>
    <Form :validation-schema="validationSchema" :initial-values="formValues" @submit="handleResetPassword"
      v-slot="{ errors, isSubmitting, meta, values }">
      <div class="form-group">
        <label for="inputToken-reset">Token de Recuperação:</label>
        <Field name="inputToken" type="text" id="inputToken-reset" class="form-control"
          :class="{ 'is-invalid': errors.inputToken }" placeholder="Cole o token aqui" />
        <ErrorMessage name="inputToken" class="invalid-feedback" />
        <small v-if="!route.query.token && !values.inputToken" class="form-text">
          Cole o token dos logs do backend ou o token recebido por email.
        </small>
      </div>

      <div class="form-group">
        <label for="newPassword-reset">Nova Senha:</label>
        <Field name="newPassword" type="password" id="newPassword-reset" class="form-control"
          :class="{ 'is-invalid': errors.newPassword }" />
        <ErrorMessage name="newPassword" class="invalid-feedback" />
      </div>

      <div class="form-group">
        <label for="newPasswordConfirm-reset">Confirmar Nova Senha:</label>
        <Field name="newPasswordConfirm" type="password" id="newPasswordConfirm-reset" class="form-control"
          :class="{ 'is-invalid': errors.newPasswordConfirm }" />
        <ErrorMessage name="newPasswordConfirm" class="invalid-feedback" />
      </div>

      <div v-if="errors.apiError" class="api-error-message">
        {{ errors.apiError }}
      </div>
      <div v-else-if="authStore.error && !meta.dirty && meta.touched && !errors.apiError" class="api-error-message">
        {{ authStore.error }}
      </div>

      <button type="submit" :disabled="isSubmitting || authStore.loading || !meta.valid && meta.touched"
        class="btn-submit">
        {{ (isSubmitting || authStore.loading) ? 'Redefinindo...' : 'Redefinir Senha' }}
      </button>
    </Form>
    <p v-if="!authStore.isAuthenticated" class="login-link">
      Lembrou sua senha? <router-link to="/login">Faça login</router-link>
    </p>
  </div>
</template>

<style scoped>
.reset-password-container {
  max-width: 480px;
  margin: 50px auto;
  padding: 30px;
  background-color: #f9fafb;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.reset-password-container h2 {
  text-align: center;
  margin-bottom: 25px;
  font-size: 1.8em;
  color: #1f2937;
  font-weight: 600;
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

.form-text {
  display: block;
  font-size: 0.8em;
  color: #6b7280;
  margin-top: 6px;
}

.api-error-message {
  color: var(--danger-color, #ef4444);
  background-color: #fee2e2;
  border: 1px solid #fca5a5;
  padding: 10px;
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

.login-link {
  text-align: center;
  margin-top: 25px;
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
</style>