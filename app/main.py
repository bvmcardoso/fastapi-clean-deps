from fastapi import FastAPI

from app.api.v1.items.router import router as items_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FastAPI Clean Deps")

origins = ["http://localhost:5173", "http://localhost:5174"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # only this origin is allowed
    allow_credentials=True,
    allow_methods=["*"],  # or restrict to specific methods like ["GET", "POST"]
    allow_headers=["*"],  # or restrict to specific headers if needed
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello, Clean Deps"}


# v1 routes
app.include_router(items_router, prefix="/api/v1")
