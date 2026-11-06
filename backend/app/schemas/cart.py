from pydantic import BaseModel,Field


class AddCartItem(BaseModel):
    menu_item_id: int
    quantity: int = 1


class UpdateCartItem(BaseModel):
   quantity: int = Field(gt=0)

class CartItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int

    class Config:
        from_attributes = True