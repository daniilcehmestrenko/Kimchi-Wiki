import jwt

from aiohttp import web
from asyncpg import Pool
from asyncpg.exceptions import UniqueViolationError

from pydantic.error_wrappers import ValidationError

from datetime import datetime, timedelta

from config import (
    DB_KEY,
    JWT_ALGORITHM,
    JWT_EXP_DELTA_SECONDS,
    JWT_SECRET
)
from models import User
from .exceptions import UserDoesNotExist, UserPasswordDoesNotMatch
from .utils import match_password
from .repositories import AuthRepository
from .schemas import UserCreate, UserAuthData


class UserRegisterView(web.View):
    async def post(self):
        """
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  first_name:
                    type: string

        responses:
          '200':
            description: OK.

        """
        repository = AuthRepository()
        request_data = await self.request.json()
        try:
            data = UserCreate(**request_data)
            pool: Pool = self.request.app[DB_KEY]
            async with pool.acquire() as conn:
                async with conn.transaction():
                    await repository.create(conn, data)

            return web.json_response(data=data.json())

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
        repository = AuthRepository()
        request_data = await self.request.json()
        try:
            authdata = UserAuthData(**request_data)
            pool: Pool = self.request.app[DB_KEY]

            async with pool.acquire() as conn:
                record = await repository.get(
                    pool=conn,
                    email=authdata.email
                )
            user = User(**record)
            await match_password(user, authdata.password)
            payload = {
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
            }
            jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

            return web.json_response({'token': jwt_token})

        except ValidationError as error:
            return web.json_response(
                data={'message': f'Validate error - {str(error)}'},
                status=400
            )
        except (UserDoesNotExist, UserPasswordDoesNotMatch):
            return web.json_response(
                data={'message': 'Wrong user cred'},
                status=400
            )
