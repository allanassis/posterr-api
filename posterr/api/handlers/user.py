import stat
from aiohttp import web
from bson import ObjectId

from posterr.services.user import User

class UserHandlers(web.View):

    async def get(self):
        id = self.request.match_info.get('id')
        db = self.request.config_dict["db"]

        if id is not None:
            return await self.get_by_id(id, db)

        return await self.get_all(db)

    async def get_by_id(self, id, db):
        item = User.get_by_id(id, db)
        if item is None:
            return web.Response(text="Not found", status=web.HTTPNotFound.status_code)
        return web.Response(body=str(item), status=web.HTTPOk.status_code)

    async def get_all(self, db):
        users = User.get_all(db)
        json_users = [str(user) for user in users]
        return web.Response(body=str(json_users), status=web.HTTPOk.status_code)

    async def post(self):
        body = await self.request.json()
        item:User = User(body["name"])
        user_id:str = item.save(self.request.config_dict["db"])
        return web.Response(body=user_id, status=web.HTTPOk.status_code)

    # async def put(self):
    #     body = await self.request.json()
    #     id = self.request.match_info.get('id')
    #     item = User(body["name"])
    #     db = self.request.config_dict["db"]
    #     updated = item.update(db)
    #     return web.Response(body=str(updated), status=web.HTTPOk.status_code)

    # async def delete(self):
    #     id = self.request.match_info.get('id')
    #     db = self.request.config_dict["db"]

    #     deleted = User.delete(id, db)
    #     return web.Response(body=str(deleted), status=web.HTTPOk.status_code)