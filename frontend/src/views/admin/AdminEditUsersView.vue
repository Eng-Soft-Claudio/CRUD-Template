<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAdminUsersStore } from '@/stores/adminUsersStore';
import type { UserUpdate, UserRead } from '@/types/user';
import { Form, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';

const route = useRoute();
const router = useRouter();
const adminUsersStore = useAdminUsersStore();

const userId = computed(() => Number(route.params.id));
const userForEdit = computed(() => adminUsersStore.userForEdit);
const isLoadingData = computed(() => adminUsersStore.isLoadingUserForEdit);
const isSubmittingForm = computed(() => adminUsersStore.isLoading);
const errorLoadingUser = computed(() => adminUsersStore.userForEditError);

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
        (value) => !value || value.length === 0 || value.length >= 8
    ),
});

interface EditFormShape {
  email: string;
  full_name: string | null;
  is_active: boolean;
  is_superuser: boolean;
  password?: string;
}

const formValues = ref<EditFormShape>({
  email: '',
  full_name: null,
  is_active: true,
  is_superuser: false,
  password: '',
});

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
      };
    } else {
      formValues.value = {
        email: '',
        full_name: null,
        is_active: true,
        is_superuser: false,
        password: '',
      };
    }
  },
  { immediate: true },
);

onMounted(async () => {
  adminUsersStore._setError(null);
  adminUsersStore._setSingleUserError(null);
  if (userId.value && !isNaN(userId.value)) {
    await adminUsersStore.fetchUserById(userId.value);
  } else {
    adminUsersStore._setSingleUserError('ID de usuário inválido na rota.');
    router.push({ name: 'admin-users' });
  }
});

const handleUpdateUserByAdmin = async (values: Record<string, any>, { setErrors }: any) => {
  adminUsersStore._setError(null);

  if (!userForEdit.value || !userId.value || isNaN(userId.value)) {
    setErrors({ apiError: 'Não há dados do usuário ou ID inválido para atualizar.' });
    return;
  }

  const updatePayload: UserUpdate = {};
  let hasChanges = false;

  const originalUser = userForEdit.value;

  if (values.email !== undefined && values.email !== originalUser.email) {
    updatePayload.email = values.email as string;
    hasChanges = true;
  }

  const currentFullName = originalUser.full_name || null;
  const formFullName = values.full_name === '' ? null : values.full_name as (string | null);
  if (values.full_name !== undefined && formFullName !== currentFullName) {
    updatePayload.full_name = formFullName;
    hasChanges = true;
  }

  if (typeof values.is_active === 'boolean' && values.is_active !== originalUser.is_active) {
    updatePayload.is_active = values.is_active;
    hasChanges = true;
  }
  if (typeof values.is_superuser === 'boolean' && values.is_superuser !== originalUser.is_superuser) {
    updatePayload.is_superuser = values.is_superuser;
    hasChanges = true;
  }

  if (values.password && (values.password as string).trim() !== '') {
    updatePayload.password = values.password as string;
    hasChanges = true;
  }

  if (!hasChanges) {
     setErrors({ apiError: 'Nenhuma alteração para salvar.' });
     return;
   }

  try {
    await adminUsersStore.updateUserByAdmin(userId.value, updatePayload);
    router.push({ name: 'admin-users' });
  } catch (err: any) {
    const errorMessageFromStore = adminUsersStore.usersError || adminUsersStore.userForEditError;
    setErrors({ apiError: errorMessageFromStore || 'Falha ao atualizar usuário.' });
    console.error('Erro ao atualizar usuário (admin) no componente:', err);
  }
};

const goBackToList = () => {
  adminUsersStore._setCurrentUserForEdit(null);
  adminUsersStore._setSingleUserError(null);
  adminUsersStore._setError(null);
  router.push({ name: 'admin-users' });
};
</script>

