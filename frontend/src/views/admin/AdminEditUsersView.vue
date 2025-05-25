<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAdminUsersStore } from '@/stores/adminUsersStore'
import type { UserUpdate, UserRead } from '@/types/user'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'

const route = useRoute()
const router = useRouter()
const adminUsersStore = useAdminUsersStore()

const userId = computed(() => Number(route.params.id))
const userForEdit = computed(() => adminUsersStore.userForEdit)
const isLoadingData = computed(() => adminUsersStore.isLoadingUserForEdit)
const isSubmittingForm = computed(() => adminUsersStore.isLoading)
const errorLoadingUser = computed(() => adminUsersStore.userForEditError)

const validationSchema = yup.object({
  email: yup.string().required('O email é obrigatório').email('Formato de email inválido'),
  full_name: yup.string().nullable(),
  is_active: yup.boolean(),
  is_superuser: yup.boolean(),
  password: yup
    .string()
    .optional()
    .test(
      'min-length-if-provided',
      'A nova senha deve ter pelo menos 8 caracteres (se fornecida)',
      (value) => !value || value.length === 0 || value.length >= 8,
    ),
})

interface EditFormShape {
  email: string
  full_name: string | null
  is_active: boolean
  is_superuser: boolean
  password?: string
}

const formValues = ref<EditFormShape>({
  email: '',
  full_name: null,
  is_active: true,
  is_superuser: false,
  password: '',
})

watch(
  userForEdit,
  (currentUser: UserRead | null) => {
    if (currentUser) {
      formValues.value = {
        email: currentUser.email,
        full_name: currentUser.full_name || null,
        is_active: currentUser.is_active,
        is_superuser: currentUser.is_superuser,
        password: '',
      }
    } else {
      formValues.value = {
        email: '',
        full_name: null,
        is_active: true,
        is_superuser: false,
        password: '',
      }
    }
  },
  { immediate: true },
)

onMounted(async () => {
  adminUsersStore._setError(null)
  adminUsersStore._setSingleUserError(null)
  if (userId.value && !isNaN(userId.value)) {
    await adminUsersStore.fetchUserById(userId.value)
  } else {
    adminUsersStore._setSingleUserError('ID de usuário inválido na rota.')
    router.push({ name: 'admin-users' })
  }
})

const handleUpdateUserByAdmin = async (values: Record<string, any>, { setErrors }: any) => {
  adminUsersStore._setError(null)

  if (!userForEdit.value || !userId.value || isNaN(userId.value)) {
    setErrors({ apiError: 'Não há dados do usuário ou ID inválido para atualizar.' })
    return
  }

  const updatePayload: UserUpdate = {}
  let hasChanges = false

  const originalUser = userForEdit.value

  if (values.email !== undefined && values.email !== originalUser.email) {
    updatePayload.email = values.email as string
    hasChanges = true
  }

  const currentFullName = originalUser.full_name || null
  const formFullName = values.full_name === '' ? null : (values.full_name as string | null)
  if (values.full_name !== undefined && formFullName !== currentFullName) {
    updatePayload.full_name = formFullName
    hasChanges = true
  }

  if (typeof values.is_active === 'boolean' && values.is_active !== originalUser.is_active) {
    updatePayload.is_active = values.is_active
    hasChanges = true
  }
  console.log(
    'VALOR DE values.is_superuser ANTES DA CONDIÇÃO:',
    values.is_superuser,
    'TIPO:',
    typeof values.is_superuser,
  )
  console.log('VALOR DE userForEdit.value.is_superuser:', userForEdit.value.is_superuser)
  if (
    typeof values.is_superuser === 'boolean' &&
    values.is_superuser !== originalUser.is_superuser
  ) {
    updatePayload.is_superuser = values.is_superuser
    hasChanges = true
  }

  if (values.password && (values.password as string).trim() !== '') {
    updatePayload.password = values.password as string
    hasChanges = true
  }

  if (!hasChanges) {
    setErrors({ apiError: 'Nenhuma alteração para salvar.' })
    return
  }

  try {
    await adminUsersStore.updateUserByAdmin(userId.value, updatePayload)
    router.push({ name: 'admin-users' })
  } catch (err: any) {
    const errorMessageFromStore = adminUsersStore.usersError || adminUsersStore.userForEditError
    setErrors({ apiError: errorMessageFromStore || 'Falha ao atualizar usuário.' })
    console.error('Erro ao atualizar usuário (admin) no componente:', err)
  }
}

