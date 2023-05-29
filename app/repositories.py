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
