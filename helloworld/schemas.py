from typing import Optional

from pydantic import BaseModel


class ItemSchema(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None
