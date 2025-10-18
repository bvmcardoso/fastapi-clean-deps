# Clean, minimal Makefile for FastAPI + uv + pytest + ruff + mypy

UV    ?= uv
RUN   ?= $(UV) run
APP   ?= app
TESTS ?= tests
HOST  ?= 0.0.0.0
PORT  ?= 8000

.DEFAULT_GOAL := help
.PHONY: help setup run test lint format typecheck check

help: ## Show available commands
	@awk 'BEGIN{FS=":.*##"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup-local: ## Sync dependencies for software engineers
	$(UV) sync --group dev

setup-prod: ## Sync dependencies for production
	$(UV) sync

run: ## Run FastAPI app with auto-reload
	$(RUN) uvicorn $(APP).main:app --reload --host $(HOST) --port $(PORT)

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
