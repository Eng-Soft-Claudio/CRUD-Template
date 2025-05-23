<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminUsersStore } from '@/stores/adminUsersStore'
import type { UserCreate } from '@/types/user'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'

const router = useRouter()
const adminUsersStore = useAdminUsersStore()

const isSubmittingForm = computed(() => adminUsersStore.isLoading) // Usar o isLoading geral

const validationSchema = yup.object({
  email: yup.string().required('O email é obrigatório').email('Formato de email inválido'),
  full_name: yup.string().nullable(),
  password: yup
    .string()
    .required('A senha é obrigatória')
    .min(8, 'A senha deve ter pelo menos 8 caracteres'),
  confirmPassword: yup
    .string()
    .required('A confirmação de senha é obrigatória')
    .oneOf([yup.ref('password')], 'As senhas não coincidem'),
  is_active: yup.boolean(),
  is_superuser: yup.boolean(),
})

const initialValues = {
  email: '',
  full_name: '',
  password: '',
  confirmPassword: '',
  is_active: true,
  is_superuser: false,
}

const handleCreateUserByAdmin = async (
  values: Record<string, any>,
  { setErrors, resetForm }: any,
) => {
  adminUsersStore._setError(null)

  const createData: UserCreate = {
    email: values.email,
    password: values.password,
    full_name: values.full_name === '' ? null : values.full_name,
    is_active: values.is_active,
    is_superuser: values.is_superuser,
  }

  try {
    await adminUsersStore.createUserByAdmin(createData)
    resetForm()
    router.push({ name: 'admin-users' })
  } catch (err: any) {
    const errorMessage = adminUsersStore.usersError || 'Falha ao criar usuário.'
    setErrors({ apiError: errorMessage })
    console.error('Erro ao criar usuário (admin) no componente:', err)
  }
}

const goBackToList = () => {
  adminUsersStore._setError(null)
  router.push({ name: 'admin-users' })
}
</script>

<template>
  <div class="view-card-container admin-create-user-layout">
    <header class="page-header-alt">
      <h1>Criar Novo Usuário <span class="admin-tag">(Admin)</span></h1>
      <button @click="goBackToList" class="btn btn-secondary btn-small">Voltar para Lista</button>
    </header>

    <Form
      :validation-schema="validationSchema"
      :initial-values="initialValues"
      @submit="handleCreateUserByAdmin"
      v-slot="{ errors, isSubmitting, meta }"
      class="create-user-form"
    >
      <div class="form-row">
        <div class="form-group">
          <label for="email-admin-create">Email:</label>
          <Field
            name="email"
            type="email"
            id="email-admin-create"
            class="form-control"
            :class="{ 'is-invalid': errors.email }"
          />
          <ErrorMessage name="email" class="invalid-feedback" />
        </div>
        <div class="form-group">
          <label for="fullName-admin-create">Nome Completo:</label>
          <Field
            name="full_name"
            type="text"
            id="fullName-admin-create"
            class="form-control"
            :class="{ 'is-invalid': errors.full_name }"
          />
          <ErrorMessage name="full_name" class="invalid-feedback" />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="password-admin-create">Senha:</label>
          <Field
            name="password"
            type="password"
            id="password-admin-create"
            class="form-control"
            :class="{ 'is-invalid': errors.password }"
          />
          <ErrorMessage name="password" class="invalid-feedback" />
        </div>
        <div class="form-group">
          <label for="confirmPassword-admin-create">Confirmar Senha:</label>
          <Field
            name="confirmPassword"
            type="password"
            id="confirmPassword-admin-create"
            class="form-control"
            :class="{ 'is-invalid': errors.confirmPassword }"
          />
          <ErrorMessage name="confirmPassword" class="invalid-feedback" />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group form-group-checkbox">
          <Field
            name="is_active"
            type="checkbox"
            id="isActive-admin-create"
            class="form-check-input"
            :value="true"
            checked
          />
          <label for="isActive-admin-create" class="form-check-label">Usuário Ativo</label>
        </div>
        <div class="form-group form-group-checkbox">
          <Field
            name="is_superuser"
            type="checkbox"
            id="isSuperuser-admin-create"
            class="form-check-input"
            :value="true"
          />
          <label for="isSuperuser-admin-create" class="form-check-label">É Superusuário</label>
        </div>
      </div>

      <div v-if="errors.apiError" class="api-error-message form-feedback">
        {{ errors.apiError }}
      </div>
      <div
        v-else-if="adminUsersStore.usersError && !errors.apiError"
        class="api-error-message form-feedback"
      >
        {{ adminUsersStore.usersError }}
      </div>

      <div class="form-actions">
        <button type="button" @click="goBackToList" class="btn btn-secondary">Cancelar</button>
        <button
          type="submit"
          :disabled="isSubmittingForm || (meta.touched && !meta.valid)"
          class="btn btn-primary"
        >
          {{ isSubmittingForm ? 'Criando...' : 'Criar Usuário' }}
        </button>
      </div>
    </Form>
  </div>
</template>

<style scoped>
/* Estilos muito similares a AdminEditUserView.vue */
.admin-create-user-layout {
  max-width: 700px;
  margin: var(--padding-xl) auto;
}
.page-header-alt {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--padding-lg);
  padding-bottom: var(--padding-md);
  border-bottom: 1px solid var(--color-border);
}
.page-header-alt h1 {
  font-size: 1.6em;
  color: var(--text-color-primary);
  margin: 0;
}
.admin-tag {
  font-size: 0.8em;
  color: var(--color-text-on-light-secondary);
  font-weight: normal;
}
.btn-back {
  /* btn, btn-secondary, btn-small virão do global */
}
.create-user-form {
  margin-top: var(--padding-md);
}
.form-row {
  display: flex;
  flex-direction: column;
  gap: 0;
  margin-bottom: 0;
}
.form-group {
  margin-bottom: var(--padding-lg);
  flex: 1;
}
.form-row .form-group {
  margin-bottom: var(--padding-lg); /* Para quando estiverem em linha */
}
.form-group-checkbox {
  align-items: center; /* herdado de .form-group */
}
.form-actions {
  margin-top: var(--padding-lg);
  display: flex;
  justify-content: flex-end;
  gap: var(--padding-md);
}
@media (min-width: 768px) {
  .form-row {
    flex-direction: row;
    gap: var(--padding-lg);
  }
}
</style>
