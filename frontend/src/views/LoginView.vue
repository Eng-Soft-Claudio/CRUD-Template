<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import { Form, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';

const authStore = useAuthStore();
const router = useRouter();

const validationSchema = yup.object({
  email: yup.string().required('O email é obrigatório').email('Formato de email inválido'),
  password: yup.string().required('A senha é obrigatória'),
});

const initialValues = {
  email: '',
  password: '',
};

const handleLogin = async (values: Record<string, any>, { setErrors }: any) => {
  authStore.setError(null);
  try {
    await authStore.login({ username: values.email, password: values.password });
    if (authStore.isAuthenticated) {
      router.push('/');
    } else if (authStore.error) {
      setErrors({ apiError: authStore.error });
    }
  } catch (error: any) {
    if (authStore.error) {
        setErrors({ apiError: authStore.error });
    } else if (error.message){
        setErrors({ apiError: error.message });
    } else {
        setErrors({ apiError: 'Ocorreu um erro inesperado.' });
    }
    console.error('Falha no login do componente:', error);
  }
};
</script>

<template>
  <div class="login-container">
    <h2>Login</h2>
    <Form :validation-schema="validationSchema" :initial-values="initialValues" @submit="handleLogin" v-slot="{ errors, isSubmitting }">
      <div class="form-group">
        <label for="email-login">Email:</label>
        <Field name="email" type="email" id="email-login" class="form-control" :class="{'is-invalid': errors.email }" />
        <ErrorMessage name="email" class="invalid-feedback" />
      </div>

      <div class="form-group">
        <label for="password-login">Senha:</label>
        <Field name="password" type="password" id="password-login" class="form-control" :class="{'is-invalid': errors.password }" />
        <ErrorMessage name="password" class="invalid-feedback" />
      </div>

      <div v-if="errors.apiError" class="api-error-message">
        {{ errors.apiError }}
      </div>
      <div v-else-if="authStore.error && !errors.apiError" class="api-error-message">
         {{ authStore.error }}
      </div>

      <button type="submit" :disabled="isSubmitting || authStore.loading" class="btn-submit">
        {{ (isSubmitting || authStore.loading) ? 'Entrando...' : 'Entrar' }}
      </button>
    </Form>
    <p class="forgot-password-link">
      <router-link to="/forgot-password">Esqueci minha senha</router-link>
    </p>
    <p class="register-link">
      Não tem uma conta? <router-link to="/register">Registre-se</router-link>
    </p>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 420px;
  margin: 60px auto;
  padding: 35px;
  background-color: #f9fafb;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}
.login-container h2 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 2em;
  color: #1f2937;
  font-weight: 600;
}
.form-group {
  margin-bottom: 22px;
}
.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #374151;
}
.form-control {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1em;
  background-color: #ffffff;
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
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 22px;
  text-align: center;
  font-size: 0.9em;
}
.btn-submit {
  width: 100%;
  background-color: var(--primary-color, #2563eb);
  color: white;
  padding: 14px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.05em;
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
.forgot-password-link,
.register-link {
  text-align: center;
  margin-top: 22px;
  font-size: 0.9em;
}
.forgot-password-link a,
.register-link a {
  color: var(--primary-color, #10b981);
  text-decoration: none;
  font-weight: 500;
}
.forgot-password-link a:hover,
.register-link a:hover {
  text-decoration: underline;
}
</style>