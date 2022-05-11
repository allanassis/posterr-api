from aiohttp import web

from posterr.api.handlers import healthcheck
from posterr.storages.database import DataBase

def init_api():
    app = web.Application(middlewares=[web.normalize_path_middleware()])
    app["db"] = DataBase()

    app.add_routes([web.get('/healthcheck', healthcheck)])
    web.run_app(app)
