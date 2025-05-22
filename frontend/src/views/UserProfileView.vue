<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import type { UserUpdate } from '@/types/user';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const currentUser = computed(() => authStore.currentUser);

const fullName = ref('');
const email = ref(''); 

const editMode = ref(false); 
const successMessage = ref<string | null>(null);
const generalError = ref<string | null>(null); 

const showDeleteConfirmModal = ref(false);

const clearMessages = () => {
  authStore.setError(null);
  successMessage.value = null;
  generalError.value = null;
};

onMounted(() => {
  if (currentUser.value) {
    fullName.value = currentUser.value.full_name || '';
    email.value = currentUser.value.email;
  }
});

authStore.$subscribe((mutation, state) => {
  if (state.user) {
    fullName.value = state.user.full_name || '';
    email.value = state.user.email;
  }
});

const toggleEditMode = () => {
  editMode.value = !editMode.value;
  clearMessages();
  if (currentUser.value) {
    fullName.value = currentUser.value.full_name || '';
    email.value = currentUser.value.email;
  }
};

const handleUpdateProfile = async () => {
  clearMessages();
  if (!currentUser.value) {
    generalError.value = "Usuário não encontrado.";
    return;
  }

  const updateData: UserUpdate = {};
  let hasChanges = false;

  if (fullName.value !== (currentUser.value.full_name || '')) {
    updateData.full_name = fullName.value.trim() === '' ? null : fullName.value.trim();
    hasChanges = true;
  }
  if (email.value !== currentUser.value.email) {
    updateData.email = email.value;
    hasChanges = true;
  }

  if (!hasChanges) {
    generalError.value = "Nenhuma alteração detectada.";
    return;
  }
  if (updateData.email && !/\S+@\S+\.\S+/.test(updateData.email)) {
    generalError.value = "Formato de email inválido.";
    return;
  }


  try {
    await authStore.updateUserProfile(updateData);
    successMessage.value = "Perfil atualizado com sucesso!";
    editMode.value = false; 
  } catch (error) {
    console.error("Falha ao atualizar perfil no componente:", error);
  }
};

const handleDeleteAccount = async () => {
  if (window.confirm('TEM CERTEZA ABSOLUTA que deseja deletar sua conta? Esta ação é irreversível.')) {
    if (window.confirm('SEGUNDA CONFIRMAÇÃO: Deletar conta permanentemente?')) {
        clearMessages();
        showDeleteConfirmModal.value = false; 
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

    <div v-if="!editMode" class="profile-display">
      <p><strong>Nome Completo:</strong> {{ currentUser.full_name || 'Não informado' }}</p>
      <p><strong>Email:</strong> {{ currentUser.email }}</p>
      <p><strong>Ativo:</strong> {{ currentUser.is_active ? 'Sim' : 'Não' }}</p>
      <p><strong>Superuser:</strong> {{ currentUser.is_superuser ? 'Sim' : 'Não' }}</p>
      <button @click="toggleEditMode" class="btn-edit">Editar Perfil</button>
      <button @click="navigateToChangePassword" class="btn-secondary">Alterar Senha</button>
    </div>

    <form v-if="editMode" @submit.prevent="handleUpdateProfile" class="profile-edit-form">
      <h3>Editar Informações</h3>
      <div>
        <label for="fullName">Nome Completo:</label>
        <input type="text" id="fullName" v-model="fullName" />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div class="form-actions">
        <button type="submit" :disabled="authStore.loading" class="btn-save">
          {{ authStore.loading ? 'Salvando...' : 'Salvar Alterações' }}
        </button>
        <button type="button" @click="toggleEditMode" class="btn-cancel">Cancelar</button>
      </div>
    </form>

    <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
    <p v-if="authStore.error" class="error-message">{{ authStore.error }}</p>
    <p v-if="generalError" class="error-message">{{ generalError }}</p>

    <hr class="divider"/>

    <div class="danger-zone">
      <h3>Zona de Perigo</h3>
      <p>Deletar sua conta é uma ação permanente e não pode ser desfeita.</p>
      <button @click="handleDeleteAccount" class="btn-danger" :disabled="authStore.loading">
        {{ authStore.loading && !editMode ? 'Processando...' : 'Deletar Minha Conta' }}
      </button>
    </div>
  </div>
  <div v-else>
    <p>Carregando informações do perfil ou usuário não autenticado...</p>
  </div>
</template>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 30px auto;
  padding: 25px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.profile-container h1, .profile-container h3 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}
.profile-display p {
  font-size: 1.1em;
  margin-bottom: 10px;
  color: #555;
}
.profile-display p strong {
  color: #333;
}
.btn-edit, .btn-secondary, .btn-save, .btn-cancel, .btn-danger {
  padding: 10px 18px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  margin-top: 10px;
  margin-right: 10px;
  transition: background-color 0.2s, transform 0.1s;
}
.btn-edit, .btn-save { background-color: #28a745; color: white; }
.btn-edit:hover, .btn-save:hover { background-color: #218838; }
.btn-secondary { background-color: #6c757d; color: white; }
.btn-secondary:hover { background-color: #5a6268; }
.btn-cancel { background-color: #ffc107; color: #212529; }
.btn-cancel:hover { background-color: #e0a800; }
.btn-danger { background-color: #dc3545; color: white; }
.btn-danger:hover { background-color: #c82333; }
.btn-danger:disabled, .btn-save:disabled {
  background-color: #ccc;
}

.profile-edit-form div {
  margin-bottom: 15px;
}
.profile-edit-form label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}
.profile-edit-form input {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.form-actions {
  margin-top: 20px;
  text-align: right;
}
.success-message, .error-message {
  padding: 10px;
  margin-top: 15px;
  border-radius: 4px;
  font-size: 0.95em;
  text-align: center;
}
.success-message { color: #155724; background-color: #d4edda; border: 1px solid #c3e6cb; }
.error-message { color: #721c24; background-color: #f8d7da; border: 1px solid #f5c6cb; }

.divider {
  margin-top: 30px;
  margin-bottom: 30px;
  border: 0;
  border-top: 1px solid #eee;
}
.danger-zone {
  padding: 15px;
  border: 1px solid #dc3545;
  border-radius: 5px;
  background-color: #f8d7da;
}
.danger-zone h3 { color: #721c24; }
.danger-zone p { color: #721c24; font-size: 0.9em; }
</style>