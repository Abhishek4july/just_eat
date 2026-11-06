from pydantic import BaseModel

class FavoriteResponse(BaseModel):
    id: int
    menu_item_id: int

    class Config:
        from_attributes = True