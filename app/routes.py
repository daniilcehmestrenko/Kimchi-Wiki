from aiohttp.web_app import Application

from .views import UserRegisterView, FolderListView


def setup_routes(app: Application):
    app.router.add_view('/register', UserRegisterView)
    app.router.add_view('/myfolders', FolderListView)
