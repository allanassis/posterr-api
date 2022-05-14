from typeguard import typechecked
from aiohttp.web import Application
from aiohttp import web
from vyper import Vyper

from posterr.api.handlers.handlers import healthcheck
from posterr.api.handlers.user import UserHandlers
from posterr.storages.database import DataBase

@typechecked
def init_api(config: Vyper) -> None:
    db_host:str = config.get_string("storages.database.host")
    db_port:str = config.get_int("storages.database.port")
    db_name:str = config.get_string("storages.database.name")

    app:Application = Application(middlewares=[web.normalize_path_middleware()])
    app["db"] = DataBase(db_name, db_host, db_port)

    app.add_routes([web.get('/healthcheck', healthcheck)])

    app.router.add_view("/user/", UserHandlers)
    app.router.add_view("/user/{id}", UserHandlers)
    
    web.run_app(app)
