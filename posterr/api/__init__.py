from aiohttp import web

from posterr.api.handlers import healthcheck
from posterr.storages.database import DataBase

def init_api(config):
    host = config.get_string("storages.database.host")
    port = config.get_int("storages.database.port")

    app = web.Application(middlewares=[web.normalize_path_middleware()])
    app["db"] = DataBase(host, port)
    app.add_routes([web.get('/healthcheck', healthcheck)])

    web.run_app(app)
