<template>
  <div class="view-card-container about-view-layout">
    <header class="about-header">
      <h1>Sobre o Projeto CRUD Template</h1>
      <p class="subtitle">Uma base robusta para iniciar seus projetos com autenticação e gerenciamento de usuários.</p>
    </header>

    <section class="about-section">
      <h2>Objetivo</h2>
      <p class="objective-text">
        Este projeto foi desenvolvido para se tornar um template para acelerar o desenvolvimento de novas aplicações
        que requerem funcionalidades de CRUD (Create, Read, Update, Delete) à um sistema completo de gerenciamento
        ao acesso de usuários. O objetivo principal é fornecer uma fundação sólida, segura e fácil de expandir, economizando
        tempo de desenvolvimento ao evitar a necessidade de reescrever código repetitivo para autenticação,
        autorização e operações básicas de usuário, tanto para usuários comuns quanto para administradores.
      </p>
    </section>

    <section class="about-section">
      <h2>Tecnologias Utilizadas</h2>
      <div class="tech-grid">
        <div class="tech-card">
          <h3>Backend</h3>
          <ul>
            <li><strong>Python 3.12+</strong></li>
            <li><strong>FastAPI</strong></li>
            <li><strong>SQLAlchemy & Alembic</strong></li>
            <li><strong>Pydantic</strong></li>
            <li><strong>Passlib & python-jose</strong></li>
            <li><strong>PostgreSQL</strong></li>
            <li><strong>Pytest</strong></li>
          </ul>
        </div>
        <div class="tech-card">
          <h3>Frontend</h3>
          <ul>
            <li><strong>Vue.js 3 (Composition API)</strong></li>
            <li><strong>TypeScript</strong></li>
            <li><strong>Vite</strong></li>
            <li><strong>Pinia & Vue Router</strong></li>
            <li><strong>VeeValidate & Yup</strong></li>
            <li><strong>Vue-Toastification</strong></li>
          </ul>
        </div>
        <div class="tech-card">
          <h3>DevOps & Infraestrutura</h3>
          <ul>
            <li><strong>Docker & Docker Compose</strong></li>
            <li><strong>ESLint / Linters</strong></li>
          </ul>
        </div>
      </div>
    </section>

    <section class="about-section">
      <h2>Funcionalidades Implementadas</h2>
      <h3>Usuário Comum:</h3>
      <ul>
        <li>Registro, Login e Logout (JWT)</li>
        <li>Visualização e Edição do próprio perfil</li>
        <li>Alteração da própria senha</li>
        <li>Recuperação de senha</li>
        <li>Deleção da própria conta</li>
      </ul>
      <h3 class="features-subtitle">Funcionalidades de Administrador:</h3>
      <ul>
        <li>Listagem de todos os usuários</li>
        <li>Criação de novos usuários</li>
        <li>Edição completa de usuários (incluindo status e permissões)</li>
        <li>Deleção de usuários</li>
      </ul>
    </section>

    <section class="about-section contact-info">
      <h2>Contato e Repositório</h2>
      <p>
        Feedback e sugestões são sempre bem-vindos.
        <a href="https://github.com/Eng-Soft-Claudio/CRUD-Template" target="_blank" rel="noopener noreferrer" class="btn btn-accent btn-inline">
          Visite o Repositório no GitHub
        </a>
      </p>
    </section>
  </div>
</template>

<style scoped>
.about-view-layout {
  max-width: 900px;
  margin: var(--padding-xl) auto;
}
.about-header {
  text-align: center;
  margin-bottom: var(--padding-xl);
  padding-bottom: var(--padding-lg);
  border-bottom: 1px solid var(--color-border);
}
.about-header h1 {
  font-size: 2.2em;
  color: var(--color-brand-primary);
  margin-bottom: var(--padding-sm);
}
.subtitle {
  font-size: 1.1em;
  color: var(--color-text-on-light-secondary);
  font-family: var(--font-sans-ui);
}
.about-section {
  margin-bottom: var(--padding-xl);
}
.about-section h2 {
  font-size: 1.6em;
  color: var(--color-text-on-light-primary);
  margin-bottom: var(--padding-md);
  padding-bottom: var(--padding-sm);
  border-bottom: 2px solid var(--color-brand-secondary);
  display: inline-block;
}
.about-section h3 {
  font-size: 1.25em;
  font-family: var(--font-sans-ui);
  font-weight: 600;
  color: var(--color-text-on-light-primary);
  margin-top: var(--padding-lg);
  margin-bottom: var(--padding-sm);
}
.features-subtitle {
  margin-top: var(--padding-lg);
}
.objective-text,
.about-section p,
.about-section ul {
  font-size: 1rem;
  color: var(--color-text-on-light-secondary);
  margin-bottom: var(--padding-md);
  text-align: justify;
}
.about-section ul {
  list-style-position: inside;
  padding-left: 0;
}
.about-section ul li {
  margin-bottom: var(--padding-xs);
}
.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: var(--padding-lg);
  margin-top: var(--padding-md);
}
.tech-card {
  background-color: var(--color-bg-page);
  padding: var(--padding-lg);
  border-radius: var(--border-radius-md);
  border: 1px solid var(--color-border);
}
.tech-card h3 {
  margin-top: 0;
  font-size: 1.15em;
  color: var(--color-brand-primary);
  border-bottom: none;
  padding-bottom: 0;
  margin-bottom: var(--padding-md);
}
.tech-card ul {
  font-size: 0.95rem;
  padding-left: var(--padding-md);
}
.contact-info {
  text-align: center;
  padding-top: var(--padding-lg);
  border-top: 1px solid var(--color-border);
}
.contact-info p {
  text-align: center;
}
.btn.btn-inline {
  margin-left: var(--padding-sm);
}
</style>