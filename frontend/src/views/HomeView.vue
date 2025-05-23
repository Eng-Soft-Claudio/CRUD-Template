<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

const authStore = useAuthStore()

const userDisplayName = computed(() => {
  if (authStore.currentUser) {
    return authStore.currentUser.full_name || authStore.currentUser.email
  }
  return 'Visitante'
})

const userInitial = computed(() => {
  if (authStore.currentUser?.email) {
    return authStore.currentUser.email.charAt(0).toUpperCase()
  }
  if (authStore.currentUser?.full_name) {
    return authStore.currentUser.full_name.charAt(0).toUpperCase()
  }
  return '?'
})

const getGreeting = () => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Bom dia'
  if (hour < 18) return 'Boa tarde'
  return 'Boa noite'
}

const greeting = computed(() => getGreeting())
</script>

<template>
  <div class="view-card-container home-view-layout">
    <section class="hero-section" :class="{ 'logged-in-hero': authStore.isAuthenticated }">
      <div class="hero-content">
        <template v-if="authStore.isAuthenticated && authStore.currentUser">
          <div class="user-avatar">
            <span>{{ userInitial }}</span>
          </div>
          <h1 class="hero-title">{{ greeting }}, {{ userDisplayName }}!</h1>
          <p class="hero-subtitle">Bem-vindo(a) de volta ao seu painel CRUD Template.</p>
          <p class="hero-text">
            A partir daqui, você pode gerenciar seu perfil, alterar suas configurações de segurança
            ou explorar outras funcionalidades da aplicação.
          </p>
          <div class="hero-actions">
            <RouterLink to="/profile" class="btn btn-primary-inverse">Meu Perfil</RouterLink>
            <RouterLink to="/change-password" class="btn btn-secondary-inverse"
              >Alterar Senha</RouterLink
            >
          </div>
        </template>
        <template v-else>
          <h1 class="hero-title">Bem-vindo ao CRUD Template</h1>
          <p class="hero-subtitle">
            Sua base inicial para projetos incríveis com FastAPI e Vue.js.
          </p>
          <p class="hero-text">
            Este template oferece um sistema completo de autenticação e gerenciamento de usuários
            para você começar rapidamente. Crie sua conta ou faça login para explorar.
          </p>
          <div class="hero-actions">
            <RouterLink to="/register" class="btn btn-primary-inverse">Criar Conta</RouterLink>
            <RouterLink to="/login" class="btn btn-secondary-inverse">Fazer Login</RouterLink>
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
        <p>
          <strong>Status Ativo:</strong>
          <span :class="authStore.currentUser.is_active ? 'status-active' : 'status-inactive'">{{
            authStore.currentUser.is_active ? 'Sim' : 'Ativo'
          }}</span>
        </p>
        <p v-if="authStore.currentUser.is_superuser">
          <strong>Nível de Acesso:</strong> <span class="status-admin">Administrador</span>
        </p>
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
.home-view-layout {
  padding: 0; 
  box-shadow: none; /* Sem sombra dupla */
  background-color: transparent; /* Sem fundo, deixa o fundo da página visível */
}

.hero-section {
  background: linear-gradient(
    135deg,
    var(--color-brand-primary) 0%,
    #4a2f1f 100%
  ); /* Ajuste gradiente */
  color: var(--text-color-light);
  padding: 50px var(--page-padding-mobile);
  text-align: center;
  min-height: 35vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: var(--border-radius-lg); /* Arredondar a hero section */
  margin: var(--padding-md) 0 var(--padding-xl) 0; /* Margem para destacar */
}
.hero-section.logged-in-hero {
  background: linear-gradient(
    135deg,
    var(--color-brand-tertiary) 0%,
    var(--text-color-primary) 100%
  );
}
.hero-content {
  max-width: 90%;
}
.user-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.15);
  color: rgba(117, 106, 89, 1.5);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5em;
  font-weight: bold;
  margin: 0 auto 20px auto;
  border: 2px solid rgba(255, 255, 255, 0.3);
}
.hero-title {
  font-size: 2em;
  font-weight: 700;
  margin-bottom: 10px;
  line-height: 1.2;
  color: rgba(117, 106, 89, 1.5);
}
.hero-subtitle {
  font-size: 1.1em;
  font-weight: 300;
  margin-bottom: 20px;
  opacity: 0.9;
  color: rgba(117, 106, 89, 1.5);
}
.hero-text {
  font-size: 1em;
  margin-bottom: 25px;
  line-height: 1.6;
  opacity: 0.85;
  color: rgba(117, 106, 89, 1.5);
}
.hero-actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

/* Estilo de botão específico para Hero com fundo de marca (para melhor contraste) */
.btn.btn-primary-inverse {
  background-color: var(--text-color-light);
  color: var(--color-brand-primary);
  box-shadow: var(--box-shadow-soft);
}
.btn.btn-primary-inverse:hover {
  background-color: var(--color-bg-hover-subtle);
}
.hero-section.logged-in-hero .btn.btn-primary-inverse {
  background-color: var(--color-brand-secondary);
  color: var(--color-text-on-light-primary);
}
.hero-section.logged-in-hero .btn.btn-primary-inverse:hover {
  background-color: var(--color-link-hover);
}

