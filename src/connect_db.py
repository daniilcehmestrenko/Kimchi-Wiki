import asyncpg
from asyncpg.pool import Pool
from aiohttp.web_app import Application

from config import DB_KEY


class ConnectDb:
    '''
    Класс создает пул подключений к бд
    '''

    async def create_db_pool(self, app: Application):
        pool: Pool = await asyncpg.create_pool(
            port=5432,
            user='postgres',
            database='wiki',
            password=123,
            max_size=6,
            min_size=6
        )
        app[DB_KEY] = pool

    async def destroy_db_pool(self, app: Application):
        pool: Pool = app[DB_KEY]
        await pool.close()
