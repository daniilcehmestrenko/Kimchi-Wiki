from pydantic import BaseModel, EmailStr, validator


class UserCreate(BaseModel):
    first_name: str
    second_name: str
    email: EmailStr
    password: str

    @validator('password')
    def password_validator(cls, value: str):
        return value


class UserAuthData(BaseModel):
    email: str
    password: str
