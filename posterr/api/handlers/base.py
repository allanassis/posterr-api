from typing import List

from typeguard import typechecked
from aiohttp.web import Response, Request, HTTPOk, HTTPNotFound
from posterr.storages.cache import Cache

from posterr.storages.database import DataBase

@typechecked
class BaseHandler(object):

    async def get_by_id(self, id: str, Class:object, dao:object, db: DataBase, cache: Cache) -> Response:
        instance:object = Class.get_by_id(id, dao, db, cache)
        if instance is None:
            return Response(body="Not found", status=HTTPNotFound.status_code)
        return Response(body=str(instance), status=HTTPOk.status_code)

    async def get_all(self, Class:object, dao: object, db:DataBase, cache: Cache) -> Response:
        instance_list: List[object] = Class.get_all(dao, db, cache)
        if not instance_list:
            return Response(body="Not found", status=HTTPNotFound.status_code)
        json_instances: List[str] = [str(instance) for instance in instance_list]
        return Response(body=str(json_instances), status=HTTPOk.status_code)

    async def _is_valid_json(self, request) -> bool:
        try:
            await request.json()
            return True
        except:
            return False