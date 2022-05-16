from typing import List, Tuple

from typeguard import typechecked
from aiohttp.web import Response, View, HTTPOk, HTTPBadRequest, HTTPUnprocessableEntity

from posterr.services.user import User, UserValidationError
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

        user_name:str = body.get("name", "")

        is_valid_body, msg = self._is_valid_post_body(user_name)
        if not is_valid_body:
            return Response(body=msg, status=HTTPBadRequest.status_code)

        user_dao:UserDao = UserDao()

        try:
            user:User = User(name=user_name)
            user_id:str = user.save(user_dao, db)

        except UserValidationError as err:
            return Response(body=str(err), status=HTTPUnprocessableEntity.status_code)

        return Response(body=user_id, status=HTTPOk.status_code)

    def _is_valid_post_body(self, name:str) -> Tuple[bool, str]:
        if not name:
            return (False, "At least you need to give a name to create a user my friend")
        return (True, "Fine :D")

    async def put(self) -> Response:
        user_id:str = self.request.match_info.get('id')
        body:dict = await self.request.json()
        db:DataBase = self.request.config_dict["db"]

        body_parsed:List = self._get_body(body)
        is_valid_body, msg = self._is_valid_put_body(*body_parsed)
        if not is_valid_body:
            return Response(body=msg, status=HTTPBadRequest.status_code)

        [ action, following_id, user_name ] = body_parsed
        user_dao:UserDao = UserDao()
        user:User = User(user_id, user_name)

        # TODO: Create a enum to handle these actions
        if action == "FOLLOW":
            user.follow(following_id, user_dao, db)

        elif action == "UNFOLLOW":
            user.unfollow(following_id, user_dao, db)

        elif action == "UPDATE":
            user.update(user_dao, db)

        return Response(body=user_id, status=HTTPOk.status_code)

    def _get_body(self, body:dict) -> List[str]:
        body = [
            body.get("action", ""),
            body.get("following", ""),
            body.get("name", "")
        ]
        return body
    
    def _is_valid_put_body(self, action:str, following_id:str, user_name:str) -> Tuple[bool, str]:
        if not action:
            return (False, "It is necessary to give one of the following actions: 'UPDATE', 'FOLLOW', 'UNFOLLOW'")

        if (action == 'UPDATE') and (not user_name):
            return (False, "You need to pass an user name to update it")

        if (action in ['FOLLOW', 'UNFOLLOW']) and (not following_id):
            return (False, "You need to pass the user id to follow")
        return (True, "Fine :D")
