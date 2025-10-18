from fastapi import APIRouter, Depends, status

from app.api.deps import get_items_service_dep
from app.schemas.items import ItemCreate, ItemRead, ItemUpdate
from app.services.items import ItemService

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[ItemRead])
def list_items(service: ItemService = Depends(get_items_service_dep)):
    return service.list_items()


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, service: ItemService = Depends(get_items_service_dep)):
    return service.get_item(item_id)


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, service: ItemService = Depends(get_items_service_dep)):
    return service.create_item(payload)


@router.patch("/{item_id}", response_model=ItemRead, status_code=status.HTTP_200_OK)
def update_item(
    item_id: int,
    data: ItemUpdate,
    service: ItemService = Depends(get_items_service_dep),
):
    service.update_item(item_id, data)
    return service.get_item(item_id)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, service: ItemService = Depends(get_items_service_dep)):
    service.delete_item(item_id)
    return None
