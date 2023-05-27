from aiohttp import web
from aiohttp.web_app import Application

from db.connect_db import ConnectDb


def setup_db(app: Application):
    db_service = ConnectDb()

    app.on_startup.append(db_service.create_db_pool)
    app.on_cleanup.append(db_service.destroy_db_pool)


if __name__ == '__main__':
    application = Application()
    setup_db(application)
    web.run_app(application, port=8001)
