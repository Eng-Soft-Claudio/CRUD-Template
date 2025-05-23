<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useAdminUsersStore } from '@/stores/adminUsersStore'
import { useToast } from 'vue-toastification'
import { useRouter } from 'vue-router'

const toast = useToast()
const authStore = useAuthStore()
const adminUsersStore = useAdminUsersStore()
const router = useRouter()

const users = computed(() => adminUsersStore.allUsers)
const isLoading = computed(() => adminUsersStore.isLoadingUsers)
const error = computed(() => adminUsersStore.usersError)

onMounted(() => {
  adminUsersStore.fetchUsers()
})

const handleEditUser = (userId: number) => {
  router.push({ name: 'admin-edit-user', params: { id: userId.toString() } })
}

const handleDeleteUser = async (userId: number) => {
  const userToDelete = users.value.find((u) => u.id === userId)
  const userDescription = userToDelete ? `(${userToDelete.email})` : `com ID ${userId}`

  if (authStore.currentUser && authStore.currentUser.id === userId) {
    toast.error(
      'Administradores não podem deletar a própria conta através deste painel. Use a página de perfil.',
    )
    return
  }

  if (
    window.confirm(
      `Tem certeza que deseja deletar o usuário ${userDescription}? Esta ação é irreversível.`,
    )
  ) {
    await adminUsersStore.deleteUser(userId)
  }
}
</script>

<template>
  <div class="view-card-container admin-users-list-layout">
    <header class="view-header">
      <h1>Painel de Administração - Usuários</h1>
      <p v-if="authStore.currentUser" class="subtitle">
        Logado como: {{ authStore.currentUser.email }} ({{
          authStore.currentUser.is_superuser ? 'Superuser' : 'Usuário Comum'
        }})
      </p>
    </header>

    <div class="content-area">
      <div v-if="isLoading && users.length === 0" class="loading-indicator form-feedback">
        <p>Carregando usuários...</p>
      </div>
      <div v-else-if="error" class="error-message form-feedback">
        <p>{{ error }}</p>
      </div>
      <div v-else-if="users.length === 0 && !isLoading" class="info-message form-feedback">
        <p>Nenhum usuário encontrado.</p>
      </div>
      <div v-else class="users-table-wrapper">
        <table class="data-table">
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
                <span :class="user.is_superuser ? 'status-admin' : 'status-normal'">
                  {{ user.is_superuser ? 'Sim' : 'Não' }}
                </span>
              </td>
              <td class="actions-cell">
                <button
                  @click="handleEditUser(user.id)"
                  class="btn btn-small btn-accent"
                  :disabled="isLoading"
                >
                  Editar
                </button>
                <button
                  @click="handleDeleteUser(user.id)"
                  class="btn btn-small btn-danger"
                  :disabled="isLoading"
                >
                  Deletar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="view-actions-footer">
        <RouterLink :to="{ name: 'admin-create-user' }" class="btn btn-primary"
          >Criar Novo Usuário</RouterLink
        >
        <button
          @click="adminUsersStore.fetchUsers()"
          :disabled="isLoading"
          class="btn btn-secondary"
        >
          {{ isLoading ? 'Atualizando...' : 'Atualizar Lista' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-users-list-layout {
  max-width: 1000px;
}
.view-header {
  margin-bottom: var(--padding-lg);
  padding-bottom: var(--padding-md);
  border-bottom: 1px solid var(--color-border);
}
.view-header h1 {
  font-size: 1.8em;
  margin-bottom: var(--padding-xs);
}
.subtitle {
  font-size: 0.9em;
  color: var(--color-text-on-light-secondary);
  font-family: var(--font-sans-ui);
}

.content-area {
  margin-top: var(--padding-md);
}
.users-table-wrapper {
  overflow-x: auto; /* Permite rolagem horizontal em tabelas largas */
}
.data-table {
  /* Classe global potencial para tabelas */
  width: 100%;
  border-collapse: collapse;
  margin-top: var(--padding-md);
  font-size: 0.9rem;
  font-family: var(--font-sans-ui);
}
.data-table th,
.data-table td {
  border: 1px solid var(--color-border);
  padding: var(--padding-sm) var(--padding-md);
  text-align: left;
  vertical-align: middle;
}
.data-table th {
  background-color: var(--color-bg-hover-subtle); /* Fundo sutil para header da tabela */
  font-weight: 600;
}
.data-table tbody tr:nth-child(even) {
  background-color: var(--color-bg-light); /* Zebrado sutil */
}
.data-table tbody tr:hover {
  background-color: var(--color-bg-hover-subtle);
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
  color: var(--color-brand-secondary);
  font-weight: 600;
}
.status-normal {
  color: var(--color-text-on-light-secondary);
}

.actions-cell {
  white-space: nowrap;
  width: 1%; /* Tenta minimizar a largura */
  text-align: center;
}
.btn-small {
  /* Classe utilitária global potencial */
  padding: var(--padding-xs) var(--padding-sm);
  font-size: 0.85em;
  margin: 0 2px;
}
.view-actions-footer {
  margin-top: var(--padding-lg);
  display: flex;
  justify-content: flex-end;
  gap: var(--padding-md);
  border-top: 1px solid var(--color-border);
  padding-top: var(--padding-lg);
}
</style>
