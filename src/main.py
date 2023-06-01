from aiohttp import web
from aiohttp.web_app import Application
from aiohttp_swagger3 import SwaggerDocs, SwaggerUiSettings

from connect_db import ConnectDb
from auth.routes import UserRegisterView, LoginView
from auth.middleware import auth_middleware
from records.routes import FolderView, RecordView


def setup_routes(app: Application):
    app.router.add_view('/register', UserRegisterView)
    app.router.add_view('/login', LoginView)
    app.router.add_view('/myfolders', FolderView)
    app.router.add_view('/records/{id}', RecordView)


def setup_db(app: Application):
    db_service = ConnectDb()

    app.on_startup.append(db_service.create_db_pool)
    app.on_cleanup.append(db_service.destroy_db_pool)


if __name__ == '__main__':
    app = Application(middlewares=[auth_middleware])
    setup_db(app)
    setup_routes(app)
    swagger = SwaggerDocs(app, swagger_ui_settings=SwaggerUiSettings(path='/docs'))
    swagger.add_routes([
        web.view('/register', UserRegisterView)
    ])
    web.run_app(app, port=8001)
