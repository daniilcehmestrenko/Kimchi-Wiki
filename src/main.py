from aiohttp import web
from aiohttp.web_app import Application

from connect_db import ConnectDb
from auth.routes import setup_routes as setup_auth
from folders.routes import setup_routes as setup_folders


def setup_routes(app: Application):
    setup_auth(app)
    setup_folders(app)


def setup_db(app: Application):
    db_service = ConnectDb()

    app.on_startup.append(db_service.create_db_pool)
    app.on_cleanup.append(db_service.destroy_db_pool)


if __name__ == '__main__':
    app = Application()
    setup_db(app)
    setup_routes(app)
    web.run_app(app, port=8001)
