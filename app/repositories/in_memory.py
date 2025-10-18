from app.schemas.items import ItemCreate, ItemRead, ItemUpdate


class InMemoryItemRepository:
    """In-memory repository for demo and tests."""

    def __init__(self) -> None:
        self._db: list[ItemRead] = []
        self._seq = 1

    def list_items(self) -> list[ItemRead]:
        return list(self._db)

    def get_item(self, item_id: int) -> ItemRead | None:
        return next((i for i in self._db if i.id == item_id), None)

    def create_item(self, data: ItemCreate) -> ItemRead:
        item = ItemRead(id=self._seq, **data.model_dump())
        self._seq += 1
        self._db.append(item)
        return item

    def delete_item(self, item_id: int) -> bool:
        item = self.get_item(item_id)
        if not item:
            return False
        self._db = [i for i in self._db if i.id != item_id]
        return True

    def update_item(self, item_id: int, data: ItemUpdate) -> bool:
        for idx, item in enumerate(self._db):
            if item.id == item_id:
                updated = item.model_copy(update=data.model_dump(exclude_unset=True))
                self._db[idx] = updated
                return True
        return False
