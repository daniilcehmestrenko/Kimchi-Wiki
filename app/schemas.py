from pydantic import BaseModel, EmailStr, validator


class UserCreate(BaseModel):
    first_name: str
    second_name: str
    email: EmailStr
    password: str

    @validator('password')
    def password_validator(cls, value: str):
        return value


class UserUpdate(BaseModel):
    first_name: str
    second_name: str
    email: EmailStr


class UserPassword(BaseModel):
    password: str

    @validator('password')
    def password_validator(cls, value: str):
        return value


class UserId(BaseModel):
    user_id: int


class UserAuthData(BaseModel):
    email: EmailStr
    password: str


class FolderCreate(BaseModel):
    title: str
    user_id: int
