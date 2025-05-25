import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar o token JWT a cada requisição
apiClient.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    const token = authStore.token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para lidar com erros 401 (Não Autorizado)
// Opcional: pode ser útil para deslogar o usuário automaticamente se o token expirar
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      const authStore = useAuthStore();
      // Se não for uma requisição de login que falhou, deslogue
      if (!error.config.url.endsWith('/auth/login')) {
          authStore.logout();
          // Opcionalmente, redirecionar para a página de login
          // router.push('/login'); // Você precisará importar o router aqui
      }
    }
    return Promise.reject(error);
  }
);


export default apiClient;