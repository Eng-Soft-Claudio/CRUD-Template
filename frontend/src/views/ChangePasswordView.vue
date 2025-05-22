<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
import type { UserPasswordChange } from '@/types/user';
import { Form, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';

const authStore = useAuthStore();

const validationSchema = yup.object({
  currentPassword: yup.string().required('A senha atual é obrigatória'),
  newPassword: yup.string()
    .required('A nova senha é obrigatória')
    .min(8, 'A nova senha deve ter pelo menos 8 caracteres')
    .notOneOf([yup.ref('currentPassword')], 'A nova senha não pode ser igual à senha atual'),
  newPasswordConfirm: yup.string()
    .required('A confirmação da nova senha é obrigatória')
    .oneOf([yup.ref('newPassword')], 'As novas senhas não coincidem'),
});

const initialValues = {
  currentPassword: '',
  newPassword: '',
  newPasswordConfirm: '',
};

const handleChangePassword = async (values: Record<string, any>, { setErrors, resetForm }: any) => {
  authStore.setError(null);

  const passwordData: UserPasswordChange = {
    current_password: values.currentPassword,
    new_password: values.newPassword,
    new_password_confirm: values.newPasswordConfirm,
  };

  try {
    await authStore.changePassword(passwordData);
    resetForm();
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
        setErrors({ apiError: 'Falha ao alterar a senha.' });
      }
    } else {
      setErrors({ apiError: 'Ocorreu um erro desconhecido ao tentar alterar a senha.' });
    }
    console.error('Erro ao alterar senha no componente:', error);
  }
};
</script>

<template>
  <div class="change-password-container">
    <h2>Alterar Senha</h2>
    <Form :validation-schema="validationSchema" :initial-values="initialValues" @submit="handleChangePassword" v-slot="{ errors, isSubmitting, meta }">
      <div class="form-group">
        <label for="currentPassword-change">Senha Atual:</label>
        <Field name="currentPassword" type="password" id="currentPassword-change" class="form-control" :class="{'is-invalid': errors.currentPassword }" />
        <ErrorMessage name="currentPassword" class="invalid-feedback" />
      </div>

      <div class="form-group">
        <label for="newPassword-change">Nova Senha:</label>
        <Field name="newPassword" type="password" id="newPassword-change" class="form-control" :class="{'is-invalid': errors.newPassword }" />
        <ErrorMessage name="newPassword" class="invalid-feedback" />
      </div>

      <div class="form-group">
        <label for="newPasswordConfirm-change">Confirmar Nova Senha:</label>
        <Field name="newPasswordConfirm" type="password" id="newPasswordConfirm-change" class="form-control" :class="{'is-invalid': errors.newPasswordConfirm }" />
        <ErrorMessage name="newPasswordConfirm" class="invalid-feedback" />
      </div>

      <div v-if="errors.apiError" class="api-error-message">
        {{ errors.apiError }}
      </div>
      <div v-else-if="authStore.error && !meta.dirty && meta.touched" class="api-error-message">
         {{ authStore.error }}
      </div>

      <button type="submit" :disabled="isSubmitting || authStore.loading || !meta.valid && meta.touched" class="btn-submit">
        {{ (isSubmitting || authStore.loading) ? 'Alterando...' : 'Alterar Senha' }}
      </button>
    </Form>
  </div>
</template>

<style scoped>
.change-password-container {
  max-width: 450px;
  margin: 50px auto;
  padding: 30px;
  background-color: #f9fafb;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
.change-password-container h2 {
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
</style>