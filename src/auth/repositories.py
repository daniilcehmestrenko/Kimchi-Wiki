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


class UserRepository(AbstractRepository):
    async def delete(self, pool: Pool, user_id: int):
        query = 'DELETE FROM users WHERE id=$1'
        return await pool.execute(query, user_id)

    async def create(self, pool: Pool, **kwargs):
        query = 'INSERT INTO users' \
                '(first_name, second_name, email, password) ' \
                'VALUES ($1, $2, $3, $4)'
        return await pool.execute(
            query,
            kwargs.get('first_name'),
            kwargs.get('second_name'),
            kwargs.get('email'),
            kwargs.get('password')
        )

    async def get_user_info(self, pool: Pool, email: str, password: str):
        query = 'SELECT * FROM users ' \
                'WHERE email=$1 and password=$2'
        return await pool.fetchrow(query, email, password)

    async def get(self, pool: Pool, user_id: int):
        query = 'SELECT * FROM users WHERE id=$1'
        return await pool.fetchrow(query, user_id)

    async def update_first_name(self, pool: Pool, id: int, first_name: str):
        query = 'UPDATE users ' \
                'SET first_name=$1 ' \
                'WHERE id=$2'
        return await pool.execute(query, first_name, id)

    async def update_second_name(self, pool: Pool, id: int, second_name: str):
        query = 'UPDATE users ' \
                'SET second_name=$1 ' \
                'WHERE id=$2'
        return await pool.execute(query, second_name, id)

    async def update_email(self, pool: Pool, id: int, email: str):
        query = 'UPDATE users ' \
                'SET email=$1 ' \
                'WHERE id=$2'
        return await pool.execute(query, email, id)

    async def update_password(self, pool: Pool, id: int, password: str):
        query = 'UPDATE users ' \
                'SET password=$1 ' \
                'WHERE id=$2'
        return await pool.execute(query, password, id)
