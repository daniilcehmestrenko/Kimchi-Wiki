from datetime import datetime
from dataclasses import dataclass


@dataclass
class Record:
    id: int
    folder_id: int
    title: str
    text: str
    dttm_created: datetime
    dttm_change: datetime
