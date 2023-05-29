from aiohttp import web
from asyncpg import Pool, Record
from asyncpg.exceptions import UniqueViolationError

from pydantic.error_wrappers import ValidationError

from config import settings
from .repositories import UserRepository, FolderRepository
from .schemas import UserCreate, UserAuthData, UserId, FolderCreate


class UserRegisterView(web.View):
    async def post(self):
        repository = UserRepository()
        request_data = await self.request.json()
        try:
            validate_data = UserCreate(**request_data)
            pool: Pool = self.request.app[settings.DB_KEY]
            async with pool.acquire() as conn:
                async with conn.transaction():
                    await repository.create(pool=conn, **validate_data.dict())
            return web.json_response(data=validate_data.json())

        except ValidationError as error:
            return web.json_response(
                data={'message': f'Validate error - {str(error)}'},
                status=400
            )
        except UniqueViolationError as error:
            return web.json_response(
                data={'message': f'Unique error - {str(error)}'},
                status=400
            )


class LoginView(web.View):
    async def post(self):
        repository = UserRepository()
        request_data = await self.request.json()
        try:
            authdata = UserAuthData(**request_data)
            pool: Pool = self.request.app[settings.DB_KEY]
            async with pool.acquire() as conn:
                user_data: Record = await repository.get_user_info(
                    pool=conn,
                    email=authdata.email,
                    password=authdata.password
                )
            if user_data:
                return web.json_response(dict(user_data))
            return web.json_response(data={'message': 'Account Not Found'})

        except ValidationError as error:
            return web.json_response(
                data={'message': f'Validate error - {str(error)}'},
                status=400
            )


class FolderListView(web.View):
    async def get(self):
        repository = FolderRepository()
        pool: Pool = self.request.app[settings.DB_KEY]
        try:
            request_data = await self.request.json()
            validate_data = UserId(**request_data)

            async with pool.acquire() as conn:
                records = await repository.get_user_folders(
                    pool=conn,
                    user_id=validate_data.user_id
                )
            return web.json_response(data=[dict(rec) for rec in records])

        except ValidationError as error:
            return web.json_response(
                data={'message': f'Validate error - {str(error)}'},
                status=400
            )

    async def post(self):
        repository = FolderRepository()
        pool: Pool = self.request.app[settings.DB_KEY]
        try:
            request_data = await self.request.json()
            validate_data = FolderCreate(**request_data)

            async with pool.acquire() as conn:
                async with conn.transaction():
                    await repository.create(pool=conn, **validate_data.dict())

            return web.json_response(data=validate_data.json())

        except ValidationError as error:
            return web.json_response(
                data={'message': f'Validation error - {str(error)}'},
                status=400
            )
