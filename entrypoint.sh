#!/bin/sh

# Executa as migrações do banco de dados
poetry run alembic -c alembic_postgresql.ini upgrade head

# Inicia a aplicação
poetry run uvicorn --host 0.0.0.0 --port 8000 madr.app:app