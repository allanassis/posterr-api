from typing import List

from typeguard import typechecked
from aiohttp.web import Response, View, HTTPOk

from posterr.services.user import User
from posterr.storages.dao.user import UserDao
from posterr.storages.database import DataBase
from posterr.api.handlers.base import BaseHandler

@typechecked
class UserHandlers(BaseHandler, View):

    async def get(self) -> Response:
        user_id:str = self.request.match_info.get('id')
        db:DataBase = self.request.config_dict["db"]

        user_dao:UserDao = UserDao()

        if user_id is not None:
            return await self.get_by_id(user_id, User, user_dao, db)

        return await self.get_all(User, user_dao, db)

    async def post(self) -> Response:
        body:dict = await self.request.json()
        db:DataBase = self.request.config_dict["db"]

        user_dao:UserDao = UserDao()
        user:User = User(name=body.get("name", ""))
        user_id:str = user.save(user_dao, db)

        return Response(body=user_id, status=HTTPOk.status_code)

    async def put(self) -> Response:
        user_id:str = self.request.match_info.get('id')
        body:dict = await self.request.json()
        db:DataBase = self.request.config_dict["db"]

        [ action, following_id, user_name ] = self._get_body(body)
        user_dao:UserDao = UserDao()
        user:User = User(user_id, user_name)

        if action == "FOLLOW":
            user.follow(following_id, user_dao, db)

        elif action == "UNFOLLOW":
            user.unfollow(following_id, user_dao, db)

        return Response(body=user_id, status=HTTPOk.status_code)

    def _get_body(self, body:dict) -> List[str]:
        body = [
            body.get("action", ""),
            body.get("following", ""),
            body.get("name", "")
        ]
        return body