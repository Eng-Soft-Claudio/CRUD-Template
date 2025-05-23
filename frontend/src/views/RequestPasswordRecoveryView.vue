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
  <div class="view-card-container request-recovery-layout">
    <h2>Esqueci Minha Senha</h2>
    <p class="form-description">
      Insira seu endereço de email. Se uma conta estiver associada, instruções para redefinir
      sua senha serão enviadas (em desenvolvimento, o token aparecerá nos logs do backend).
    </p>
    <Form :validation-schema="validationSchema" :initial-values="initialValues" @submit="handleRequestRecovery" v-slot="{ errors, isSubmitting, meta }">
      <div class="form-group">
        <label for="email-recovery">Email:</label>
        <Field name="email" type="email" id="email-recovery" class="form-control" :class="{'is-invalid': errors.email }" placeholder="seuemail@exemplo.com" />
        <ErrorMessage name="email" class="invalid-feedback" />
      </div>

      <div v-if="successInfoMessage && !errors.apiError" class="info-message form-feedback">
        {{ successInfoMessage }}
      </div>
      <div v-if="errors.apiError" class="api-error-message form-feedback">
        {{ errors.apiError }}
      </div>
      <div v-else-if="authStore.error && !meta.dirty && meta.touched && !errors.apiError" class="api-error-message form-feedback">
        {{ authStore.error }}
      </div>

      <button type="submit" :disabled="isSubmitting || authStore.loading || !meta.valid && meta.touched" class="btn btn-primary btn-block">
        {{ (isSubmitting || authStore.loading) ? 'Enviando...' : 'Solicitar Recuperação' }}
      </button>
    </Form>
    <hr class="divider"/>
    <p class="form-link-center">
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
.request-recovery-layout {
  max-width: 500px;
  margin: var(--padding-xl) auto;
}
.request-recovery-layout h2 {
  text-align: center;
  margin-bottom: var(--padding-md);
  font-size: 1.8em;
}
.form-description {
  text-align: center;
  margin-bottom: var(--padding-lg);
  font-size: 0.95rem;
  color: var(--color-text-on-light-secondary);
  font-family: var(--font-sans-ui);
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
.dev-instructions {
  margin-top: var(--padding-lg);
  padding: var(--padding-md);
  background-color: #fffbeb;
  border: 1px solid #fef3c7;
  color: #78350f;
  border-radius: var(--border-radius-md);
  font-size: 0.85em;
  text-align: left;
  font-family: var(--font-sans-ui);
}
.dev-instructions strong {
  font-weight: 600;
}
</style>