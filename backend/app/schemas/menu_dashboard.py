from pydantic import BaseModel


class TopMenuItemResponse(BaseModel):
    id: int
    name: str
    order_count: int

    class Config:
        from_attributes = True