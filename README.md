# CRUD Template

<p align="justify">
Este projeto é um template completo para aplicações CRUD (Create, Read, Update, Delete), utilizando uma stack moderna com Vue.js no frontend e FastAPI no backend. A estrutura é modular e pronta para ser adaptada a diferentes domínios de negócio.
</p>

---

## 🚀 Tecnologias

### Backend
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)  
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)  
![Pydantic](https://img.shields.io/badge/Pydantic-2A6EBB?style=for-the-badge&logo=pydantic&logoColor=white)  
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-FF281F?style=for-the-badge&logo=sqlalchemy&logoColor=white)  
![Alembic](https://img.shields.io/badge/Alembic-000000?style=for-the-badge&logo=alembic&logoColor=white)  
![Uvicorn](https://img.shields.io/badge/Uvicorn-222222?style=for-the-badge&logo=uvicorn&logoColor=white)  
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)  

### Frontend
![Vue.js](https://img.shields.io/badge/Vue.js-42B883?style=for-the-badge&logo=vue.js&logoColor=white)  
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)  
![Pinia](https://img.shields.io/badge/Pinia-FADA5E?style=for-the-badge&logo=pinia&logoColor=black)  
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)  
![Axios](https://img.shields.io/badge/Axios-5A29E4?style=for-the-badge&logo=axios&logoColor=white)  

### DevOps & Outros
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)  
![Docker Compose](https://img.shields.io/badge/Docker--Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)  
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)  


---

## 📁 Estrutura do Projeto


    crud-template/
    ├── backend/
    │   ├── app/
    │   │   ├── api/
    │   │   ├── core/
    │   │   ├── models/
    │   │   ├── schemas/
    │   │   └── main.py
    |   ├── tests/
    │   └── Dockerfile
    ├── frontend/
    │   ├── src/
    │   │   ├── components/
    │   │   ├── views/
    │   │   ├── store/
    │   │   └── main.ts
    │   └── Dockerfile
    ├── docker-compose.yml
    ├── .env
    └── README.md

---

## 🚀 Como Executar

Pré-requisitos

    Docker instalado

    Docker Compose instalado

Clone o repositório:

    git clone https://github.com/Eng-Soft-Claudio/CRUD-Template.git
    
    cd CRUD-Template

Inicie os containers:

    docker-compose up --build

Acesse a aplicação:

    Frontend: http://localhost:3000
        
    API (Swagger): http://localhost:8000/docs

---

## 📦 Funcionalidades

    Operações CRUD completas

    Validação de dados no backend com Pydantic

    Gerenciamento de estado global com Pinia

    Comunicação entre frontend e backend via Axios

    Documentação automática da API com Swagger

    Ambiente de desenvolvimento isolado com Docker

---

## 🛠️ Personalização

    Para alterar o banco de dados, modifique as configurações em backend/app/core/config.py.

    Para adicionar novas rotas ou modelos, edite os arquivos em backend/app/api/ e backend/app/models/.

    No frontend, novas páginas podem ser adicionadas em frontend/src/views/ e componentes reutilizáveis em frontend/src/components/.

---

## 📄 Licença 🧰

Direitos Autorais 2025 Cláudio de Lima Tosta
<p align="justify">
É concedida permissão, gratuita, a qualquer pessoa que obtenha uma cópia deste software e dos arquivos de documentação associados (o "Software"), para lidar com o Software sem restrições, incluindo, entre outras, os direitos de usar, copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias do Software, e para permitir que as pessoas a quem o Software é fornecido o façam, sujeito às seguintes condições:
</p>
<p align="justify">
O aviso de direitos autorais acima e este aviso de permissão devem ser incluídos em todas as cópias ou partes substanciais do Software.
</p>
<p align="justify">
O SOFTWARE É FORNECIDO "NO ESTADO EM QUE SE ENCONTRA", SEM GARANTIA DE QUALQUER TIPO, EXPRESSA OU IMPLÍCITA, INCLUINDO, MAS NÃO SE LIMITANDO ÀS GARANTIAS DE COMERCIALIZAÇÃO, ADEQUAÇÃO A UM DETERMINADO FIM E NÃO VIOLAÇÃO. EM NENHUMA HIPÓTESE OS AUTORES OU TITULARES DOS DIREITOS AUTORAIS SERÃO RESPONSÁVEIS POR QUALQUER RECLAMAÇÃO, DANOS OU OUTRA RESPONSABILIDADE, SEJA EM UMA AÇÃO CONTRATUAL, ATO ILÍCITO OU DE OUTRA FORMA, DECORRENTE DE, DE OU EM CONEXÃO COM O SOFTWARE OU O USO OU OUTRAS NEGOCIAÇÕES NO SOFTWARE.
</p>
