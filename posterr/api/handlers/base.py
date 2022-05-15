from typing import List

from aiohttp.web import Response, HTTPOk, HTTPNotFound

from posterr.storages.database import DataBase

class BaseHandler(object):

    async def get_by_id(self, Class:object, id: str, db: DataBase) -> Response:
        instance:object = Class.get_by_id(id, db)
        if instance is None:
            return Response(text="Not found", status=HTTPNotFound.status_code)
        return Response(body=str(instance), status=HTTPOk.status_code)

    async def get_all(self, Class:object, db:DataBase) -> Response:
        instance_list: List[object] = Class.get_all(db)
        json_instances: List[str] = [str(instance) for instance in instance_list]
        return Response(body=str(json_instances), status=HTTPOk.status_code)
