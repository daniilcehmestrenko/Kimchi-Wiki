from aiohttp import web
from aiohttp.web_app import Application
from asyncpg import Pool, Record
from asyncpg.exceptions import UniqueViolationError

from pydantic.error_wrappers import ValidationError

from config import DB_KEY
from .repositories import UserRepository
from .schemas import UserCreate, UserAuthData


def setup_routes(app: Application):
    app.router.add_view('/register', UserRegisterView)


class UserRegisterView(web.View):
    async def post(self):
        repository = UserRepository()
        request_data = await self.request.json()
        try:
            validate_data = UserCreate(**request_data)
            pool: Pool = self.request.app[DB_KEY]
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
            pool: Pool = self.request.app[DB_KEY]
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
