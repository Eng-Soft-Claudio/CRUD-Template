<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import type { UserCreate } from '@/types/user';
import { Form, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';

const authStore = useAuthStore();

const validationSchema = yup.object({
  email: yup.string().required('O email é obrigatório').email('Formato de email inválido'),
  fullName: yup.string().optional(),
  password: yup.string().required('A senha é obrigatória').min(8, 'A senha deve ter pelo menos 8 caracteres'),
  confirmPassword: yup.string()
    .required('A confirmação de senha é obrigatória')
    .oneOf([yup.ref('password')], 'As senhas não coincidem'),
});

const initialValues = {
  email: '',
  fullName: '',
  password: '',
  confirmPassword: '',
};

const handleRegister = async (values: Record<string, any>, { setErrors }: any) => {
  authStore.setError(null);

  const userData: UserCreate = {
    email: values.email,
    password: values.password,
    full_name: values.fullName || null,
  };

  try {
    await authStore.register(userData);
  } catch (error: any) {
    if (error.response && error.response.data && error.response.data.detail) {
      setErrors({ apiError: error.response.data.detail });
    } else {
      setErrors({ apiError: 'Falha ao registrar. Tente novamente.' });
    }
    console.error('Falha no registro do componente:', error);
  }
};
</script>

<template>
  <div class="register-container">
    <h2>Registrar</h2>
    <Form :validation-schema="validationSchema" :initial-values="initialValues" @submit="handleRegister" v-slot="{ errors, isSubmitting }">
      <div class="form-group">
        <label for="email-register">Email:</label>
        <Field name="email" type="email" id="email-register" class="form-control" :class="{'is-invalid': errors.email }" />
        <ErrorMessage name="email" class="invalid-feedback" />
      </div>

      <div class="form-group">
        <label for="fullName-register">Nome Completo (Opcional):</label>
        <Field name="fullName" type="text" id="fullName-register" class="form-control" />
      </div>

      <div class="form-group">
        <label for="password-register">Senha:</label>
        <Field name="password" type="password" id="password-register" class="form-control" :class="{'is-invalid': errors.password }" />
        <ErrorMessage name="password" class="invalid-feedback" />
      </div>

      <div class="form-group">
        <label for="confirmPassword-register">Confirmar Senha:</label>
        <Field name="confirmPassword" type="password" id="confirmPassword-register" class="form-control" :class="{'is-invalid': errors.confirmPassword }" />
        <ErrorMessage name="confirmPassword" class="invalid-feedback" />
      </div>

      <div v-if="errors.apiError" class="api-error-message">
        {{ errors.apiError }}
      </div>
      <div v-else-if="authStore.error" class="api-error-message">
        {{ authStore.error }}
      </div>


      <button type="submit" :disabled="isSubmitting || authStore.loading" class="btn-submit">
        {{ (isSubmitting || authStore.loading) ? 'Registrando...' : 'Registrar' }}
      </button>
    </Form>
    <p class="login-redirect">
      Já tem uma conta? <router-link to="/login">Faça login</router-link>
    </p>
  </div>
</template>

<style scoped>
.register-container {
  max-width: 450px;
  margin: 50px auto;
  padding: 30px;
  background-color: #f9fafb;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
.register-container h2 {
  text-align: center;
  margin-bottom: 25px;
  font-size: 1.8em;
  color: #1f2937;
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
.login-redirect {
  text-align: center;
  margin-top: 25px;
  font-size: 0.9em;
}
.login-redirect a {
  color: var(--primary-color, #10b981);
  text-decoration: none;
  font-weight: 500;
}
.login-redirect a:hover {
  text-decoration: underline;
}
</style>