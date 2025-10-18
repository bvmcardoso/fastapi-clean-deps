# FastAPI Clean Deps

Clean Architecture with FastAPI - layers API → Service → Repository, dependency injection via Depends, and isolated tests using dependency_overrides.

## Developer Experience

```bash
make setup-local        # install all dependencies (including dev tools)
make setup-prod         # install only production dependencies
make run                # run the FastAPI app with auto-reload
make test               # execute the test suite
make lint               # check code style with ruff
make format-and-fix     # format code and fix lint issues
make typecheck          # static type checking with mypy
make check              # full quality gate (format, lint, typecheck, test)
make help               # list available commands
```

Application: http://127.0.0.1:8000/
Docs: http://127.0.0.1:8000/docs

## Project Structure

```
app/
  api/
    deps.py             # dependency providers for routes
    v1/
      items/
        router.py       # CRUD endpoints for items
  core/
    container.py        # dependency injection wiring
  repositories/
    protocol.py         # abstract repository contract (Protocol)
    in_memory.py        # in-memory implementation for testing
  schemas/
    items.py            # Pydantic DTOs (ItemCreate, ItemRead, ItemUpdate)
  services/
    items.py            # business rules and validations
  main.py               # FastAPI app entry point
tests/
  conftest.py           # shared test configuration
  test_healthcheck.py   # root endpoint sanity test
  test_items_api.py     # full CRUD flow tests for items
Makefile                # developer tasks (uv + ruff + mypy + pytest)
pyproject.toml          # project and tool configuration
pytest.ini              # pytest overrides
uv.lock                 # uv dependency lockfile
LICENSE                 # license
README.md               # documentation
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
