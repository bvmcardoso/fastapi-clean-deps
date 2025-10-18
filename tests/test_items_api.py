import json

from fastapi import status
from fastapi.testclient import TestClient

from app.api.deps import get_items_service_dep
from app.main import app
from app.repositories.in_memory import InMemoryItemRepository
from app.schemas.items import ItemCreate
from app.services.items import ItemService


def make_test_service() -> ItemService:
    repo = InMemoryItemRepository()
    repo.create_item(ItemCreate(name="Keyboard", description="Mechanical"))
    repo.create_item(ItemCreate(name="Mouse", description="Wireless"))
    return ItemService(repo=repo)


def test_items_crud_flow_v1():
    # Single instance for the unit test
    service = make_test_service()
    app.dependency_overrides[get_items_service_dep] = lambda: service

    with TestClient(app) as client:
        # Read all - List of Items
        response_list = client.get("/api/v1/items/")
        items = response_list.json()
        assert response_list.status_code == status.HTTP_200_OK
        assert len(items) == 2
        assert [item["name"] for item in items] == ["Keyboard", "Mouse"]
        assert [item["description"] for item in items] == ["Mechanical", "Wireless"]

        # Create - New item
        response_create = client.post(
            "/api/v1/items/", json={"name": "Headset", "description": "USB-C"}
        )
        created_item = response_create.json()

        assert response_create.status_code == status.HTTP_201_CREATED

        assert created_item["id"] == 3
        assert created_item["name"] == "Headset"
        assert created_item["description"] == "USB-C"

        # Read - Single Item
        response_read = client.get(f"/api/v1/items/{created_item['id']}")
        assert response_read.status_code == status.HTTP_200_OK
        assert response_read.json()["id"] == 3
        assert response_read.json()["name"] == "Headset"
        assert response_read.json()["description"] == "USB-C"

        # Delete
        response_delete = client.delete(f"/api/v1/items/{created_item['id']}")
        assert response_delete.status_code == status.HTTP_204_NO_CONTENT

        # Update
        first_item_id = items[0]["id"]

        new_item_information = {
            "name": "New item info",
            "description": "New item description",
        }
        response_update = client.patch(
            f"api/v1/items/{first_item_id}", data=json.dumps(new_item_information)
        )

        updated_item = response_update.json()
        assert updated_item["id"] == first_item_id
        assert updated_item["name"] == new_item_information["name"]
        assert updated_item["description"] == new_item_information["description"]

        # cleanup
        app.dependency_overrides.clear()
