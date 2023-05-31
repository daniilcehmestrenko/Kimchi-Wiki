from aiohttp import web
from aiohttp.web_app import Application

from connect_db import ConnectDb
from auth.routes import UserRegisterView, LoginView
from auth.middleware import auth_middleware
from folders.routes import FolderListView


def setup_routes(app: Application):
    app.router.add_view('/register', UserRegisterView)
    app.router.add_view('/login', LoginView)
    app.router.add_view('/user/{id}/myfolders', FolderListView)


def setup_db(app: Application):
    db_service = ConnectDb()

    app.on_startup.append(db_service.create_db_pool)
    app.on_cleanup.append(db_service.destroy_db_pool)


if __name__ == '__main__':
    app = Application(middlewares=[auth_middleware])
    setup_db(app)
    setup_routes(app)
    web.run_app(app, port=8001)
