<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { onMounted, computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const authStore = useAuthStore()
const route = useRoute()

const userDisplayName = computed(() => {
  if (authStore.currentUser) {
    return authStore.currentUser.full_name || authStore.currentUser.email
  }
  return ''
})

const isAdmin = computed(() => authStore.currentUser?.is_superuser || false)

const isMobileMenuOpen = ref(false)

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

watch(
  () => route.path,
  () => {
    closeMobileMenu()
  },
)

onMounted(async () => {
  await authStore.tryAutoLogin()
})

const handleLogout = () => {
  closeMobileMenu()
  authStore.logout()
}
</script>

<template>
  <div class="app-layout">
    <header class="app-header">
      <div class="nav-container">
        <div class="logo-area">
          <RouterLink to="/" class="project-name" @click="closeMobileMenu"
            >CRUD Template</RouterLink
          >
        </div>

        <button
          @click="toggleMobileMenu"
          class="mobile-menu-toggle"
          aria-label="Toggle menu"
          :aria-expanded="isMobileMenuOpen"
        >
          <span class="hamburger-icon">
            <span class="line line1"></span>
            <span class="line line2"></span>
            <span class="line line3"></span>
          </span>
        </button>

        <div class="navigation-wrapper" :class="{ 'is-open': isMobileMenuOpen }">
          <nav class="main-navigation">
            <RouterLink to="/" @click="closeMobileMenu">Home</RouterLink>
            <RouterLink to="/about" @click="closeMobileMenu">About</RouterLink>
            <RouterLink v-if="isAdmin" to="/admin/users" class="admin-link" @click="closeMobileMenu"
              >Admin Usuários</RouterLink
            >
          </nav>
          <nav class="user-navigation">
            <template v-if="!authStore.isAuthenticated">
              <RouterLink to="/login" @click="closeMobileMenu">Login</RouterLink>
              <RouterLink to="/register" @click="closeMobileMenu">Registrar</RouterLink>
            </template>
            <template v-else>
              <span class="user-greeting">Olá, {{ userDisplayName }}!</span>
              <RouterLink to="/profile" @click="closeMobileMenu">Meu Perfil</RouterLink>
              <button @click="handleLogout" class="logout-button">Logout</button>
            </template>
          </nav>
        </div>
      </div>
    </header>

    <main class="main-content" @click="closeMobileMenu">
      <!-- Fecha menu ao clicar no conteúdo principal -->
      <RouterView v-slot="{ Component }">
        <transition name="route-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </RouterView>
    </main>

    <footer class="app-footer">
      <p>© {{ new Date().getFullYear() }} CRUD Template. Todos os direitos reservados.</p>
    </footer>
  </div>
</template>

<style scoped>
/* :root e variáveis CSS como definido em main.css globalmente */

.app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--bg-page);
}
.app-header {
  background-color: var(--bg-light);
  border-bottom: 1px solid var(--border-color);
  width: 100%;
  box-shadow: var(--box-shadow-light);
  line-height: 1.5;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-container {
  display: flex;
  justify-content: space-between; /* Alinha logo à esquerda e o resto à direita */
  align-items: center;
  padding: 0 var(--mobile-padding);
  min-height: var(--header-height);
  position: relative; /* Para o posicionamento absoluto do menu mobile */
}

.logo-area {
  /* Não precisa mais de margin-bottom, pois é linha única em mobile com hamburger */
}
.project-name {
  font-size: 1.5em;
  font-weight: 700;
  color: var(--text-color-primary);
  text-decoration: none;
}

.mobile-menu-toggle {
  display: none; /* Escondido em telas maiores */
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--padding-sm);
  z-index: 1010; /* Acima do menu mobile */
}
.hamburger-icon {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  width: 24px;
  height: 20px;
}
.hamburger-icon .line {
  display: block;
  height: 2px;
  width: 100%;
  background-color: var(--text-color-primary);
  border-radius: 2px;
  transition: all 0.3s ease-in-out;
}

/* Animação do Hamburger para X */
.navigation-wrapper.is-open ~ .mobile-menu-toggle .hamburger-icon .line1 {
  transform: rotate(45deg) translate(5px, 5px);
}
.navigation-wrapper.is-open ~ .mobile-menu-toggle .hamburger-icon .line2 {
  opacity: 0;
}
.navigation-wrapper.is-open ~ .mobile-menu-toggle .hamburger-icon .line3 {
  transform: rotate(-45deg) translate(5px, -5px);
}

.navigation-wrapper {
  display: flex;
  align-items: center; /* Padrão para desktop */
  gap: var(--padding-md);
}

.main-navigation,
.user-navigation {
  display: flex;
  align-items: center;
  gap: var(--padding-sm);
  flex-wrap: wrap;
}

