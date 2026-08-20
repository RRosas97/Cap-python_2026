from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):

    id: int = Field(gt=0)
    username: str = Field(min_length=1, max_length=100)
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w{2,}$")


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)


class UserOut(BaseModel):
    id: int
    username: str
    email: str

    model_config = {"from_attributes": True}
