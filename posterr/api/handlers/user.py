from aiohttp.web import Response, View, HTTPOk
from typeguard import typechecked

from posterr.services.user import User
from posterr.api.handlers.base import BaseHandler
from posterr.storages.dao.user import UserDao
from posterr.storages.database import DataBase

@typechecked
class UserHandlers(BaseHandler, View):

    async def get(self) -> Response:
        id:str = self.request.match_info.get('id')
        db:DataBase = self.request.config_dict["db"]
        dao = UserDao()

        if id is not None:
            return await self.get_by_id(id, User, dao, db)

        return await self.get_all(User, dao, db)

    async def post(self) -> Response:
        body:dict = await self.request.json()
        user:User = User(name=body["name"])
        dao = UserDao()
        user_id:str = user.save(dao, self.request.config_dict["db"])

        return Response(body=user_id, status=HTTPOk.status_code)

    async def put(self) -> Response:
        body:dict = await self.request.json()
        db:DataBase = self.request.config_dict["db"]
        userDao = UserDao()
        id:str = self.request.match_info.get('id')
        action:str = body.get("action")
        following_id:str = body.get("following")
        user:User = User(id, body.get("name"))

        if action == "FOLLOW":
            user.follow(following_id, userDao, db)
        elif action == "UNFOLLOW":
            user.unfollow(following_id, userDao, db)

        return Response(body=id, status=HTTPOk.status_code)

    # async def delete(self):
    #     id = self.request.match_info.get('id')
    #     db = self.request.config_dict["db"]

    #     deleted = User.delete(id, db)
    #     return web.Response(body=str(deleted), status=web.HTTPOk.status_code)