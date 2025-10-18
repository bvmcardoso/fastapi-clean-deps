from fastapi import FastAPI

from app.api.v1.items.router import router as items_router

app = FastAPI(title="FastAPI Clean Deps")


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello, Clean Deps"}


# v1 routes
app.include_router(items_router, prefix="/api/v1")
