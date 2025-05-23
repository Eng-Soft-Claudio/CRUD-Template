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
  <div class="view-card-container change-password-layout">
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

      <div v-if="errors.apiError" class="api-error-message form-feedback">
        {{ errors.apiError }}
      </div>
      <div v-else-if="authStore.error && !meta.dirty && meta.touched && !errors.apiError" class="api-error-message form-feedback">
         {{ authStore.error }}
      </div>

      <button type="submit" :disabled="isSubmitting || authStore.loading || !meta.valid && meta.touched" class="btn btn-primary btn-block">
        {{ (isSubmitting || authStore.loading) ? 'Alterando...' : 'Alterar Senha' }}
      </button>
    </Form>
  </div>
</template>

<style scoped>
.change-password-layout {
  max-width: 480px;
  margin: var(--padding-xl) auto;
}
.change-password-layout h2 {
  text-align: center;
  margin-bottom: var(--padding-lg);
}
.btn-block {
  width: 100%;
  margin-top: var(--padding-md);
}
</style>