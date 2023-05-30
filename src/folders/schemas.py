from pydantic import BaseModel


class FolderCreate(BaseModel):
    title: str
    user_id: int


class UserId(BaseModel):
    user_id: int