.main-navigation a,
.user-navigation a,
.user-navigation .user-greeting,
.user-navigation .logout-button {
  padding: var(--padding-sm) var(--padding-md);
  text-decoration: none;
  color: var(--primary-color);
  border-radius: var(--border-radius-sm);
  transition:
    background-color 0.2s ease,
    color 0.2s ease;
  font-size: 0.95em;
  white-space: nowrap;
}
.main-navigation a:hover,
.user-navigation a:hover,
.user-navigation .logout-button:hover {
  background-color: var(--link-hover-bg);
  color: var(--primary-hover-color);
}
.main-navigation a.router-link-exact-active {
  background-color: var(--primary-color);
  color: var(--text-on-primary);
  font-weight: 600;
}
.main-navigation a.router-link-exact-active:hover {
  background-color: var(--primary-hover-color);
}
.admin-link {
  color: var(--admin-link-color, #ffc107) !important;
  font-weight: bold;
}
.admin-link:hover {
  background-color: var(--admin-link-hover-bg, #e0a800) !important;
  color: var(--text-color-primary) !important;
}
.admin-link.router-link-exact-active {
  background-color: var(--admin-link-hover-bg, #e0a800) !important;
  color: var(--text-color-primary) !important;
}
.user-greeting {
  color: var(--text-color-secondary);
  margin-right: var(--padding-sm);
  cursor: default;
  padding: var(--padding-sm) var(--padding-md);
}
.logout-button {
  background: none;
  border: 1px solid var(--danger-color);
  color: var(--danger-color);
  cursor: pointer;
}
.logout-button:hover {
  background-color: var(--danger-color) !important;
  color: var(--text-on-primary) !important;
}

.main-content {
  width: 100%;
  max-width: var(--content-max-width);
  margin: 25px auto;
  padding: 0 var(--mobile-padding);
  flex-grow: 1;
}
.route-fade-enter-active,
.route-fade-leave-active {
  transition: opacity 0.15s ease;
}
.route-fade-enter-from,
.route-fade-leave-to {
  opacity: 0;
}
.app-footer {
  text-align: center;
  padding: var(--padding-lg) var(--mobile-padding);
  background-color: var(--bg-dark);
  color: var(--text-on-dark-bg);
  font-size: 0.875em;
  width: 100%;
}

/* Media Queries para o Menu Hamburger e Layout Desktop */
/* Breakpoint para mobile (onde o hamburger aparece). Ex: até 768px */
@media (max-width: 767.98px) {
  .mobile-menu-toggle {
    display: flex; /* Mostra o hamburger */
  }
  .nav-container {
    /* justify-content: space-between; Garante logo à esquerda e hamburger à direita */
  }
  .navigation-wrapper {
    display: none; /* Esconde o menu por padrão */
    flex-direction: column;
    align-items: flex-start; /* Alinha itens à esquerda no menu aberto */
    position: absolute;
    top: var(--header-height); /* Abaixo do header */
    left: 0;
    right: 0;
    background-color: var(--bg-light);
    padding: var(--padding-md) var(--mobile-padding);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-top: 1px solid var(--border-color);
    z-index: 999; /* Abaixo do botão de toggle, mas acima do conteúdo */
  }
  .navigation-wrapper.is-open {
    display: flex; /* Mostra o menu quando aberto */
  }
  .main-navigation,
  .user-navigation {
    flex-direction: column;
    width: 100%;
    gap: 0;
    margin-bottom: 0; /* Reset margin */
  }
  .main-navigation a,
  .user-navigation a,
  .user-navigation .user-greeting,
  .user-navigation .logout-button {
    width: 100%; /* Itens ocupam largura total */
    padding: var(--padding-md) var(--padding-sm); /* Ajuste no padding */
    border-bottom: 1px solid var(--border-color); /* Linhas divisórias */
    border-radius: 0;
  }
  .main-navigation a:last-child,
  .user-navigation a:last-child,
  .user-navigation .logout-button {
    border-bottom: none;
  }
  .user-actions-area {
    /* No mobile, o user-actions-area não é mais um agrupador separado visualmente */
    width: 100%;
  }
  .user-greeting {
    text-align: left;
  }
}

@media (min-width: 768px) {
  .nav-container {
    max-width: var(--content-max-width);
    margin: 0 auto;
    padding: 0 var(--desktop-padding);
    /* justify-content: space-between; já está em .nav-container base */
  }
  .logo-area {
    margin-right: var(--padding-lg); /* Espaço entre logo e main-nav */
  }
  .navigation-wrapper {
    display: flex !important; /* Garante que esteja visível e flex em desktop */
    flex-direction: row;
    position: static; /* Reset position */
    background-color: transparent;
    padding: 0;
    box-shadow: none;
    border-top: none;
    width: auto; /* Ocupa o espaço restante */
    flex-grow: 1; /* Para ocupar o espaço disponível */
    justify-content: space-between; /* Espaça main-nav e user-actions-area */
  }
  .main-navigation {
    flex-direction: row;
    width: auto;
    margin-bottom: 0;
    gap: var(--padding-md); /* Retorna gap horizontal */
  }
  .user-actions-area {
    /* width: auto; Já é auto */
    margin-left: var(--padding-lg); /* Espaço antes das ações do usuário */
  }
  .user-navigation {
    flex-direction: row;
    width: auto;
    margin-bottom: 0;
    justify-content: flex-end;
    gap: var(--padding-sm);
  }
  .main-navigation a,
  .user-navigation a,
  .user-navigation .user-greeting,
  .user-navigation .logout-button {
    width: auto;
    padding: var(--padding-sm) var(--padding-md);
    border-bottom: none;
    border-radius: var(--border-radius-sm);
  }
  .main-content {
    padding: 0 var(--desktop-padding);
    margin-top: 30px;
    margin-bottom: 30px;
  }
}

@media (min-width: 992px) {
  .project-name {
    font-size: 1.7em;
  }
  .main-navigation a,
  .user-navigation a,
  .user-navigation .user-greeting,
  .user-navigation .logout-button {
    font-size: 1em;
  }
}

@media (min-width: 1400px) {
  .project-name {
    font-size: 1.8em;
  }
  nav a,
  nav .user-greeting,
  nav .logout-button {
    padding: 10px 16px;
  }
}
@media (min-width: 1600px) {
  .project-name {
    font-size: 1.9em;
  }
}
</style>
