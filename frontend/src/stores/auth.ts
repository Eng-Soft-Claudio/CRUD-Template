import { defineStore } from 'pinia'
import apiClient from '@/services/apiService'
import type {
  UserRead,
  UserCreate,
  UserPasswordChange,
  PasswordRecoveryRequest,
  PasswordResetForm,
  UserUpdate,
} from '@/types/user'
import type { Token } from '@/types/token'
import router from '@/router'
import { useToast } from 'vue-toastification'

const toast = useToast()

interface AuthState {
  user: UserRead | null
  token: string | null
  isAuthenticated: boolean
  error: string | null
  loading: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    token: localStorage.getItem('token'),
    isAuthenticated: !!localStorage.getItem('token'),
    error: null,
    loading: false,
  }),
  getters: {
    currentUser: (state) => state.user,
  },
  actions: {
    setLoading(loading: boolean) {
      this.loading = loading
    },
    setError(error: string | null) {
      this.error = error
      if (error) {
        toast.error(error); 
      }
    },
    setToken(token: string | null) {
      this.token = token
      this.isAuthenticated = !!token
      if (token) {
        localStorage.setItem('token', token)
      } else {
        localStorage.removeItem('token')
      }
    },
    setUser(user: UserRead | null) {
      this.user = user
      if (user) {
        localStorage.setItem('user', JSON.stringify(user))
      } else {
        localStorage.removeItem('user')
      }
    },

    async login(credentials: { username: string; password: string }) {
      this.setLoading(true)
      this.setError(null)
      try {
        const formData = new FormData()
        formData.append('username', credentials.username)
        formData.append('password', credentials.password)

        const response = await apiClient.post<Token>('/auth/login', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        })

        const tokenData = response.data
        this.setToken(tokenData.access_token)
        await this.fetchCurrentUser()
        router.push('/')
        toast.success('Login bem-sucedido!')
      } catch (err: any) {
        console.error('Login error:', err)
        const errorMessage = err.response?.data?.detail || 'Falha ao fazer login. Verifique suas credenciais.'
        this.setError(errorMessage) 
        this.setToken(null)
        this.setUser(null)
      } finally {
        this.setLoading(false)
      }
    },

    async register(userData: UserCreate) {
      this.setLoading(true)
      this.setError(null)
      try {
        const response = await apiClient.post<UserRead>('/auth/register', userData)
        router.push('/login')
        toast.success('Registro bem-sucedido! Por favor, faça login.')
        return response.data
      } catch (err: any) {
        console.error('Register error:', err)
        const errorMessage = err.response?.data?.detail || 'Falha ao registrar. Tente novamente.'
        this.setError(errorMessage)
        throw err
      } finally {
        this.setLoading(false)
      }
    },

    async fetchCurrentUser() {
      this.setLoading(true)
      if (!this.token) {
        this.setUser(null)
        this.setLoading(false)
        return
      }
      try {
        const response = await apiClient.get<UserRead>('/auth/me')
        this.setUser(response.data)
      } catch (err: any) {
        console.error('Fetch current user error:', err)
        this.setUser(null)
        this.setToken(null)
        if (err.response && err.response.status === 401) {
          router.push('/login')
        }
      } finally {
        this.setLoading(false)
      }
    },

    logout() {
      this.setToken(null)
      this.setUser(null)
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
      toast.info('Você foi desconectado.')
    },

    async tryAutoLogin() {
      if (this.token) {
        await this.fetchCurrentUser()
      }
    },

    async changePassword(passwordData: UserPasswordChange) {
      this.setLoading(true)
      this.setError(null)
      try {
        await apiClient.put('/auth/me/password', passwordData)
        toast.success('Senha alterada com sucesso!')
      } catch (err: any) {
        console.error('Change password error:', err)
        let errorMessage = 'Falha ao alterar a senha. Ocorreu um erro desconhecido.'
        if (err.response?.data?.detail) {
          if (typeof err.response.data.detail === 'string') {
            errorMessage = err.response.data.detail
          } else if (Array.isArray(err.response.data.detail) && err.response.data.detail[0]?.msg) {
            errorMessage = err.response.data.detail[0].msg
          } else {
            errorMessage = 'Falha ao alterar a senha. Verifique os dados fornecidos.'
          }
        } else if (err.message) {
          errorMessage = err.message
        }
        this.setError(errorMessage)
        throw err
      } finally {
        this.setLoading(false)
      }
    },

    async requestPasswordRecovery(email: string) {
      this.setLoading(true)
      this.setError(null)
      try {
        const recoveryData: PasswordRecoveryRequest = { email }
        const response = await apiClient.post<{ message: string }>(
          '/auth/password-recovery',
          recoveryData,
        )
        toast.info(response.data.message + " Em DEV, verifique os logs do backend para o token.")
        return response.data.message
      } catch (err: any) {
        console.error('Password recovery request error:', err)
        const errorMessage = err.response?.data?.detail || 'Ocorreu um erro ao solicitar a recuperação de senha.'
        this.setError(errorMessage)
        throw err
      } finally {
        this.setLoading(false)
      }
    },

    async resetPassword(resetData: PasswordResetForm) {
      this.setLoading(true)
      this.setError(null)
      try {
        await apiClient.post('/auth/reset-password', resetData)
        router.push('/login')
        toast.success('Senha redefinida com sucesso! Por favor, faça login com sua nova senha.')
      } catch (err: any) {
        console.error('Reset password error:', err)
        let errorMessage = 'Falha ao redefinir a senha. Tente novamente ou solicite um novo link.'
        if (err.response?.data?.detail) {
          if (typeof err.response.data.detail === 'string') {
            errorMessage = err.response.data.detail
          } else if (Array.isArray(err.response.data.detail) && err.response.data.detail[0]?.msg) {
            errorMessage = err.response.data.detail[0].msg
          } else {
            errorMessage = 'Falha ao redefinir a senha.'
          }
        }
        this.setError(errorMessage)
        throw err
      } finally {
        this.setLoading(false)
      }
    },

    async updateUserProfile(updateData: UserUpdate) {
      this.setLoading(true)
      this.setError(null)
      try {
        const response = await apiClient.patch<UserRead>('/auth/me', updateData)
        this.setUser(response.data)
        toast.success('Perfil atualizado com sucesso!')
        return response.data
      } catch (err: any) {
        console.error("Update profile error:", err)
        let errorMessage = 'Falha ao atualizar o perfil. Ocorreu um erro desconhecido.'
        if (err.response?.data?.detail) {
             if (typeof err.response.data.detail === 'string') {
                errorMessage = err.response.data.detail
            } else if (Array.isArray(err.response.data.detail) && err.response.data.detail[0]?.msg) {
                errorMessage = err.response.data.detail[0].msg
            } else {
                errorMessage = 'Falha ao atualizar o perfil.'
            }
        }
        this.setError(errorMessage)
        throw err
      } finally {
        this.setLoading(false)
      }
    },

    async deleteUserAccount() {
      this.setLoading(true)
      this.setError(null)
      try {
        await apiClient.delete('/auth/me')
        this.logout() 
        toast.success('Sua conta foi deletada com sucesso.')
      } catch (err: any) {
        console.error("Delete account error:", err)
        const errorMessage = err.response?.data?.detail || 'Falha ao deletar a conta. Tente novamente.'
        this.setError(errorMessage)
        throw err
      } finally {
        this.setLoading(false)
      }
    },
  },
})