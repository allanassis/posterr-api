import logging
from typeguard import typechecked
from aiohttp.web import Application
from aiohttp import web
from vyper import Vyper

from posterr.api.handlers.healthcheck import healthcheck
from posterr.api.handlers.post import PostHandlers
from posterr.api.handlers.user import UserHandlers
from posterr.storages.database import DataBase
from posterr.config import ConfigManager

@typechecked
def init_api() -> None:
    logging.basicConfig(level=logging.DEBUG)

    config = ConfigManager().config
    db_host:str = config.get_string("storages.database.host")
    db_port:str = config.get_int("storages.database.port")
    db_name:str = config.get_string("storages.database.name")

    app:Application = Application(middlewares=[web.normalize_path_middleware()])
    app["db"] = DataBase(db_name, db_host, db_port)

    app.add_routes([web.get('/healthcheck', healthcheck)])

    app.router.add_view("/user/", UserHandlers)
    app.router.add_view("/user/{id}", UserHandlers)
    
    app.router.add_view("/post/", PostHandlers)
    app.router.add_view("/post/{id}", PostHandlers)
    
    web.run_app(app)
