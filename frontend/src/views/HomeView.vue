<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
import { computed } from 'vue';
import { RouterLink } from 'vue-router';

const authStore = useAuthStore();

const userDisplayName = computed(() => {
  if (authStore.currentUser) {
    return authStore.currentUser.full_name || authStore.currentUser.email;
  }
  return 'Visitante';
});

const userInitial = computed(() => {
  if (authStore.currentUser?.email) {
    return authStore.currentUser.email.charAt(0).toUpperCase();
  }
  if (authStore.currentUser?.full_name) {
    return authStore.currentUser.full_name.charAt(0).toUpperCase();
  }
  return '?';
});

const getGreeting = () => {
  const hour = new Date().getHours();
  if (hour < 12) return 'Bom dia';
  if (hour < 18) return 'Boa tarde';
  return 'Boa noite';
};

const greeting = computed(() => getGreeting());

</script>

<template>
  <div class="home-view-wrapper">
    <section class="hero-section" :class="{ 'logged-in-hero': authStore.isAuthenticated }">
      <div class="hero-content">
        <template v-if="authStore.isAuthenticated && authStore.currentUser">
          <div class="user-avatar">
            <span>{{ userInitial }}</span>
          </div>
          <h1 class="hero-title">{{ greeting }}, {{ userDisplayName }}!</h1>
          <p class="hero-subtitle">Bem-vindo(a) de volta ao seu painel CRUD Template.</p>
          <p class="hero-text">A partir daqui, você pode gerenciar seu perfil, alterar suas configurações de segurança ou explorar outras funcionalidades da aplicação.</p>
          <div class="hero-actions">
            <RouterLink to="/profile" class="btn btn-primary">Meu Perfil</RouterLink>
            <RouterLink to="/change-password" class="btn btn-secondary">Alterar Senha</RouterLink>
          </div>
        </template>
        <template v-else>
          <h1 class="hero-title">Bem-vindo ao CRUD Template</h1>
          <p class="hero-subtitle">Sua base inicial para projetos incríveis com FastAPI e Vue.js.</p>
          <p class="hero-text">
            Este template oferece um sistema completo de autenticação e gerenciamento de usuários para você começar
            rapidamente. Crie sua conta ou faça login para explorar.
          </p>
          <div class="hero-actions">
            <RouterLink to="/register" class="btn btn-primary">Criar Conta</RouterLink>
            <RouterLink to="/login" class="btn btn-secondary">Fazer Login</RouterLink>
          </div>
        </template>
      </div>
    </section>

    <section v-if="authStore.isAuthenticated && authStore.currentUser" class="quick-info-section">
      <div class="info-card">
        <h3>Status da Conta</h3>
        <p><strong>Email:</strong> {{ authStore.currentUser.email }}</p>
        <p><strong>Nome:</strong> {{ authStore.currentUser.full_name || 'Não informado' }}</p>
        <p><strong>ID do Usuário:</strong> {{ authStore.currentUser.id }}</p>
        <p><strong>Status:</strong> <span :class="authStore.currentUser.is_active ? 'status-active' : 'status-inactive'">{{ authStore.currentUser.is_active ? 'Sim' : 'Ativo' }}</span></p>
        <p v-if="authStore.currentUser.is_superuser"><strong>Nível de Acesso:</strong> <span class="status-admin">Administrador</span></p>
      </div>
    </section>

    <section class="features-overview-section" v-else>
        <h2>Funcionalidades Principais</h2>
        <div class="features-grid">
            <div class="feature-item">
                <span class="feature-icon">🔐</span>
                <h3>Autenticação Segura</h3>
                <p>Registro, login e gerenciamento de sessão com JWT.</p>
            </div>
            <div class="feature-item">
                <span class="feature-icon">👤</span>
                <h3>Gerenciamento de Perfil</h3>
                <p>Usuários podem visualizar e atualizar seus próprios dados.</p>
            </div>
            <div class="feature-item">
                <span class="feature-icon">🔑</span>
                <h3>Recuperação de Senha</h3>
                <p>Fluxo completo para redefinição de senhas esquecidas.</p>
            </div>
            <div class="feature-item">
                <span class="feature-icon">🛠️</span>
                <h3>Base para Administradores</h3>
                <p>Pronto para expansão com funcionalidades de admin.</p>
            </div>
        </div>
    </section>
  </div>
</template>

<style scoped>

.home-view-wrapper {
  padding-bottom: 40px;
  width: 100%;
}

.hero-section {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover-color) 100%);
  color: var(--text-color-light);
  padding: 40px var(--mobile-padding);
  text-align: center;
  min-height: 30vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.hero-section.logged-in-hero {
   background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
}

.hero-content {
  max-width: 90%;
}

.user-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5em;
  font-weight: bold;
  margin: 0 auto 20px auto;
  border: 2px solid rgba(255, 255, 255, 0.4);
}

.hero-title {
  font-size: 2em;
  font-weight: 700;
  margin-bottom: 10px;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.1em;
  font-weight: 300;
  margin-bottom: 20px;
  opacity: 0.9;
}

.hero-text {
  font-size: 1em;
  margin-bottom: 25px;
  line-height: 1.6;
  opacity: 0.85;
}

