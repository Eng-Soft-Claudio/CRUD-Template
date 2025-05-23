<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import type { UserUpdate, UserRead } from '@/types/user'
import { useRouter } from 'vue-router'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'

const authStore = useAuthStore()
const router = useRouter()

const currentUser = computed(() => authStore.currentUser)

const editMode = ref(false)
const successMessage = ref<string | null>(null)
const generalError = ref<string | null>(null);

const showDeleteConfirmModal = ref(false)

const validationSchema = yup.object({
  fullName: yup.string().nullable(),
  email: yup.string().required('O email é obrigatório').email('Formato de email inválido'),
})

const formValues = ref({
  fullName: '',
  email: '',
})

const populateForm = () => {
  if (currentUser.value) {
    formValues.value.fullName = currentUser.value.full_name || ''
    formValues.value.email = currentUser.value.email || ''
  }
}

onMounted(() => {
  populateForm()
})

watch(
  currentUser,
  (newUserValue: UserRead | null) => {
    if (newUserValue && !editMode.value) {
      populateForm()
    }
  },
  { immediate: true, deep: true },
)

const toggleEditMode = () => {
  editMode.value = !editMode.value
  authStore.setError(null)
  successMessage.value = null
  generalError.value = null;
  if (editMode.value) {
    populateForm()
  }
}

const handleUpdateProfile = async (values: Record<string, any>, { setErrors }: any) => {
  authStore.setError(null)
  successMessage.value = null

  if (!currentUser.value) {
    setErrors({ apiError: 'Usuário não encontrado.' })
    return
  }

  const updateData: UserUpdate = {}
  let hasChanges = false

  const currentFullName = currentUser.value.full_name || ''
  const currentEmail = currentUser.value.email

  if (values.fullName !== currentFullName) {
    updateData.full_name = values.fullName.trim() === '' ? null : values.fullName.trim()
    hasChanges = true
  }
  if (values.email !== currentEmail) {
    updateData.email = values.email
    hasChanges = true
  }

  if (!hasChanges) {
    setErrors({ apiError: 'Nenhuma alteração detectada.' })
    return
  }

  try {
    await authStore.updateUserProfile(updateData)
    successMessage.value = 'Perfil atualizado com sucesso!'
    editMode.value = false
  } catch (error: any) {
    if (authStore.error) {
      setErrors({ apiError: authStore.error })
    } else if (error.response?.data?.detail) {
      const detail = error.response.data.detail
      if (typeof detail === 'string') {
        setErrors({ apiError: detail })
      } else if (Array.isArray(detail) && detail[0]?.msg) {
        setErrors({ apiError: detail[0].msg })
      } else {
        setErrors({ apiError: 'Falha ao atualizar o perfil.' })
      }
    } else {
      setErrors({ apiError: 'Ocorreu um erro desconhecido ao atualizar o perfil.' })
    }
    console.error('Falha ao atualizar perfil no componente:', error)
  }
}

const handleDeleteAccount = async () => {
  if (
    window.confirm('TEM CERTEZA ABSOLUTA que deseja deletar sua conta? Esta ação é irreversível.')
  ) {
    if (window.confirm('SEGUNDA CONFIRMAÇÃO: Deletar conta permanentemente?')) {
      authStore.setError(null)
      successMessage.value = null
      generalError.value = null;
      try {
        await authStore.deleteUserAccount()
      } catch (error) {
        console.error('Falha ao deletar conta no componente:', error)
      }
    }
  }
}

const navigateToChangePassword = () => {
  router.push({ name: 'change-password' })
}
</script>

