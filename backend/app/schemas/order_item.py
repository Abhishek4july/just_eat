from pydantic import BaseModel, ConfigDict

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int


class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    price: float
    menu_item_name: str

    model_config = ConfigDict(from_attributes=True)