.hero-actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.btn {
  padding: 10px 20px;
  font-size: 1em;
  text-decoration: none;
  border-radius: var(--border-radius-md);
  transition: background-color 0.2s ease, transform 0.2s ease;
  border: none;
  cursor: pointer;
  font-weight: 500;
  width: 100%;
  max-width: 280px;
}

.btn-primary { background-color: #ffffff; color: var(--primary-color); box-shadow: var(--box-shadow-light); }
.hero-section.logged-in-hero .btn-primary { background-color: var(--primary-color); color: var(--text-on-primary); }
.btn-primary:hover { background-color: #f0f0f0; transform: translateY(-2px); }
.hero-section.logged-in-hero .btn-primary:hover { background-color: var(--primary-hover-color); }

.btn-secondary { background-color: transparent; color: var(--text-color-light); border: 2px solid var(--text-color-light); }
.hero-section.logged-in-hero .btn-secondary { color: var(--primary-color); border-color: var(--primary-color); }
.btn-secondary:hover { background-color: var(--text-color-light); color: var(--primary-color); transform: translateY(-2px); }
.hero-section.logged-in-hero .btn-secondary:hover { background-color: var(--primary-color); color: var(--text-on-primary); }

.quick-info-section {
  padding: 30px var(--mobile-padding);
  max-width: var(--content-max-width);
  margin: 0 auto;
}

.info-card {
  background-color: var(--bg-light);
  padding: 20px;
  border-radius: var(--border-radius-lg);
  box-shadow: var(--box-shadow-medium);
  border-left: 4px solid var(--primary-color);
}
.info-card h3 { font-size: 1.4em; color: var(--text-color-primary); margin-top: 0; margin-bottom: 15px; }
.info-card p { font-size: 0.95em; color: var(--text-color-secondary); margin-bottom: 8px; line-height: 1.6; }
.info-card p strong { color: #374151; } /* Poderia ser --text-color-primary também */
.status-active { color: var(--success-color, #16a34a); font-weight: bold; }
.status-inactive { color: var(--danger-color, #dc2626); font-weight: bold; }
.status-admin { color: var(--info-color, #7c3aed); font-weight: bold; padding: 2px 5px; background-color: rgba(124, 58, 237, 0.1); border-radius: var(--border-radius-sm); }

.features-overview-section { text-align: center; padding: 40px var(--mobile-padding); background-color: var(--bg-page); }
.features-overview-section h2 { font-size: 1.8em; color: var(--text-color-primary); margin-bottom: 30px; }
.features-grid { display: grid; grid-template-columns: 1fr; gap: 20px; max-width: var(--content-max-width); margin: 0 auto; }
.feature-item { background-color: var(--bg-light); padding: 20px; border-radius: var(--border-radius-lg); box-shadow: var(--box-shadow-light); transition: transform 0.2s ease, box-shadow 0.2s ease; }
.feature-item:hover { transform: translateY(-4px); box-shadow: 0 5px 10px rgba(0,0,0,0.1); }
.feature-icon { font-size: 2.2em; display: block; margin-bottom: 12px; color: var(--primary-color); }
.feature-item h3 { font-size: 1.2em; color: var(--text-color-primary); margin-bottom: 8px; }
.feature-item p { font-size: 0.9em; color: var(--text-color-secondary); line-height: 1.6; }


@media (min-width: 600px) {
  .hero-actions {
    flex-direction: row;
    max-width: 450px;
    margin-left: auto;
    margin-right: auto;
  }
  .btn {
     width: auto;
     min-width: 150px;
  }
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 768px) {
  .hero-section { padding: 60px var(--desktop-padding); min-height: 35vh; }
  .hero-content { max-width: 650px; }
  .user-avatar { width: 90px; height: 90px; font-size: 2.8em; margin-bottom: 20px; }
  .hero-title { font-size: 2.8em; }
  .hero-subtitle { font-size: 1.3em; }
  .hero-text { font-size: 1.1em; }
  .quick-info-section { padding: 40px var(--desktop-padding); }
  .features-overview-section { padding: 50px var(--desktop-padding); }
  .features-overview-section h2 { font-size: 2em; }
}

@media (min-width: 992px) {
  .hero-title { font-size: 3.2em; }
  .hero-subtitle { font-size: 1.4em; }
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1200px) {
  .hero-section { min-height: 40vh; padding-top: 80px; padding-bottom: 80px; }
  .hero-content { max-width: 700px; }
  .hero-title { font-size: 3.5em; }
  .hero-subtitle { font-size: 1.5em; }
  .hero-text { font-size: 1.15em; }
  .user-avatar { width: 100px; height: 100px; font-size: 3em; }
  .quick-info-section { padding-top: 50px; padding-bottom: 50px; }
  .info-card h3 { font-size: 1.6em; }
  .info-card p { font-size: 1.05em; }
  .features-overview-section h2 { font-size: 2.2em; margin-bottom: 50px; }
  .features-grid {
     grid-template-columns: repeat(4, 1fr);
  }
  .feature-item { padding: 30px; }
  .feature-icon { font-size: 2.8em; }
  .feature-item h3 { font-size: 1.4em; }
  .feature-item p { font-size: 1em; }
}

@media (min-width: 1600px) {
  .hero-content { max-width: 800px; }
  .hero-title { font-size: 4em; }
  .hero-subtitle { font-size: 1.7em; }
  .hero-text { font-size: 1.2em; }
  .btn { padding: 14px 32px; font-size: 1.1em; }
}
</style>