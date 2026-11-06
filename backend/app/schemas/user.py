from pydantic import BaseModel


class UpdateProfile(BaseModel):
    username: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True


class ChangePassword(BaseModel):
    current_password: str
    new_password: str