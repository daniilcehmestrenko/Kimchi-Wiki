from asyncpg import Pool, Record
from abc import ABC, abstractmethod
from typing import List


class AbstractManager(ABC):

    @classmethod
    @abstractmethod
    async def get(cls, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    async def create(cls, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    async def delete(cls, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    async def update(cls, *args, **kwargs):
        pass


class UserManager(AbstractManager):

    @classmethod
    async def get(cls, pool: Pool, user_id: int) -> Record:
        query = 'SELECT * FROM users WHERE id = $1'
        return await pool.fetchrow(query, user_id)

    @classmethod
    async def all(cls, pool: Pool) -> List[Record]:
        query = 'SELECT * FROM user'
        return await pool.fetch(query)
