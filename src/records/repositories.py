from asyncpg.pool import Pool
from abstracts import AbstractRepository

from .schemas import FolderPOST, RecordPOST


class FolderRepository(AbstractRepository):
    async def get_folders(self, pool: Pool, user_id: int):
        query = 'SELECT * FROM folders ' \
                'WHERE user_id = $1'
        return await pool.fetch(query, user_id)

    async def create(self, pool: Pool, folder: FolderPOST, user_id: int):
        query = 'INSERT INTO folders(title, user_id) ' \
                'VALUES ($1, $2)'
        return await pool.execute(query, folder.title, folder.user_id)


class RecordRepository(AbstractRepository):
    async def get_records(self, pool: Pool, folder_id: int):
        query = 'SELECT * FROM records ' \
                'WHERE folder_id = $1'
        return await pool.fetch(query, folder_id)

    async def create(self, pool: Pool, record: RecordPOST, folder_id: int):
        query = 'INSERT INTO records(title, text, folder_id) ' \
                'VALUES ($1, $2, $3)'
        return await pool.execute(
            query,
            record.title,
            record.text,
            folder_id
        )
