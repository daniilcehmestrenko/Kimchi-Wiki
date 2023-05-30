from datetime import datetime
from dataclasses import dataclass


@dataclass
class Folder:
    id: int
    title: str
    user_id: int
    dttm_created: datetime
