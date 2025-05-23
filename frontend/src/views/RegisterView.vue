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
  <div class="view-card-container register-view-layout">
    <h2>Registrar</h2>
    <Form :validation-schema="validationSchema" :initial-values="initialValues" @submit="handleRegister" v-slot="{ errors, isSubmitting }">
      <div class="form-group">
        <label for="email-register">Email:</label>
        <Field name="email" type="email" id="email-register" class="form-control" :class="{'is-invalid': errors.email }" />
        <ErrorMessage name="email" class="invalid-feedback" />
      </div>

      <div class="form-group">
        <label for="fullName-register">Nome Completo (Opcional):</label>
        <Field name="fullName" type="text" id="fullName-register" class="form-control" :class="{'is-invalid': errors.fullName }" />
        <ErrorMessage name="fullName" class="invalid-feedback" />
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

      <div v-if="errors.apiError" class="api-error-message form-feedback">
        {{ errors.apiError }}
      </div>
      <div v-else-if="authStore.error && !errors.apiError" class="api-error-message form-feedback">
        {{ authStore.error }}
      </div>

      <button type="submit" :disabled="isSubmitting || authStore.loading" class="btn btn-primary btn-block">
        {{ (isSubmitting || authStore.loading) ? 'Registrando...' : 'Registrar' }}
      </button>
    </Form>
    <p class="form-link-center">
      Já tem uma conta? <router-link to="/login">Faça login</router-link>
    </p>
  </div>
</template>

<style scoped>
.register-view-layout {
  max-width: 480px;
  margin: var(--padding-xl) auto;
}
.register-view-layout h2 {
  text-align: center;
  margin-bottom: var(--padding-lg);
  font-size: 2em;
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