.btn.btn-secondary-inverse {
  background-color: transparent;
  color: var(--text-color-light);
  border: 2px solid var(--text-color-light);
}
.hero-section.logged-in-hero .btn.btn-secondary-inverse {
  color: var(--color-brand-secondary);
  border-color: var(--color-brand-secondary);
}
.btn.btn-secondary-inverse:hover {
  background-color: var(--text-color-light);
  color: var(--color-brand-primary);
}
.hero-section.logged-in-hero .btn.btn-secondary-inverse:hover {
  background-color: var(--color-brand-secondary);
  color: var(--color-text-on-light-primary);
}

.quick-info-section {
  padding: var(--padding-lg) 0;
} /* Reduzido padding, já está no .view-card-container */
.info-card {
  background-color: var(--color-bg-light);
  padding: var(--padding-lg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--box-shadow-medium);
  border-left: 5px solid var(--color-brand-secondary);
  margin-bottom: var(--padding-xl);
}
.info-card h3 {
  font-size: 1.3em;
  color: var(--color-brand-primary);
  margin-top: 0;
  margin-bottom: var(--padding-md);
}
.info-card p {
  font-size: 1rem;
  color: var(--color-text-on-light-secondary);
  margin-bottom: var(--padding-sm);
  line-height: 1.6;
}
.info-card p strong {
  color: var(--text-color-primary);
}
.status-active {
  color: var(--color-success);
  font-weight: bold;
}
.status-inactive {
  color: var(--color-danger);
  font-weight: bold;
}
.status-admin {
  color: var(--color-brand-secondary);
  font-weight: bold;
  padding: 2px 5px;
  background-color: rgba(192, 160, 98, 0.1);
  border-radius: var(--border-radius-sm);
}

.features-overview-section {
  text-align: center;
  padding: var(--padding-xl) 0;
  background-color: transparent;
}
.features-overview-section h2 {
  font-size: 1.7em;
  color: var(--text-color-primary);
  margin-bottom: var(--padding-lg);
}
.features-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--padding-lg);
}
.feature-item {
  background-color: var(--color-bg-light);
  padding: var(--padding-lg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--box-shadow-light);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}
.feature-item:hover {
  transform: translateY(-4px);
  box-shadow: var(--box-shadow-medium);
}
.feature-icon {
  font-size: 2.2em;
  display: block;
  margin-bottom: var(--padding-md);
  color: var(--color-brand-primary);
}
.feature-item h3 {
  font-size: 1.15em;
  color: var(--text-color-primary);
  margin-bottom: var(--padding-sm);
}
.feature-item p {
  font-size: 0.9rem;
  color: var(--color-text-on-light-secondary);
  line-height: 1.6;
}

@media (min-width: 600px) {
  .hero-actions {
    flex-direction: row;
    max-width: 450px;
    margin-left: auto;
    margin-right: auto;
  }
  .btn {
    width: auto;
    min-width: 160px;
  }
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (min-width: 768px) {
  .hero-section {
    padding: 70px var(--page-padding-desktop);
    min-height: 40vh;
  }
  .hero-content {
    max-width: 650px;
  }
  .user-avatar {
    width: 100px;
    height: 100px;
    font-size: 3em;
    margin-bottom: 25px;
  }
  .hero-title {
    font-size: 2.8em;
  }
  .hero-subtitle {
    font-size: 1.3em;
  }
  .hero-text {
    font-size: 1.1em;
  }
  .quick-info-section {
    padding-top: var(--padding-xl);
    padding-bottom: var(--padding-xl);
  }
}
@media (min-width: 992px) {
  .hero-title {
    font-size: 3.2em;
  }
  .hero-subtitle {
    font-size: 1.4em;
  }
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (min-width: 1200px) {
  .hero-section {
    min-height: 45vh;
    padding-top: 90px;
    padding-bottom: 90px;
  }
  .hero-content {
    max-width: 700px;
  }
  .hero-title {
    font-size: 3.5em;
  }
  .info-card h3 {
    font-size: 1.4em;
  }
  .features-grid {
    grid-template-columns: repeat(4, 1fr);
  }
  .feature-item {
    padding: 25px;
  }
  .feature-icon {
    font-size: 2.5em;
  }
  .feature-item h3 {
    font-size: 1.25em;
  }
  .feature-item p {
    font-size: 0.95rem;
  }
}
@media (min-width: 1600px) {
  .hero-content {
    max-width: 800px;
  }
  .hero-title {
    font-size: 3.8em;
  }
  .hero-subtitle {
    font-size: 1.6em;
  }
  .btn {
    padding: 12px 30px;
    font-size: 1.05em;
  }
}
</style>
