from typing import List

from typeguard import typechecked
from aiohttp.web import View, Response, HTTPOk
from aiohttp.typedefs import _MultiDictProxy

from posterr.services.user import User
from posterr.services.post import Post, PostType
from posterr.storages.dao.user import UserDao
from posterr.storages.database import DataBase
from posterr.storages.dao.post import PostDao
from posterr.api.handlers.base import BaseHandler

@typechecked
class PostHandlers(BaseHandler, View):

    async def get(self) -> Response:
        post_id:str = self.request.match_info.get('id')
        db:DataBase = self.request.config_dict["db"]

        [ user_id, last_post_date, limit_per_page ] = self._get_queries(self.request.query)

        post_dao_args:dict = {
            "limit": int(limit_per_page),
            "last_post_date": last_post_date,
        }

        if user_id:
            user_dao:UserDao = UserDao()
            user:User = User.get_by_id(user_id, user_dao, db)
            post_dao_args["following_list"] = user.following["list"]

        post_dao:PostDao = PostDao(post_dao_args)
        if post_id is not None:
            return await self.get_by_id(post_id, Post, post_dao, db)

        return await self.get_all(Post, post_dao, db)

    def _get_queries(self, query:_MultiDictProxy) -> List[str]:
        queries:List = [
            query.get("user_id", ""),
            query.get("last_post_date", ""),
            query.get("limit", "10")
        ]
        return queries

    async def post(self) -> Response:
        body:dict = await self.request.json()
        db: DataBase = self.request.config_dict["db"]

        [ user_id, post_parent_id, post_type, post_text ] = self._get_body(body)

        userDao:UserDao = UserDao()
        user:User = User.get_by_id(user_id, userDao, db)

        postDao:PostDao = PostDao()
        post:Post = Post(post_text, user_id, post_parent_id, post_type)
        post_id:str = user.post(post, userDao, postDao, db)

        return Response(body=post_id, status=HTTPOk.status_code)

    def _get_body(self, body:dict) -> List[str]:
        body:List = [
            body.get("user_id", ""),
            body.get("parent_id", ""),
            body.get("type", PostType.NORMAL.name),
            body.get("text", "")
        ]
        return body
