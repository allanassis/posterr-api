from typeguard import typechecked
from aiohttp.web import Application
from aiohttp import web
from vyper import Vyper

from posterr.api.handlers import healthcheck
from posterr.storages.database import DataBase

@typechecked
def init_api(config: Vyper):
    db_host:str = config.get_string("storages.database.host")
    db_port:str = config.get_int("storages.database.port")
    db_name:str = config.get_string("storages.database.name")

    app:Application = Application(middlewares=[web.normalize_path_middleware()])
    app["db"] = DataBase(db_name, db_host, db_port)
    app.add_routes([web.get('/healthcheck', healthcheck)])

    web.run_app(app)