<template>
  <div class="admin-edit-user-container">
    <header class="page-header">
      <h1>{{ userForEdit ? `Editar Usuário: ${userForEdit.email}` : 'Editar Usuário' }} (Admin)</h1>
      <button @click="goBackToList" class="btn-back btn-secondary">Voltar para Lista</button>
    </header>

    <div v-if="isLoadingData" class="loading-indicator">
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
            v-model="formValues.email"
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
            v-model="formValues.full_name"
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
          />
          <label for="isActive-admin-edit" class="form-check-label">Usuário Ativo</label>
          <ErrorMessage name="is_active" class="invalid-feedback" />
        </div>

        <div class="form-group form-group-checkbox">
          <Field
            name="is_superuser"
            type="checkbox"
            id="isSuperuser-admin-edit"
            class="form-check-input"
            v-model="formValues.is_superuser"
            :value="true"
          />
          <label for="isSuperuser-admin-edit" class="form-check-label">É Superusuário</label>
          <ErrorMessage name="is_superuser" class="invalid-feedback" />
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
          v-model="formValues.password"
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
        <button type="button" @click="goBackToList" class="btn-secondary">Cancelar</button>
        <button
          type="submit"
          :disabled="isSubmittingForm || !meta.dirty"
          class="btn-primary"
        >
          {{ isSubmittingForm ? 'Salvando...' : 'Salvar Alterações' }}
        </button>
      </div>
    </Form>
  </div>
</template>

<style scoped>
.admin-edit-user-container { max-width: 700px; margin: 30px auto; padding: 25px; background-color: #fff; border-radius: 8px; box-shadow: 0 3px 10px rgba(0,0,0,0.07); }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; padding-bottom: 15px; border-bottom: 1px solid var(--border-color, #eee); }
.page-header h1 { font-size: 1.6em; color: var(--text-color-primary, #2c3e50); margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: calc(100% - 120px);}
.btn-back { padding: 8px 15px; font-size: 0.9em; white-space: nowrap; }
.edit-user-form { margin-top: 20px; }
.form-row { display: flex; flex-direction: column; gap: 0px; margin-bottom: 0; }
.form-group { margin-bottom: 22px; flex: 1; }
.form-row .form-group { margin-bottom: 22px; }
.form-group label { display: block; margin-bottom: 8px; font-weight: 500; color: #34495e; }
.form-control { width: 100%; padding: 10px 12px; border: 1px solid #bdc3c7; border-radius: var(--border-radius-md, 6px); font-size: 1em; transition: border-color 0.2s, box-shadow 0.2s; }
.form-control:focus { border-color: var(--primary-color, #3498db); box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2); outline: none; }
.form-control.is-invalid { border-color: var(--danger-color, #e74c3c); }
.invalid-feedback { display: block; color: var(--danger-color, #e74c3c); font-size: 0.875em; margin-top: 5px; }
.form-text { font-size: 0.85em; color: var(--text-color-secondary, #7f8c8d); margin-top: 5px; display: block; }
.form-group-checkbox { display: flex; align-items: center; gap: 8px; margin-top: 10px; }
.form-group-checkbox label { margin-bottom: 0; cursor: pointer; font-weight: normal; }
.form-check-input { width: auto; margin-right: 0; height: 1.1em; width: 1.1em; cursor: pointer; }
.form-actions { margin-top: 30px; display: flex; justify-content: flex-end; gap: 12px; }
.btn-primary, .btn-secondary { padding: 10px 20px; border: none; border-radius: var(--border-radius-md, 6px); cursor: pointer; font-size: 1em; font-weight: 500; }
.btn-primary { background-color: var(--primary-color, #3498db); color: white; }
.btn-primary:hover:not(:disabled) { background-color: var(--primary-hover-color, #2980b9); }
.btn-secondary { background-color: #bdc3c7; color: #2c3e50; }
.btn-secondary:hover:not(:disabled) { background-color: #95a5a6; }
.btn-primary:disabled, .btn-secondary:disabled { background-color: #e0e0e0; cursor: not-allowed; }
.loading-indicator, .error-message-box { text-align: center; padding: 20px; font-size: 1.1em; }
.form-feedback { padding: 12px; margin-bottom:20px; border-radius:var(--border-radius-md); font-size:0.95em; text-align:center; border-width: 1px; border-style: solid; }
.api-error-message { color: var(--danger-color, #c0392b); background-color: #fdecea; border-color: #f5b0b1; }
@media (min-width: 768px) {
  .form-row { flex-direction: row; gap: 20px; }
  .page-header h1 { max-width: calc(100% - 150px); }
}
</style>