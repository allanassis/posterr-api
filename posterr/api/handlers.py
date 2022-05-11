from aiohttp import web

async def healthcheck(request):
    return web.Response(body="Healthcheck", status=web.HTTPOk.status_code)
