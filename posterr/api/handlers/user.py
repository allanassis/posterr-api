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
        user = User.get_by_id(id, User, db)
        if user is None:
            return web.Response(text="Not found", status=web.HTTPNotFound.status_code)
        return web.Response(body=str(user), status=web.HTTPOk.status_code)

    async def get_all(self, db):
        users = User.get_all(User, db)
        json_users = [str(user) for user in users]
        return web.Response(body=str(json_users), status=web.HTTPOk.status_code)

    async def post(self):
        body = await self.request.json()
        user:User = User(body["name"])
        user_id:str = user.save(self.request.config_dict["db"])
        return web.Response(body=user_id, status=web.HTTPOk.status_code)

    async def put(self):
        body:dict = await self.request.json()
        db = self.request.config_dict["db"]

        id = self.request.match_info.get('id')
        action = body.get("action")
        following_id = body.get("following")
        user = User(id, body.get("name"))

        if action == "FOLLOW":
            user.follow(following_id, db)
        elif action == "UNFOLLOW":
            user.unfollow(following_id, db)

        return web.Response(body=id, status=web.HTTPOk.status_code)

    # async def delete(self):
    #     id = self.request.match_info.get('id')
    #     db = self.request.config_dict["db"]

    #     deleted = User.delete(id, db)
    #     return web.Response(body=str(deleted), status=web.HTTPOk.status_code)