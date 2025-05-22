<script setup lang="ts">
// Nenhuma lógica de script específica é necessária para esta página estática por enquanto
</script>

<template>
  <div class="about-container">
    <header class="about-header">
      <h1>Sobre o Projeto CRUD Template</h1>
      <p class="subtitle">Uma base robusta para iniciar seus projetos com autenticação e gerenciamento de usuários.</p>
    </header>

    <section class="about-section">
      <h2>Objetivo</h2>
      <p class="objective">
        Este projeto foi desenvolvido como um template abrangente para acelerar o desenvolvimento de novas aplicações
        que requerem funcionalidades de CRUD (Create, Read, Update, Delete) e um sistema completo de gerenciamento
        de usuários. O objetivo principal é fornecer uma fundação sólida, segura e fácil de expandir, economizando
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
            <li><strong>FastAPI:</strong> Framework web moderno e de alta performance.</li>
            <li><strong>SQLAlchemy:</strong> ORM para interação com o banco de dados.</li>
            <li><strong>Alembic:</strong> Para migrações de banco de dados.</li>
            <li><strong>Pydantic:</strong> Para validação de dados e schemas.</li>
            <li><strong>Passlib & python-jose:</strong> Para hashing de senhas e JWT.</li>
            <li><strong>PostgreSQL:</strong> Banco de dados relacional.</li>
            <li><strong>Uvicorn:</strong> Servidor ASGI.</li>
          </ul>
        </div>
        <div class="tech-card">
          <h3>Frontend</h3>
          <ul>
            <li><strong>Vue.js 3 (Composition API)</strong></li>
            <li><strong>TypeScript:</strong> Para tipagem estática e robustez.</li>
            <li><strong>Vite:</strong> Ferramenta de build e servidor de desenvolvimento rápido.</li>
            <li><strong>Pinia:</strong> Gerenciamento de estado.</li>
            <li><strong>Vue Router:</strong> Para roteamento Single Page Application.</li>
            <li><strong>VeeValidate & Yup:</strong> Para validação de formulários.</li>
            <li><strong>Vue-Toastification:</strong> Para notificações.</li>
            <li><strong>Axios:</strong> Cliente HTTP para chamadas API.</li>
          </ul>
        </div>
        <div class="tech-card">
          <h3>DevOps & Infraestrutura</h3>
          <ul>
            <li><strong>Docker & Docker Compose:</strong> Para conteinerização e orquestração local.</li>
            <li><strong>Linters (ESLint, etc.):</strong> Para qualidade de código.</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="about-section">
      <h2>Funcionalidades Implementadas</h2>
      <h3>Usuário Comum:</h3>
      <ul>
        <li>Registro de conta</li>
        <li>Login e Logout seguro com JWT</li>
        <li>Visualização e Edição do próprio perfil (nome, email)</li>
        <li>Alteração da própria senha</li>
        <li>Recuperação de senha (fluxo "Esqueci Minha Senha")</li>
        <li>Deleção da própria conta</li>
      </ul>
      <h3 class="upcoming-features-title">Próximas Funcionalidades (Administrador):</h3>
      <p class="upcoming-features-note">(Funcionalidades de administrador estão planejadas e serão adicionadas em breve para completar o template.)</p>
      <ul>
        <li>Listar todos os usuários</li>
        <li>Visualizar, criar, editar e deletar usuários (como admin)</li>
        <li>Gerenciar permissões e status de usuários (ativo, superuser)</li>
      </ul>
    </section>

    <section class="about-section contact-section">
      <h2>Contato e Contribuições</h2>
      <p class="contact-contributions">
        Este é um projeto em constante evolução. Feedback e sugestões são sempre bem-vindos.
        Se desejar contribuir ou reportar issues, por favor, visite o repositório do projeto.
        <br/><em>(Nota: Este é um projeto template, adapte esta seção conforme necessário)</em>
      </p>
      <a href="https://github.com/Eng-Soft-Claudio/CRUD-Template" target="_blank" rel="noopener noreferrer" class="btn-repo">Repositório no GitHub</a>
    </section>
  </div>
</template>

<style scoped>
.about-container {
  max-width: 900px;
  margin: 30px auto;
  padding: 20px 30px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: var(--text-color-primary, #2c3e50);
  line-height: 1.7;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 3px 10px rgba(0,0,0,0.07);
}

.about-header {
  text-align: center;
  margin-bottom: 40px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border-color, #ecf0f1);
}

.about-header h1 {
  font-size: 2.5em;
  font-weight: 600;
  color: var(--primary-color, #007bff);
  margin-bottom: 10px;
}

.subtitle {
  font-size: 1.15em;
  color: var(--text-color-secondary, #7f8c8d);
}

.about-section {
  margin-bottom: 40px;
}

.about-section h2 {
  font-size: 1.8em;
  font-weight: 600;
  color: var(--text-color-primary, #34495e);
  margin-bottom: 15px;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--primary-color, #007bff);
  display: inline-block;
}

.about-section h3 {
  font-size: 1.4em;
  font-weight: 500;
  color: var(--text-color-primary);
  margin-top: 25px;
  margin-bottom: 10px;
}

.objective{
  text-align: justify;
}

.upcoming-features-title {
  margin-top: 30px;
}
.upcoming-features-note {
  font-style: italic;
  color: var(--text-color-secondary);
  font-size: 0.95em;
  margin-bottom: 15px;
  text-align: justify;
}
.contact-contributions{
  text-align: justify;
}

.about-section p,
.about-section ul {
  font-size: 1.05em;
  color: var(--text-color-secondary, #555);
  margin-bottom: 15px;
}

.about-section ul {
  list-style: disc;
  padding-left: 25px;
}

.about-section ul li {
  margin-bottom: 8px;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 25px;
  margin-top: 20px;
}

.tech-card {
  background-color: var(--bg-light, #f8f9fa);
  padding: 20px;
  border-radius: 8px;
  border: 1px solid var(--border-color, #e9ecef);
}

.tech-card h3 {
  margin-top: 0;
  color: var(--primary-color);
  border-bottom: none;
  padding-bottom: 0;
  margin-bottom: 12px;
}

.contact-section {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid var(--border-color, #ecf0f1);
}

.btn-repo {
  display: inline-block;
  margin-top: 15px;
  padding: 10px 25px;
  background-color: var(--primary-color, #007bff);
  color: white;
  text-decoration: none;
  border-radius: 5px;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.btn-repo:hover {
  background-color: var(--primary-hover-color, #0056b3);
}
</style>