from datetime import datetime
from pydantic import BaseModel,ConfigDict
from typing import Optional

class RestaurantCreate(BaseModel):
    name: str
    description: str
    address: str
    city: str
    state: str
    cuisine: str
    phone: str


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    cuisine: Optional[str] = None
    phone: Optional[str] = None

class RestaurantResponse(BaseModel):
    id: int
    name: str
    description: str
    address: str
    city: str
    state: str
    cuisine: str
    phone: str
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)