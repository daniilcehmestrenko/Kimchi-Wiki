from pydantic import BaseModel


class FolderGET(BaseModel):
    id: int
    title: str
    user_id: int


class FolderPOST(BaseModel):
    title: str
    user_id: int


class RecordGET(BaseModel):
    id: int
    title: str
    text: str
    folder_id: int


class RecordPOST(BaseModel):
    title: str
    text: str
    folder_id: int
