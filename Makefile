.PHONY: help install sync run dev test clean db-up db-down db-restart shell

help: ## Lista comandos disponíveis
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

install: ## Instala dependências (alias para sync)
	uv sync

sync: ## Sincroniza dependências com uv.lock
	uv sync

run: ## Roda a API (FastAPI/Uvicorn)
	uv run uvicorn main:app --reload

dev: db-up run ## Sobe DB e roda a API

test: clean ## Roda testes
	uv run pytest --cache-clear

clean: ## Remove caches Python e pytest
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache .ruff_cache

db-up: ## Sobe o Postgres no Docker
	docker compose up -d postgres

db-down: ## Para o Postgres
	docker compose stop postgres

db-restart: ## Reinicia o Postgres
	docker compose restart postgres

shell: ## Abre shell Python no ambiente do projeto
	uv run python
