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


@dataclass
class Folder:
    id: int
    title: str
    user_id: int
    dttm_created: datetime


@dataclass
class Record:
    id: int
    folder_id: int
    title: str
    text: str
    dttm_created: datetime
    dttm_change: datetime
