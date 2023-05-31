import jwt

from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web import Request

from asyncpg.pool import Pool

from config import JWT_SECRET, JWT_ALGORITHM, DB_KEY, WHITE_LIST
from .repositories import UserRepository
from .models import User


async def auth_middleware(app: Application, handler):
    async def middleware(request: Request):
        if request.rel_url.path in WHITE_LIST:
            return await handler(request)

        repository = UserRepository()
        pool: Pool = app[DB_KEY]
        request.user = None
        jwt_token = request.headers.get('Authorization')

        if jwt_token:
            try:
                payload = jwt.decode(
                    jwt_token, JWT_SECRET,
                    algorithms=[JWT_ALGORITHM]
                )
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return web.json_response(
                    data={'message': 'Token is invalid'},
                    status=400
                )
            async with pool.acquire() as conn:
                user = await repository.get_by_id(conn, payload['user_id'])
                request.user = User(**dict(user))

            return await handler(request)
        return web.json_response(
            data={'message': 'Permission denied'},
            status=400
        )
    return middleware
