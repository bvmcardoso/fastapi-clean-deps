from functools import lru_cache

from app.repositories.in_memory import InMemoryItemRepository
from app.services.items import ItemService


@lru_cache
def get_item_repo() -> InMemoryItemRepository:
    # Returns the concrete implementation
    return InMemoryItemRepository()


@lru_cache
def get_item_service() -> ItemService:
    return ItemService(repo=get_item_repo())
