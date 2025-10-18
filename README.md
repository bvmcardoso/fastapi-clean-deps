# FastAPI Clean Deps


Clean Architecture with **FastAPI Dependencies** — layers **API → Service → Repository**, dependency injection via `Depends`, and **isolated tests** using `dependency_overrides`.


## ⚡ Developer Experience (DX)


```bash
make setup # install dependencies via uv
make run # run the app in dev mode
make test # run the test suite
```


Open: http://127.0.0.1:8000/
Docs: http://127.0.0.1:8000/docs


> If you don't use `uv`, export a `requirements.txt` with `make export-reqs` and then `pip install -r requirements.txt`.


## Structure
```
app/
api/ # routers and API dependencies
services/ # business/application layer
repositories/ # contracts and data access implementations
schemas/ # Pydantic contracts (input/output)
core/ # container (dependency wiring)
main.py # FastAPI application
```


## Core idea
- The API injects **Services** via `Depends` (DIP in practice).
- Services talk to **Repositories** through a **Protocol** (abstraction), not a concrete impl.
- In tests, swap providers with `app.dependency_overrides`.


---


## Roadmap
- `feature/sqlalchemy-adapter` (DB-backed repository)
- `feature/async` (async-first layer)
- `feature/redis-cache` (cross-cutting cache)
- `feature/ci` (pipelines: lint + typecheck + test)
