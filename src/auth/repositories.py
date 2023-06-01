from asyncpg import Pool

from abstracts import AbstractRepository
from .exceptions import UserDoesNotExist
from .schemas import UserCreate


class AuthRepository(AbstractRepository):
    async def create(self, pool: Pool, user: UserCreate):
        query = 'INSERT INTO users ' \
                '(first_name, second_name, email, password) ' \
                'VALUES ($1, $2, $3, $4)'
        return await pool.execute(
            query,
            user.first_name,
            user.second_name,
            user.email,
            user.password
        )

    async def get_by_id(self, pool: Pool, id: int):
        query = 'SELECT * FROM users ' \
                'WHERE id=$1'
        user = await pool.fetchrow(query, id)
        if user:
            return user
        raise UserDoesNotExist

    async def get(self, pool: Pool, email: str):
        query = 'SELECT * FROM users ' \
                'WHERE email=$1'
        user = await pool.fetchrow(query, email)
        if user:
            return user
        raise UserDoesNotExist
