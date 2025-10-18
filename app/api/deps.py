from fastapi import Depends

from app.core.container import get_item_service
from app.services.items import ItemService


def get_items_service_dep(
    service: ItemService = Depends(get_item_service),
) -> ItemService:
    """Wraps the container provider to make it easier to override the entire service
    during test instead of just the repository layer"""
    return service
