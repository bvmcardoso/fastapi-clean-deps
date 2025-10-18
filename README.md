# FastAPI Clean Deps

Clean Architecture with FastAPI - layers API → Service → Repository, dependency injection via Depends, and isolated tests using dependency_overrides.

## Developer Experience

```bash
make setup       # install dependencies via uv
make run         # run the app in dev mode
make test        # run the test suite
make lint        # check code style with ruff
make format      # format code automatically
make typecheck   # static type checking with mypy
```

Application: http://127.0.0.1:8000/
Docs: http://127.0.0.1:8000/docs

## Project Structure

```
app/
  api/             # routers and API dependencies
  services/        # business and validation logic
  repositories/    # contracts and data access implementations
  schemas/         # Pydantic DTOs (input/output)
  core/            # container and dependency wiring
  main.py          # FastAPI application entry point
tests/
  test_*.py        # isolated API and service tests
```

## Design Principles

- API injects Services via Depends (Dependency Inversion Principle in practice)
- Services depend on Repository Protocols, not concrete implementations
- Repositories encapsulate infrastructure (in-memory for now, database later)
- Tests override dependencies using app.dependency_overrides for full isolation

## Roadmap

- feature/sqlalchemy-adapter: database-backed repository
- feature/async: async-first layers
- feature/redis-cache: optional caching layer
- feature/ci: lint, typecheck, and test pipelines
