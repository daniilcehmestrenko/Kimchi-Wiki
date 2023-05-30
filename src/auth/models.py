from datetime import datetime
from dataclasses import dataclass


@dataclass
class User:
    id: int
    first_name: str
    second_name: str
    email: str
    password: str
    dttm_created: datetime
