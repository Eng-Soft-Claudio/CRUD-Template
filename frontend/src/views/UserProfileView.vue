<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useAuthStore } from '@/stores/auth';
import type { UserUpdate } from '@/types/user';
import { useRouter } from 'vue-router';
import { Form, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';

const authStore = useAuthStore();
const router = useRouter();

const currentUser = computed(() => authStore.currentUser);

const editMode = ref(false);
const successMessage = ref<string | null>(null);

const showDeleteConfirmModal = ref(false);

const validationSchema = yup.object({
  fullName: yup.string().nullable(),
  email: yup.string().required('O email é obrigatório').email('Formato de email inválido'),
});

const formValues = ref({
  fullName: '',
  email: '',
});

const populateForm = () => {
  if (currentUser.value) {
    formValues.value.fullName = currentUser.value.full_name || '';
    formValues.value.email = currentUser.value.email || '';
  }
};

onMounted(() => {
  populateForm();
});

watch(currentUser, (newUser) => {
  if (newUser && !editMode.value) {
    populateForm();
  }
}, { immediate: true, deep: true });


const toggleEditMode = () => {
  editMode.value = !editMode.value;
  authStore.setError(null);
  successMessage.value = null;
  if (editMode.value) {
    populateForm();
  }
};

const handleUpdateProfile = async (values: Record<string, any>, { setErrors }: any) => {
  authStore.setError(null);
  successMessage.value = null;

  if (!currentUser.value) {
    setErrors({ apiError: "Usuário não encontrado." });
    return;
  }

  const updateData: UserUpdate = {};
  let hasChanges = false;

  const currentFullName = currentUser.value.full_name || '';
  const currentEmail = currentUser.value.email;

  if (values.fullName !== currentFullName) {
    updateData.full_name = values.fullName.trim() === '' ? null : values.fullName.trim();
    hasChanges = true;
  }
  if (values.email !== currentEmail) {
    updateData.email = values.email;
    hasChanges = true;
  }

  if (!hasChanges) {
    setErrors({ apiError: "Nenhuma alteração detectada." });
    return;
  }

  try {
    await authStore.updateUserProfile(updateData);
    successMessage.value = "Perfil atualizado com sucesso!";
    editMode.value = false;
  } catch (error: any) {
    if (authStore.error) {
      setErrors({ apiError: authStore.error });
    } else if (error.response?.data?.detail) {
        const detail = error.response.data.detail;
        if (typeof detail === 'string') {
            setErrors({ apiError: detail });
        } else if (Array.isArray(detail) && detail[0]?.msg) {
            setErrors({ apiError: detail[0].msg });
        } else {
            setErrors({ apiError: 'Falha ao atualizar o perfil.' });
        }
    } else {
      setErrors({ apiError: 'Ocorreu um erro desconhecido ao atualizar o perfil.' });
    }
    console.error("Falha ao atualizar perfil no componente:", error);
  }
};

const handleDeleteAccount = async () => {
  if (window.confirm('TEM CERTEZA ABSOLUTA que deseja deletar sua conta? Esta ação é irreversível.')) {
    if (window.confirm('SEGUNDA CONFIRMAÇÃO: Deletar conta permanentemente?')) {
        authStore.setError(null);
        successMessage.value = null;
        try {
            await authStore.deleteUserAccount();
        } catch (error) {
            console.error("Falha ao deletar conta no componente:", error);
        }
    }
  }
};

const navigateToChangePassword = () => {
  router.push({ name: 'change-password' });
};
</script>

<template>
  <div class="profile-container" v-if="currentUser">
    <h1>Perfil do Usuário</h1>

    <div v-if="successMessage" class="success-message form-feedback">
      {{ successMessage }}
    </div>

    <div v-if="!editMode" class="profile-display">
      <p><strong>Nome Completo:</strong> {{ currentUser.full_name || 'Não informado' }}</p>
      <p><strong>Email:</strong> {{ currentUser.email }}</p>
      <p><strong>Ativo:</strong> {{ currentUser.is_active ? 'Sim' : 'Não' }}</p>
      <p><strong>Superuser:</strong> {{ currentUser.is_superuser ? 'Sim' : 'Não' }}</p>
      <div class="actions-group">
        <button @click="toggleEditMode" class="btn-primary">Editar Perfil</button>
        <button @click="navigateToChangePassword" class="btn-secondary">Alterar Senha</button>
      </div>
    </div>

    <Form v-if="editMode" :validation-schema="validationSchema" :initial-values="formValues" @submit="handleUpdateProfile" v-slot="{ errors, isSubmitting, meta }" class="profile-edit-form">
      <h3>Editar Informações</h3>
      <div class="form-group">
        <label for="fullName-profile">Nome Completo:</label>
        <Field name="fullName" type="text" id="fullName-profile" class="form-control" />
        <ErrorMessage name="fullName" class="invalid-feedback" />
      </div>
      <div class="form-group">
        <label for="email-profile">Email:</label>
        <Field name="email" type="email" id="email-profile" class="form-control" :class="{'is-invalid': errors.email }" required />
        <ErrorMessage name="email" class="invalid-feedback" />
      </div>

      <div v-if="errors.apiError" class="api-error-message form-feedback">
        {{ errors.apiError }}
      </div>
       <div v-else-if="authStore.error && (!meta.dirty || !meta.touched) && !errors.apiError" class="api-error-message form-feedback">
         {{ authStore.error }}
      </div>

      <div class="form-actions">
        <button type="submit" :disabled="isSubmitting || authStore.loading || !meta.dirty" class="btn-primary btn-save">
          {{ (isSubmitting || authStore.loading) ? 'Salvando...' : 'Salvar Alterações' }}
        </button>
        <button type="button" @click="toggleEditMode" class="btn-secondary btn-cancel">Cancelar</button>
      </div>
    </Form>

    <hr class="divider"/>

    <div class="danger-zone">
      <h3>Zona de Perigo</h3>
      <p>Deletar sua conta é uma ação permanente e não pode ser desfeita.</p>
      <button @click="handleDeleteAccount" class="btn-danger" :disabled="authStore.loading && editMode">
        {{ authStore.loading && editMode ? 'Aguarde...' : 'Deletar Minha Conta' }}
      </button>
    </div>
  </div>
  <div v-else class="loading-profile">
    <p>Carregando informações do perfil...</p>
  </div>
</template>

<style scoped>
.profile-container {
  max-width: 650px;
  margin: 40px auto;
  padding: 30px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.08);
}
.profile-container h1, .profile-container h3 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 25px;
}
.profile-container h1 {
  font-size: 2em;
  font-weight: 600;
}
.profile-container h3 {
  font-size: 1.5em;
  font-weight: 500;
  border-bottom: 1px solid #ecf0f1;
  padding-bottom: 10px;
  margin-top: 30px;
}
.profile-display p {
  font-size: 1.1em;
  margin-bottom: 12px;
  color: #34495e;
  line-height: 1.6;
}
.profile-display p strong {
  color: #2c3e50;
  margin-right: 8px;
}
.actions-group {
  margin-top: 25px;
  display: flex;
  gap: 15px;
  justify-content: flex-start;
  flex-wrap: wrap;
}
.btn-primary, .btn-secondary, .btn-danger {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1em;
  font-weight: 500;
  transition: background-color 0.2s, box-shadow 0.2s;
}
.btn-primary { background-color: var(--primary-color, #3498db); color: white; }
.btn-primary:hover:not(:disabled) { background-color: var(--primary-hover-color, #2980b9); box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.btn-secondary { background-color: #bdc3c7; color: #2c3e50; }
.btn-secondary:hover:not(:disabled) { background-color: #95a5a6; }
.btn-danger { background-color: var(--danger-color, #e74c3c); color: white; }
.btn-danger:hover:not(:disabled) { background-color: var(--danger-hover-color, #c0392b); }
.btn-save { margin-right: 10px; }

.profile-edit-form .form-group {
  margin-bottom: 18px;
}
.profile-edit-form label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  color: #34495e;
}
.form-control {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #bdc3c7;
  border-radius: 6px;
  font-size: 1em;
  background-color: #fff;
  transition: border-color 0.2s, box-shadow 0.2s;
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
.form-actions {
  margin-top: 25px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
.form-feedback {
  padding: 12px;
  margin-top: 20px;
  margin-bottom: 20px;
  border-radius: 6px;
  font-size: 0.95em;
  text-align: center;
}
.success-message { color: #1abc9c; background-color: #e8f8f5; border: 1px solid #a3e4d7; }
.api-error-message, .error-message { color: var(--danger-color, #c0392b); background-color: #fdedec; border: 1px solid #f5b7b1; }

.divider {
  margin-top: 35px;
  margin-bottom: 35px;
  border: 0;
  border-top: 1px solid #ecf0f1;
}
.danger-zone {
  padding: 20px;
  border: 1px solid var(--danger-color, #e74c3c);
  border-radius: 8px;
  background-color: #fdecea;
}
.danger-zone h3 { color: var(--danger-color, #c0392b); margin-top: 0; }
.danger-zone p { color: #7b241c; font-size: 0.95em; }
.danger-zone .btn-danger {
  margin-top: 15px;
}
.loading-profile p {
  text-align: center;
  padding: 30px;
  font-size: 1.2em;
  color: #7f8c8d;
}
button:disabled {
  background-color: #d2d6de;
  cursor: not-allowed;
  border-color: #d2d6de;
}
</style>