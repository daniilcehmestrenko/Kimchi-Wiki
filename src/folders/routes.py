from aiohttp import web
from aiohttp.web_app import Application
from asyncpg.pool import Pool

from pydantic.error_wrappers import ValidationError

from config import DB_KEY
from .repositories import FolderRepository
from .schemas import FolderCreate, UserId


def setup_routes(app: Application):
    app.router.add_view('/myfolders', FolderListView)


class FolderListView(web.View):
    async def get(self):
        repository = FolderRepository()
        pool: Pool = self.request.app[DB_KEY]
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
        pool: Pool = self.request.app[DB_KEY]
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
