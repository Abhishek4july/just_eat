from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
class MenuItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    is_special: bool = False
    special_title: Optional[str] = None



class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    is_special: Optional[bool] = None
    special_title: Optional[str] = None


class MenuItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    category: str
    is_special: bool
    special_title: Optional[str] = None
    order_count: int
    restaurant_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)