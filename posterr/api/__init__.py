from aiohttp import web

from posterr.api.handlers import healthcheck

def init_api():
    app = web.Application(middlewares=[web.normalize_path_middleware()])
    app.add_routes([web.get('/healthcheck', healthcheck)])
    web.run_app(app)
