from asyncpg import Pool
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


class FolderRepository(AbstractRepository):
    async def delete(self, pool: Pool, folder_id: int):
        query = 'DELETE FROM folders WHERE id = $1'
        return await pool.execute(query, folder_id)

    async def create(self, pool: Pool, **kwargs):
        query = 'INSERT INTO folders(title, user_id) ' \
                'VALUES ($1, $2)'
        return await pool.execute(
            query,
            kwargs.get('title'),
            kwargs.get('user_id')
        )

    async def get_user_folders(self, pool: Pool, user_id: int):
        query = 'SELECT * FROM folders WHERE user_id=$1'
        return await pool.fetch(query, user_id)

    async def get(self, pool: Pool, folder_id: int):
        query = 'SELECT * FROM folders WHERE id = $1'
        return await pool.fetchrow(query, folder_id)

    async def update_title(self, pool: Pool, id: int, title: str):
        query = 'UPDATE folders ' \
                'SET title=$2 ' \
                'WHERE id=$1'
        return await pool.execute(query, id, title)