const goBackToList = () => {
  adminUsersStore._setCurrentUserForEdit(null)
  adminUsersStore._setSingleUserError(null)
  adminUsersStore._setError(null)
  router.push({ name: 'admin-users' })
}
</script>

<template>
  <div class="view-card-container admin-edit-user-layout">
    <header class="page-header-alt">
      <h1>
        {{ userForEdit ? `Editar Usuário: ${userForEdit.email}` : 'Editar Usuário' }}
        <span class="admin-tag">(Admin)</span>
      </h1>
      <button @click="goBackToList" class="btn btn-secondary btn-small">Voltar para Lista</button>
    </header>

    <div v-if="isLoadingData" class="loading-indicator form-feedback">
      <p>Carregando dados do usuário...</p>
    </div>
    <div v-else-if="errorLoadingUser && !userForEdit" class="api-error-message form-feedback">
      <p>{{ errorLoadingUser }}</p>
    </div>
    <div v-else-if="!userForEdit && !isLoadingData" class="api-error-message form-feedback">
      <p>Usuário não encontrado ou ID inválido.</p>
    </div>

    <Form
      v-if="userForEdit && !isLoadingData"
      :validation-schema="validationSchema"
      v-model:values="formValues"
      @submit="handleUpdateUserByAdmin"
      v-slot="{ errors, isSubmitting, meta }"
      enable-reinitialize
      class="edit-user-form"
    >
      <div class="form-row">
        <div class="form-group">
          <label for="email-admin-edit">Email:</label>
          <Field
            name="email"
            type="email"
            id="email-admin-edit"
            class="form-control"
            :class="{ 'is-invalid': errors.email }"
          />
          <ErrorMessage name="email" class="invalid-feedback" />
        </div>
        <div class="form-group">
          <label for="fullName-admin-edit">Nome Completo:</label>
          <Field
            name="full_name"
            type="text"
            id="fullName-admin-edit"
            class="form-control"
            :class="{ 'is-invalid': errors.full_name }"
          />
          <ErrorMessage name="full_name" class="invalid-feedback" />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group form-group-checkbox">
          <Field
            name="is_active"
            type="checkbox"
            id="isActive-admin-edit"
            class="form-check-input"
            v-model="formValues.is_active"
            :value="true"
            :unchecked-value="false"
          />
          <label for="isActive-admin-edit" class="form-check-label">Usuário Ativo</label>
        </div>
        <div class="form-group form-group-checkbox">
          <Field
            name="is_superuser"
            type="checkbox"
            id="isSuperuser-admin-edit"
            class="form-check-input"
            v-model="formValues.is_superuser"
            :value="true"
            :unchecked-value="false"
          />
          <label for="isSuperuser-admin-edit" class="form-check-label">É Superusuário</label>
        </div>
      </div>

      <div class="form-group">
        <label for="password-admin-edit">Nova Senha (opcional):</label>
        <Field
          name="password"
          type="password"
          id="password-admin-edit"
          class="form-control"
          :class="{ 'is-invalid': errors.password }"
          placeholder="Deixe em branco para não alterar"
        />
        <ErrorMessage name="password" class="invalid-feedback" />
        <small class="form-text">Preencha apenas se desejar alterar a senha deste usuário.</small>
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
        <button type="submit" :disabled="isSubmittingForm || !meta.dirty" class="btn btn-primary">
          {{ isSubmittingForm ? 'Salvando...' : 'Salvar Alterações' }}
        </button>
      </div>
    </Form>
  </div>
</template>

<style scoped>
.admin-edit-user-layout {
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
  color: var(--color-text-on-light-primary);
  margin: 0;
}
.admin-tag {
  font-size: 0.8em;
  color: var(--color-text-on-light-secondary);
  font-weight: normal;
}
.form-row {
  display: flex;
  flex-direction: column;
  gap: 0; /* Ajustado, o gap pode vir de .form-group se forem lado a lado */
  margin-bottom: 0; /* Ajustado */
}
@media (min-width: 768px) {
  .form-row {
    flex-direction: row;
    gap: var(--padding-lg);
  }
  .form-row .form-group {
    margin-bottom: var(--padding-lg); /* Para quando estão em linha */
  }
}
.form-group-checkbox {
  align-items: center; /* Já estava bom */
}
.form-actions {
  margin-top: var(--padding-lg);
  display: flex;
  justify-content: flex-end;
  gap: var(--padding-md);
}
</style>
