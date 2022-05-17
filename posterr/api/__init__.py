import logging
from typeguard import typechecked
from aiohttp.web import Application
from aiohttp import web
from aiohttp_middlewares import error, cors, timeout

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
    db_port:int = config.get_int("storages.database.port")
    db_name:str = config.get_string("storages.database.name")

    timeout_time:int = config.get_int("storages.database.port")

    app:Application = Application(middlewares=[
        web.normalize_path_middleware(),
        error.error_middleware(),
        cors.cors_middleware(allow_all=True), # TODO: THIS SHOULD BE CHANGE TO THE SPA DOMAIN THAT WILL USE THIS API
        timeout.timeout_middleware(timeout_time)
    ])
    app["db"] = DataBase(db_name, db_host, db_port)

    app.add_routes([web.get('/healthcheck', healthcheck)])

    app.router.add_view("/user/", UserHandlers)
    app.router.add_view("/user/{id}", UserHandlers)
    
    app.router.add_view("/post/", PostHandlers)
    app.router.add_view("/post/{id}", PostHandlers)
    
    web.run_app(app)
