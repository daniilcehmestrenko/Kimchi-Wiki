from abc import ABC


class AbstractRepository(ABC):
    table_name = None

    async def get(self, *args, **kwargs):
        pass

    async def create(self, *args, **kwargs):
        pass

    async def delete(self, *args, **kwargs):
        pass
