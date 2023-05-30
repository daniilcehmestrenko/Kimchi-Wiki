from asyncpg import Pool, Record
from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    async def get(self, *args, **kwargs):
        pass

    @abstractmethod
    async def create(self, *args, **kwargs):
        pass

    @abstractmethod
    async def delete(self, *args, **kwargs):
        pass


class RecordRepository(AbstractRepository):
    async def delete(self, pool: Pool, record_id: int):
        query = 'DELETE FROM records WHERE id = $1'
        return await pool.execute(query, record_id)

    async def create(self, pool: Pool, *args):
        query = 'INSERT INTO records(folder_id, title, text) ' \
                'VALUES ($1, $2, $3)'
        return await pool.execute(query, *args)

    async def get(self, pool: Pool, record_id: int) -> Record:
        query = 'SELECT * FROM records WHERE id = $1'
        return await pool.fetchrow(query, record_id)

    async def update_title(self, pool: Pool, title: str, id: int):
        query = 'UPDATE records ' \
                'SET title=$1 ' \
                'WHERE id=$2'
        return await pool.execute(query, title, id)

    async def update_text(self, pool: Pool, text: str, record_id: int):
        query = 'UPDATE records ' \
                'SET text=$1 ' \
                'WHERE id=$2'
        return await pool.execute(query, text, record_id)
