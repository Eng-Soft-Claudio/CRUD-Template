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
  <div class="view-card-container reset-password-layout">
    <h2>Redefinir Senha</h2>

    <Form :validation-schema="validationSchema" v-model:values="formValues" @submit="handleResetPassword"
      v-slot="{ errors, isSubmitting, meta }">
      <div class="form-group">
        <label for="inputToken-reset">Token de Recuperação:</label>
        <Field name="inputToken" type="text" id="inputToken-reset" class="form-control"
          :class="{ 'is-invalid': errors.inputToken }" placeholder="Cole o token aqui" />
        <ErrorMessage name="inputToken" class="invalid-feedback" />
        <small v-if="!route.query.token && !formValues.inputToken" class="form-text">
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

      <div v-if="errors.apiError" class="api-error-message form-feedback">
        {{ errors.apiError }}
      </div>
      <div v-else-if="authStore.error && !meta.dirty && meta.touched && !errors.apiError" class="api-error-message form-feedback">
         {{ authStore.error }}
      </div>

      <button type="submit" :disabled="isSubmitting || authStore.loading || !meta.valid && meta.touched"
        class="btn btn-primary btn-block">
        {{ (isSubmitting || authStore.loading) ? 'Redefinindo...' : 'Redefinir Senha' }}
      </button>
    </Form>
    <p v-if="!authStore.isAuthenticated" class="form-link-center">
      Lembrou sua senha? <router-link to="/login">Faça login</router-link>
    </p>
  </div>
</template>

<style scoped>
.reset-password-layout {
  max-width: 480px;
  margin: var(--padding-xl) auto;
}
.reset-password-layout h2 {
  text-align: center;
  margin-bottom: var(--padding-lg);
  font-size: 1.8em; /* Coerente com RequestPasswordRecoveryView */
}
.btn-block {
  width: 100%;
  margin-top: var(--padding-md);
}
.form-link-center {
  text-align: center;
  margin-top: var(--padding-lg);
  font-size: 0.9rem;
  font-family: var(--font-sans-ui);
}
.form-link-center a {
  font-weight: 600;
}
</style>