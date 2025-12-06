from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True

