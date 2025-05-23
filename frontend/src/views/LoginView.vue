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
  <div class="view-card-container login-view-layout">
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

      <div v-if="errors.apiError" class="api-error-message form-feedback">
        {{ errors.apiError }}
      </div>
      <div v-else-if="authStore.error && !errors.apiError" class="api-error-message form-feedback">
         {{ authStore.error }}
      </div>

      <button type="submit" :disabled="isSubmitting || authStore.loading" class="btn btn-primary btn-block">
        {{ (isSubmitting || authStore.loading) ? 'Entrando...' : 'Entrar' }}
      </button>
    </Form>
    <p class="form-link-center">
      <router-link to="/forgot-password">Esqueci minha senha</router-link>
    </p>
    <p class="form-link-center">
      Não tem uma conta? <router-link to="/register">Registre-se</router-link>
    </p>
  </div>
</template>

<style scoped>
.login-view-layout {
  max-width: 420px; /* Largura específica para este formulário */
  margin: var(--padding-xl) auto; /* Margem e centralização */
}
.login-view-layout h2 {
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