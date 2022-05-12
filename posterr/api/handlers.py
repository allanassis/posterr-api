from aiohttp.web import Request, Response, HTTPOk

async def healthcheck(request: Request) -> Response:
    db = request.config_dict["db"]
    db.healthcheck()
    return Response(body="Healthcheck", status=HTTPOk.status_code)
