from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime
from repositories import UserManager, AbstractManager


class AbstractEntity(ABC):
    manager = AbstractManager

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)

    @abstractmethod
    async def save(self, *args, **kwargs):
        pass

    @abstractmethod
    async def delete(self, *args, **kwargs):
        pass


class User(AbstractEntity):
    id: Optional[int]
    first_name: str
    second_name: str
    email: str
    password: str
    dttm_created: datetime

    manager = UserManager

    async def save(self):
        return await self.manager.create(self.__dict__)

    async def delete(self, *args, **kwargs):
        return await self.manager.delete(*args, **kwargs)


class Folder(AbstractEntity):
    id: Optional[int]
    title: str
    record_id: int
    dttm_created: datetime

    manager = UserManager

    async def save(self):
        return await self.manager.create(self.__dict__)

    async def delete(self, *args, **kwargs):
        return await self.manager.delete(*args, **kwargs)


class Record(AbstractEntity):
    id: Optional[int]
    folder_id: int
    title: str
    text: str
    dttm_created: datetime
    dttm_change: datetime

    manager = UserManager

    async def save(self):
        return await self.manager.create(self.__dict__)

    async def delete(self, *args, **kwargs):
        return await self.manager.delete(*args, **kwargs)
