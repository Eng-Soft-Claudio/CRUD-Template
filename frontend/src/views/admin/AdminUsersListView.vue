      
<script setup lang="ts">
import { onMounted, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useAdminUsersStore } from '@/stores/adminUsersStore';
import { useToast } from 'vue-toastification';
import { useRouter } from 'vue-router';

const toast = useToast(); 
const authStore = useAuthStore();
const adminUsersStore = useAdminUsersStore();
const router = useRouter();

const users = computed(() => adminUsersStore.allUsers);
const isLoading = computed(() => adminUsersStore.isLoadingUsers);
const error = computed(() => adminUsersStore.usersError);

onMounted(() => {
  adminUsersStore.fetchUsers();
});

const handleEditUser = (userId: number) => {
  router.push({ name: 'admin-edit-user', params: { id: userId.toString() } });
};

const handleDeleteUser = async (userId: number) => {
  const userToDelete = users.value.find(u => u.id === userId);
  const userDescription = userToDelete ? `(${userToDelete.email})` : `com ID ${userId}`;

  if (authStore.currentUser && authStore.currentUser.id === userId) {
    toast.error("Administradores não podem deletar a própria conta através deste painel. Use a página de perfil.");
    return;
  }

  if (window.confirm(`Tem certeza que deseja deletar o usuário ${userDescription}? Esta ação é irreversível.`)) {
    await adminUsersStore.deleteUser(userId);
  }
};
</script>

<template>
  <div class="admin-users-list-container">
    <header class="admin-header">
      <h1>Painel de Administração - Usuários</h1>
      <p v-if="authStore.currentUser">
        Logado como: {{ authStore.currentUser.email }} ({{ authStore.currentUser.is_superuser ? 'Superuser' : 'Usuário Comum' }})
      </p>
    </header>

    <div class="admin-content">
      <div v-if="isLoading && users.length === 0" class="loading-indicator">
        <p>Carregando usuários...</p>
      </div>
      <div v-else-if="error" class="error-message-box">
        <p>{{ error }}</p>
      </div>
      <div v-else-if="users.length === 0 && !isLoading" class="no-users-message">
        <p>Nenhum usuário encontrado.</p>
      </div>
      <div v-else class="users-table-wrapper">
        <table class="users-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Email</th>
              <th>Nome Completo</th>
              <th>Ativo</th>
              <th>Superuser</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.full_name || 'N/A' }}</td>
              <td>
                <span :class="user.is_active ? 'status-active' : 'status-inactive'">
                  {{ user.is_active ? 'Sim' : 'Não' }}
                </span>
              </td>
              <td>
                <span :class="user.is_superuser ? 'status-admin' : ''">
                  {{ user.is_superuser ? 'Sim' : 'Não' }}
                </span>
              </td>
              <td class="actions-cell">
                <button @click="handleEditUser(user.id)" class="btn-action btn-edit" :disabled="isLoading">Editar</button>
                <button @click="handleDeleteUser(user.id)" class="btn-action btn-delete" :disabled="isLoading">Deletar</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="admin-actions-footer">
         <button @click="adminUsersStore.fetchUsers()" :disabled="isLoading" class="btn-refresh">
          {{ isLoading ? 'Atualizando...' : 'Atualizar Lista' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-users-list-container {
  max-width: var(--content-max-width, 1200px);
  margin: 20px auto;
  padding: 20px var(--desktop-padding, 30px);
}
.admin-header { margin-bottom: 30px; padding-bottom: 15px; border-bottom: 1px solid var(--border-color, #eee); }
.admin-header h1 { font-size: 2em; color: var(--text-color-primary, #2c3e50); margin-bottom: 5px; }
.admin-header p { font-size: 0.9em; color: var(--text-color-secondary, #7f8c8d); }

.admin-content { padding-top: 10px; }
.loading-indicator p, .no-users-message p { text-align: center; font-size: 1.1em; color: var(--text-color-secondary); padding: 20px; }
.error-message-box p { color: var(--danger-color, #e74c3c); background-color: #fdecea; border: 1px solid #f5b0b0; padding: 15px; border-radius: var(--border-radius-md, 6px); text-align: center;}

.users-table-wrapper { overflow-x: auto; }
.users-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  font-size: 0.95em;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.users-table th, .users-table td {
  border: 1px solid var(--border-color, #ddd);
  padding: 10px 12px;
  text-align: left;
  vertical-align: middle;
}
.users-table th {
  background-color: var(--bg-light, #f8f9fa);
  color: var(--text-color-primary, #333);
  font-weight: 600;
}
.users-table tbody tr:nth-child(even) { background-color: #fdfdfd; }
.users-table tbody tr:hover { background-color: #f1f1f1; }

.status-active { color: var(--success-color, #28a745); font-weight: bold; }
.status-inactive { color: var(--danger-color, #dc3545); font-weight: bold; }
.status-admin { color: var(--info-color, #17a2b8); font-weight: bold; }

.actions-cell { white-space: nowrap; width: 1%; text-align: center; }
.btn-action {
  padding: 6px 10px;
  margin: 0 4px;
  border: none;
  border-radius: var(--border-radius-sm, 4px);
  cursor: pointer;
  font-size: 0.85em;
  transition: opacity 0.2s;
}

.btn-action:hover:not(:disabled) { opacity: 0.8; }
.btn-edit { background-color: var(--primary-color, #007bff); color: white; }
.btn-delete { background-color: var(--danger-color, #dc3545); color: white; }
.btn-action:disabled { opacity: 0.5; cursor: not-allowed; }

.admin-actions-footer { margin-top: 30px; display: flex; justify-content: flex-end; gap: 15px; }
.btn-refresh, .btn-primary-action {
  padding: 10px 18px;
  font-size: 1em;
  border: none;
  border-radius: var(--border-radius-md, 6px);
  cursor: pointer;
}
.btn-refresh { background-color: var(--secondary-color, #6c757d); color: white; }
.btn-refresh:hover:not(:disabled) { background-color: var(--secondary-hover-color, #5a6268); }
.btn-refresh:disabled, .btn-primary-action:disabled { background-color: #ccc; }
</style>

    