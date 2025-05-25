#!/bin/sh

# =======================================================================================================
# --- Script de Entrypoint para o Backend ---                                                       #####
# =======================================================================================================

# Este script é executado quando o container do backend é iniciado.
# Ele é responsável por aplicar as migrações do banco de dados e iniciar o servidor da aplicação.

# =======================================================================================================
# --- Aplicar Migrações do Banco de Dados ---                                                       #####
# =======================================================================================================
echo "Applying database migrations..."
alembic upgrade head

# =======================================================================================================
# --- Iniciar Servidor da Aplicação ---                                                             #####
# =======================================================================================================
echo "Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