<template>
  <div class="view-card-container profile-view-layout" v-if="currentUser">
    <h1>Meu Perfil</h1>

    <div v-if="successMessage" class="success-message form-feedback">
      {{ successMessage }}
    </div>
    <div v-if="generalError && !authStore.error" class="error-message form-feedback">
      {{ generalError }}
    </div>
    <div v-if="authStore.error" class="api-error-message form-feedback">
      {{ authStore.error }}
    </div>

    <div v-if="!editMode" class="profile-display">
      <div class="profile-field">
        <span class="profile-field-label">Nome Completo:</span>
        <span class="profile-field-value">{{ currentUser.full_name || 'Não informado' }}</span>
      </div>
      <div class="profile-field">
        <span class="profile-field-label">Email:</span>
        <span class="profile-field-value">{{ currentUser.email }}</span>
      </div>
      <div class="profile-field">
        <span class="profile-field-label">Status:</span>
        <span
          class="profile-field-value"
          :class="currentUser.is_active ? 'status-active' : 'status-inactive'"
        >
          {{ currentUser.is_active ? 'Ativo' : 'Inativo' }}
        </span>
      </div>
      <div class="profile-field" v-if="currentUser.is_superuser">
        <span class="profile-field-label">Nível de Acesso:</span>
        <span class="profile-field-value status-admin">Administrador</span>
      </div>

      <div class="actions-group">
        <button @click="toggleEditMode" class="btn btn-accent">Editar Perfil</button>
        <button @click="navigateToChangePassword" class="btn btn-secondary">Alterar Senha</button>
      </div>
    </div>

    <Form
      v-if="editMode"
      :validation-schema="validationSchema"
      :initial-values="formValues"
      @submit="handleUpdateProfile"
      v-slot="{ errors, isSubmitting, meta }"
      class="profile-edit-form"
    >
      <h3>Editar Informações</h3>
      <div class="form-group">
        <label for="fullName-profile">Nome Completo:</label>
        <Field name="fullName" type="text" id="fullName-profile" class="form-control" />
        <ErrorMessage name="fullName" class="invalid-feedback" />
      </div>
      <div class="form-group">
        <label for="email-profile">Email:</label>
        <Field
          name="email"
          type="email"
          id="email-profile"
          class="form-control"
          :class="{ 'is-invalid': errors.email }"
          required
        />
        <ErrorMessage name="email" class="invalid-feedback" />
      </div>

      <div v-if="errors.apiError" class="api-error-message form-feedback">
        {{ errors.apiError }}
      </div>

      <div class="form-actions">
        <button type="button" @click="toggleEditMode" class="btn btn-secondary">Cancelar</button>
        <button
          type="submit"
          :disabled="isSubmitting || authStore.loading || !meta.dirty"
          class="btn btn-primary"
        >
          {{ isSubmitting || authStore.loading ? 'Salvando...' : 'Salvar Alterações' }}
        </button>
      </div>
    </Form>

    <hr class="divider" />

    <div class="danger-zone">
      <h3>Zona de Perigo</h3>
      <p>Deletar sua conta é uma ação permanente e não pode ser desfeita.</p>
      <button
        @click="handleDeleteAccount"
        class="btn btn-danger"
        :disabled="authStore.loading && editMode"
      >
        {{ authStore.loading && editMode ? 'Aguarde...' : 'Deletar Minha Conta' }}
      </button>
    </div>
  </div>
  <div v-else class="view-card-container loading-profile">
    <p>Carregando informações do perfil ou usuário não autenticado...</p>
  </div>
</template>

<style scoped>
.profile-view-layout {
  max-width: 700px;
  margin: var(--padding-xl) auto;
}
.profile-view-layout h1 {
  text-align: center;
  margin-bottom: var(--padding-xl);
  font-size: 2em;
}
.profile-view-layout h3 {
  font-size: 1.5em;
  font-family: var(--font-sans-ui);
  font-weight: 600;
  color: var(--text-color-primary);
  margin-top: var(--padding-lg);
  margin-bottom: var(--padding-md);
  text-align: left;
  padding-bottom: var(--padding-sm);
  border-bottom: 1px solid var(--color-border);
}
.profile-display {
  margin-bottom: var(--padding-xl);
}
.profile-field {
  display: flex;
  justify-content: space-between;
  padding: var(--padding-sm) 0;
  border-bottom: 1px dotted var(--color-border-subtle, #e0e0e0);
}
.profile-field:last-child {
  border-bottom: none;
}
.profile-field-label {
  font-weight: 600;
  font-family: var(--font-sans-ui);
  color: var(--color-text-on-light-secondary);
}
.profile-field-value {
  color: var(--text-color-primary);
}
.status-active {
  color: var(--color-success);
  font-weight: 600;
}
.status-inactive {
  color: var(--color-danger);
  font-weight: 600;
}
.status-admin {
  color: var(--color-accent-gold);
  font-weight: 600;
}

.actions-group {
  margin-top: var(--padding-lg);
  display: flex;
  gap: var(--padding-md);
  justify-content: flex-start;
}
.profile-edit-form {
  margin-top: var(--padding-lg);
}
.form-actions {
  margin-top: var(--padding-lg);
  display: flex;
  justify-content: flex-end;
  gap: var(--padding-md);
}
.divider {
  margin-top: var(--padding-xl);
  margin-bottom: var(--padding-xl);
}
.danger-zone {
  padding: var(--padding-lg);
  border: 1px solid var(--color-danger);
  border-radius: var(--border-radius-lg);
  background-color: #fff5f5;
  margin-top: var(--padding-lg);
}
.danger-zone h3 {
  color: var(--color-danger);
  margin-top: 0;
  font-size: 1.3em;
  border-bottom: none;
  text-align: left;
}
.danger-zone p {
  color: var(--color-danger);
  font-size: 0.95em;
  margin-bottom: var(--padding-md);
}
.danger-zone .btn-danger {
  margin-top: var(--padding-sm);
}
.loading-profile p {
  text-align: center;
  padding: var(--padding-xl);
  font-size: 1.1em;
  color: var(--text-color-secondary);
}
.form-feedback {
  /* Para ser usado por api-error-message e success-message */
  margin-bottom: var(--padding-lg);
}
</style>
