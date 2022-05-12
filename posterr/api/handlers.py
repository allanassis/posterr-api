from typeguard import typechecked
from aiohttp.web import Request, Response, HTTPOk

from posterr.storages.database import DataBase

@typechecked
async def healthcheck(request: Request) -> Response:
    db:DataBase = request.config_dict["db"]
    db.healthcheck()
    return Response(body="Healthcheck", status=HTTPOk.status_code)
