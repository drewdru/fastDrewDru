from typing import Optional

from fastapi import APIRouter, Body, Path, Query

from helloworld.schemas import Item

helloworld = APIRouter()


@helloworld.get(
    "/",
    responses={
        200: {
            "description": "Return Hello World.",
        }
    },
)
async def read_root() -> dict:
    """Hello world"""
    return {"Hello": "World"}


@helloworld.get(
    "/items/{item_id}",
    responses={
        200: {
            "description": "Item Data.",
        }
    },
)
async def read_item(
    item_id: int = Path(None, title="Item ID", description="Item Identifier"),
    q: Optional[str] = Query(
        None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
    ),
) -> dict:
    """Get Item"""
    return {"item_id": item_id, "q": q}


@helloworld.put(
    "/items/{item_id}",
    status_code=201,
    responses={
        201: {
            "description": "Item Data.",
        }
    },
)
async def update_item(
    item_id: int = Path(None, title="Item ID", description="Item Identifier"),
    item: Item = Body(
        None,
        title="Item",
        description="New Item Data",
    ),
) -> dict:
    """Update Item"""
    return {"item_name": item.name, "item_id": item_id}
