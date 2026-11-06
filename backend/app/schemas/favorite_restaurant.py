from pydantic import BaseModel

from app.schemas.restaurant import RestaurantResponse


class FavoriteRestaurantResponse(BaseModel):
    id: int
    restaurant: RestaurantResponse

    class Config:
        from_attributes = True