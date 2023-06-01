from aiohttp import web
from asyncpg.pool import Pool

from pydantic.error_wrappers import ValidationError

from models import User
from config import DB_KEY
from .schemas import FolderPOST, FolderGET, RecordGET, RecordPOST
from .repositories import FolderRepository, RecordRepository


class FolderView(web.View):
    async def get(self):
        repository = FolderRepository()
        user: User = self.request.user
        pool: Pool = self.request.app[DB_KEY]

        async with pool.acquire() as conn:
            user_folders = await repository.get_folders(conn, user.id)
        data = [FolderGET(**record).dict() for record in user_folders]
        return web.json_response(
            data=data,
            status=200
        )

    async def post(self):
        repository = FolderRepository()
        user: User = self.request.user
        pool: Pool = self.request.app[DB_KEY]

        try:
            request_data = await self.request.json()
            validate_date = FolderPOST(**request_data)

            async with pool.acquire() as conn:
                async with conn.transaction():
                    await repository.create(
                        pool=conn,
                        folder=validate_date,
                        user_id=user.id
                    )
            return web.json_response(
                data=validate_date.dict(),
                status=200
            )
        except ValidationError as error:
            return web.json_response(
                data={'message': f'Validate error {str(error)}'},
                status=400
            )


class RecordView(web.View):
    async def get(self):
        repository = RecordRepository()
        folder_id = self.request.match_info['id']
        pool: Pool = self.request.app[DB_KEY]

        async with pool.acquire() as conn:
            records = await repository.get_records(conn, int(folder_id))
        data = [RecordGET(**record).dict() for record in records]
        return web.json_response(
            data=data,
            status=200
        )

    async def post(self):
        repository = RecordRepository()
        folder_id = self.request.match_info['id']
        pool: Pool = self.request.app[DB_KEY]
        try:
            request_data = await self.request.json()
            validate_data = RecordPOST(**request_data)
            async with pool.acquire() as conn:
                async with conn.transaction():
                    await repository.create(
                        pool=conn,
                        record=validate_data,
                        folder_id=int(folder_id)
                    )
            return web.json_response(
                data=validate_data.dict(),
                status=200
            )
        except ValidationError as error:
            return web.json_response(
                data={'message': f'Validate error {str(error)}'},
                status=400
            )
