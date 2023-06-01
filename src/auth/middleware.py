import jwt

from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web import Request

from asyncpg.pool import Pool

from models import User
from config import JWT_SECRET, JWT_ALGORITHM, DB_KEY, WHITE_LIST
from .repositories import AuthRepository


async def auth_middleware(app: Application, handler):
    async def middleware(request: Request):
        if request.rel_url.path in WHITE_LIST:
            return await handler(request)
        elif 'docs' in request.rel_url.path:
            return await handler(request)

        repository = AuthRepository()
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
                record = await repository.get_by_id(conn, payload['user_id'])
                request.user = User(**record)

            return await handler(request)
        return web.json_response(
            data={'message': 'Permission denied'},
            status=400
        )
    return middleware
