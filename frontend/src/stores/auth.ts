import { defineStore } from 'pinia';
import apiClient from '@/services/apiService';
import type { UserRead, UserCreate } from '@/types/user'; 
import type { Token } from '@/types/token';
import router from '@/router'; // Importar o router


interface AuthState {
  user: UserRead | null;
  token: string | null;
  isAuthenticated: boolean;
  error: string | null;
  loading: boolean;
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
      this.loading = loading;
    },
    setError(error: string | null) {
      this.error = error;
    },
    setToken(token: string | null) {
      this.token = token;
      this.isAuthenticated = !!token;
      if (token) {
        localStorage.setItem('token', token);
      } else {
        localStorage.removeItem('token');
      }
    },
    setUser(user: UserRead | null) {
      this.user = user;
      if (user) {
        localStorage.setItem('user', JSON.stringify(user));
      } else {
        localStorage.removeItem('user');
      }
    },

    async login(credentials: { username: string; password: string }) {
      this.setLoading(true);
      this.setError(null);
      try {
        const formData = new FormData();
        formData.append('username', credentials.username);
        formData.append('password', credentials.password);

        const response = await apiClient.post<Token>('/auth/login', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded', 
          },
        });
        
        const tokenData = response.data;
        this.setToken(tokenData.access_token);
        await this.fetchCurrentUser(); 
        router.push('/'); 
      } catch (err: any) {
        console.error("Login error:", err);
        if (err.response && err.response.data && err.response.data.detail) {
          this.setError(err.response.data.detail);
        } else {
          this.setError('Falha ao fazer login. Verifique suas credenciais.');
        }
        this.setToken(null);
        this.setUser(null);
      } finally {
        this.setLoading(false);
      }
    },

    async register(userData: UserCreate) {
      this.setLoading(true);
      this.setError(null);
      try {
        const response = await apiClient.post<UserRead>('/auth/register', userData);
        router.push('/login');
        alert('Registro bem-sucedido! Por favor, faça login.'); 
        return response.data;
      } catch (err: any) {
        console.error("Register error:", err);
        if (err.response && err.response.data && err.response.data.detail) {
          this.setError(err.response.data.detail);
        } else {
          this.setError('Falha ao registrar. Tente novamente.');
        }
        throw err; 
      } finally {
        this.setLoading(false);
      }
    },

    async fetchCurrentUser() {
      this.setLoading(true);
      if (!this.token) {
        this.setUser(null);
        this.setLoading(false);
        return;
      }
      try {
        const response = await apiClient.get<UserRead>('/auth/me');
        this.setUser(response.data);
      } catch (err: any) {
        console.error("Fetch current user error:", err);
        this.setUser(null);
        this.setToken(null); 
        if (err.response && err.response.status === 401) {
          router.push('/login');
        }
      } finally {
        this.setLoading(false);
      }
    },

    logout() {
      this.setToken(null);
      this.setUser(null);
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      router.push('/login');
    },

    async tryAutoLogin() {
      if (this.token) {
        await this.fetchCurrentUser();
      }
    }
  },
});