from pydantic import BaseModel


class PreferenceRequest(BaseModel):
    favorite_cuisine: str | None = None
    dietary_restriction: str | None = None


class PreferenceResponse(BaseModel):
    id: int
    favorite_cuisine: str | None
    dietary_restriction: str | None

    class Config:
        from_attributes = True