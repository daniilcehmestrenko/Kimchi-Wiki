from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    id: int
    first_name: str
    second_name: str
    email: str
    password: str
    dttm_created: datetime
