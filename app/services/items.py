from fastapi import HTTPException, status

from app.repositories.protocol import ItemRepository
from app.schemas.items import ItemCreate, ItemRead, ItemUpdate


class ItemService:
    """Application/business layer. Holds validations and policies."""

    def __init__(self, repo: ItemRepository) -> None:
        self.repo = repo

    def list_items(self) -> list[ItemRead]:
        return self.repo.list_items()

    def get_item(self, item_id: int) -> ItemRead | None:
        item = self.repo.get_item(item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return item

    def create_item(self, data: ItemCreate) -> ItemRead:
        # Example rule: unique name (case-insensitive)
        existing = [i for i in self.repo.list_items() if i.name.lower() == data.name.lower()]
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Name already exists.")
        return self.repo.create_item(data)

    def update_item(self, item_id: int, data: ItemUpdate) -> None:
        ok = self.repo.update_item(item_id, data)
        if not ok:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    def delete_item(self, item_id: int) -> None:
        ok = self.repo.delete_item(item_id)
        if not ok:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
