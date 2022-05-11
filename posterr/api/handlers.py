from aiohttp import web

async def healthcheck(request):
    db = request.config_dict["db"]
    db.healthcheck()
    return web.Response(body="Healthcheck", status=web.HTTPOk.status_code)
