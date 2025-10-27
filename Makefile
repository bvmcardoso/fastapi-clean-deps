# Clean, minimal Makefile for FastAPI + uv + pytest + ruff + mypy + docker-compose

UV    ?= uv
RUN   ?= $(UV) run
APP   ?= app
TESTS ?= tests
HOST  ?= 0.0.0.0
PORT  ?= 8000

.DEFAULT_GOAL := help
.PHONY: help setup-local setup-prod run test lint format-and-fix typecheck check \
        up down logs logs-db ps migrate reset-db

help: ## Show available commands
	@awk 'BEGIN{FS=":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# ---------------------------------------
# Dev Environment
# ---------------------------------------

setup-local: ## Sync dependencies for software engineers
	$(UV) sync --group dev

setup-prod: ## Sync dependencies for production
	$(UV) sync --frozen

run: ## Run FastAPI app with auto-reload (local)
	$(RUN) uvicorn $(APP).main:app --reload --host $(HOST) --port $(PORT)

# ---------------------------------------
# Quality
# ---------------------------------------

test: ## Run all tests
	PYTHONPATH=. $(RUN) pytest

lint: ## Check code style
	$(RUN) ruff check $(APP) $(TESTS)

format-and-fix: ## Format code automatically and fix errors
	$(RUN) ruff format $(APP) $(TESTS)
	$(RUN) ruff check --fix $(APP) $(TESTS)

typecheck: ## Static type checking
	$(RUN) mypy $(APP)

check: ## Full quality gate (format + lint + typecheck + tests)
	$(MAKE) format-and-fix
	$(MAKE) lint
	$(MAKE) typecheck
	$(MAKE) test

# ---------------------------------------
# Docker / Infra
# ---------------------------------------

up: ## Start all containers in detached mode
	docker compose up -d

down: ## Stop and remove all containers, networks and volumes
	docker compose down -v

logs: ## Tail logs of the API container
	docker compose logs -f api

logs-db: ## Tail logs of the DB container
	docker compose logs -f db

ps: ## List running containers
	docker compose ps

migrate: ## Run Alembic migrations inside the API container
	docker compose exec api $(RUN) alembic upgrade head

reset-db: ## Drop and recreate the database (dev only)
	docker compose down -v
	docker compose up -d db
	sleep 3
	docker compose exec api $(RUN) alembic upgrade head
