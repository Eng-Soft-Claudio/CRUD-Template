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
  <div class="admin-create-user-container">
    <header class="page-header">
      <h1>Criar Novo Usuário (Admin)</h1>
      <button @click="goBackToList" class="btn-back btn-secondary">Voltar para Lista</button>
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
        <button type="button" @click="goBackToList" class="btn-secondary">Cancelar</button>
        <button
          type="submit"
          :disabled="isSubmittingForm || (meta.touched && !meta.valid)"
          class="btn-primary"
        >
          {{ isSubmittingForm ? 'Criando...' : 'Criar Usuário' }}
        </button>
      </div>
    </Form>
  </div>
</template>

<style scoped>
/* Estilos podem ser muito similares aos de AdminEditUserView.vue, adapte se necessário */
.admin-create-user-container {
  max-width: 700px;
  margin: 30px auto;
  padding: 25px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.07);
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border-color, #eee);
}
.page-header h1 {
  font-size: 1.6em;
  color: var(--text-color-primary, #2c3e50);
  margin: 0;
}
.btn-back {
  padding: 8px 15px;
  font-size: 0.9em;
}

.create-user-form {
  margin-top: 20px;
}
.form-row {
  display: flex;
  flex-direction: column;
  gap: 0px;
  margin-bottom: 0;
}
.form-group {
  margin-bottom: 22px;
  flex: 1;
}
.form-row .form-group {
  margin-bottom: 22px;
}
.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #34495e;
}
.form-control {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #bdc3c7;
  border-radius: var(--border-radius-md, 6px);
  font-size: 1em;
  transition:
    border-color 0.2s,
    box-shadow 0.2s;
}
.form-control:focus {
  border-color: var(--primary-color, #3498db);
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
  outline: none;
}
.form-control.is-invalid {
  border-color: var(--danger-color, #e74c3c);
}
.invalid-feedback {
  display: block;
  color: var(--danger-color, #e74c3c);
  font-size: 0.875em;
  margin-top: 5px;
}
.form-text {
  font-size: 0.85em;
  color: var(--text-color-secondary, #7f8c8d);
  margin-top: 5px;
  display: block;
}
.form-group-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 10px;
}
.form-group-checkbox label {
  margin-bottom: 0;
  cursor: pointer;
  font-weight: normal;
}
.form-check-input {
  width: auto;
  margin-right: 0;
  height: 1.1em;
  width: 1.1em;
  cursor: pointer;
}
.form-actions {
  margin-top: 30px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
.btn-primary,
.btn-secondary {
  padding: 10px 20px;
  border: none;
  border-radius: var(--border-radius-md, 6px);
  cursor: pointer;
  font-size: 1em;
  font-weight: 500;
}
.btn-primary {
  background-color: var(--primary-color, #3498db);
  color: white;
}
.btn-primary:hover:not(:disabled) {
  background-color: var(--primary-hover-color, #2980b9);
}
.btn-secondary {
  background-color: #bdc3c7;
  color: #2c3e50;
}
.btn-secondary:hover:not(:disabled) {
  background-color: #95a5a6;
}
.btn-primary:disabled,
.btn-secondary:disabled {
  background-color: #e0e0e0;
  cursor: not-allowed;
}
.api-error-message {
  color: var(--danger-color, #c0392b);
  background-color: #fdecea;
  border: 1px solid #f5b0b1;
  padding: 12px;
  border-radius: var(--border-radius-md);
  margin-bottom: 20px;
  text-align: center;
  font-size: 0.95em;
}
@media (min-width: 768px) {
  .form-row {
    flex-direction: row;
    gap: 20px;
  }
}
</style>
