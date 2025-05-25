import { defineStore } from 'pinia'
import apiClient from '@/services/apiService'
import type { UserRead, UserUpdate, UserCreate } from '@/types/user'
import { useToast } from 'vue-toastification'

const toast = useToast()

interface AdminUserState {
  user: UserRead | null
}

interface AdminUsersState {
  users: UserRead[]
  currentUserForEdit: UserRead | null
  isLoading: boolean
  isLoadingSingleUser: boolean
  error: string | null
  singleUserError: string | null
  totalUsers: number
  currentPage: number
  itemsPerPage: number
}

export const useAdminUsersStore = defineStore('adminUsers', {
  state: (): AdminUsersState => ({
    users: [],
    currentUserForEdit: null,
    isLoading: false,
    isLoadingSingleUser: false,
    error: null,
    singleUserError: null,
    totalUsers: 0,
    currentPage: 1,
    itemsPerPage: 100,
  }),
  getters: {
    allUsers: (state) => state.users,
    isLoadingUsers: (state) => state.isLoading,
    usersError: (state) => state.error,
    userForEdit: (state) => state.currentUserForEdit,
    isLoadingUserForEdit: (state) => state.isLoadingSingleUser,
    userForEditError: (state) => state.singleUserError,
  },
  actions: {
    _setLoading(loading: boolean) {
      this.isLoading = loading
    },
    _setError(error: string | null) {
      this.error = error
      if (error && !this.isLoadingSingleUser) {
        toast.error(error)
      }
    },
    _setUsers(users: UserRead[]) {
      this.users = users
    },
    _setPaginationDetails(total: number, page: number, limit: number) {
      this.totalUsers = total
      this.currentPage = page
      this.itemsPerPage = limit
    },
    _setCurrentUserForEdit(user: UserRead | null) {
      this.currentUserForEdit = user
    },
    _setLoadingSingleUser(loading: boolean) {
      this.isLoadingSingleUser = loading
    },
    _setSingleUserError(error: string | null) {
      this.singleUserError = error
      if (error) {
        toast.error(error)
      }
    },

    async fetchUsers(skip: number = 0, limit: number = 100) {
      this._setLoading(true)
      this._setError(null)
      try {
        const response = await apiClient.get<UserRead[]>(`/users/`, {
          params: { skip, limit },
        })
        this._setUsers(response.data)
      } catch (err: any) {
        console.error('Error fetching users:', err)
        const errorMessage = err.response?.data?.detail || 'Falha ao carregar usuários.'
        this._setError(errorMessage)
        this._setUsers([])
      } finally {
        this._setLoading(false)
      }
    },

    async fetchUserById(userId: number) {
      this._setLoadingSingleUser(true)
      this._setSingleUserError(null)
      this._setCurrentUserForEdit(null)
      try {
        const response = await apiClient.get<UserRead>(`/users/${userId}`)
        this._setCurrentUserForEdit(response.data)
        return response.data
      } catch (err: any) {
        console.error(`Error fetching user ${userId}:`, err)
        const errorMessage =
          err.response?.data?.detail || `Falha ao carregar usuário com ID ${userId}.`
        this._setSingleUserError(errorMessage)
        throw err
      } finally {
        this._setLoadingSingleUser(false)
      }
    },

    async deleteUser(userId: number) {
      this._setLoading(true)
      this._setError(null)
      try {
        await apiClient.delete(`/users/${userId}`)
        toast.success(`Usuário com ID ${userId} deletado com sucesso.`)
        this.users = this.users.filter((user) => user.id !== userId)
      } catch (err: any) {
        console.error(`Error deleting user ${userId}:`, err)
        const errorMessage =
          err.response?.data?.detail || `Falha ao deletar usuário com ID ${userId}.`
        this._setError(errorMessage)
      } finally {
        this._setLoading(false)
      }
    },

    async updateUserByAdmin(userId: number, updateData: UserUpdate) {
      this._setLoading(true)
      this._setError(null)
      try {
        const response = await apiClient.put<UserRead>(`/users/${userId}`, updateData)
        toast.success(`Usuário ID ${userId} atualizado com sucesso.`)
        const userIndex = this.users.findIndex((u) => u.id === userId)
        if (userIndex !== -1) {
          this.users[userIndex] = response.data
        }
        if (this.currentUserForEdit && this.currentUserForEdit.id === userId) {
          this._setCurrentUserForEdit(response.data)
        }
        return response.data
      } catch (err: any) {
        const errorMessage =
          err.response?.data?.detail || `Falha ao atualizar usuário ID ${userId}.`
        this._setError(errorMessage)
        throw err
      } finally {
        this._setLoading(false)
      }
    },

    async createUserByAdmin(userData: UserCreate) {
      this._setLoading(true)
      this._setError(null)
      try {
        const response = await apiClient.post<UserRead>(`/users/`, userData)
        toast.success(`Usuário ${response.data.email} criado com sucesso.`)
        this.users.unshift(response.data)
        return response.data
      } catch (err: any) {
        console.error('Error creating user (admin):', err)
        const errorMessage = err.response?.data?.detail || 'Falha ao criar usuário.'
        this._setError(errorMessage)
        throw err
      } finally {
        this._setLoading(false)
      }
    },
  },
})
