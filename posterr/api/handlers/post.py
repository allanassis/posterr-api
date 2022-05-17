from typing import List, Tuple

from typeguard import typechecked
from aiohttp.web import View, Response, HTTPOk, HTTPBadRequest
from aiohttp.typedefs import _MultiDictProxy

from posterr.services.user import User
from posterr.services.post import Post, PostType
from posterr.storages.cache import Cache
from posterr.storages.dao.user import UserDao
from posterr.storages.database import DataBase
from posterr.storages.dao.post import PostDao
from posterr.api.handlers.base import BaseHandler

@typechecked
class PostHandlers(BaseHandler, View):

    async def get(self) -> Response:
        post_id:str = self.request.match_info.get('id')
        db:DataBase = self.request.config_dict["db"]
        cache:Cache = self.request.config_dict["cache"]


        [ user_id, last_post_id, limit_per_page ] = self._get_queries(self.request.query)

        post_dao_args:dict = {
            "limit": int(limit_per_page),
            "last_post_id": last_post_id,
        }

        if user_id:
            user_dao:UserDao = UserDao()
            user:User = User.get_by_id(user_id, user_dao, db, cache)
            post_dao_args["following_list"] = user.following["list"]
            post_dao_args["following"] = True

        post_dao:PostDao = PostDao(post_dao_args)
        if post_id is not None:
            return await self.get_by_id(post_id, Post, post_dao, db, cache)

        return await self.get_all(Post, post_dao, db, cache)

    def _get_queries(self, query:_MultiDictProxy) -> List[str]:
        queries:List = [
            query.get("user_id", ""),
            query.get("last_post_id", ""),
            query.get("limit", "10")
        ]
        return queries

    async def post(self) -> Response:
        if not await self._is_valid_json(self.request):
            return Response(body="Invalid JSON", status=HTTPBadRequest.status_code)

        body:dict = await self.request.json()
        db: DataBase = self.request.config_dict["db"]
        cache: Cache = self.request.config_dict["cache"]


        body_parsed = self._get_body(body)

        is_valid_body, msg = self._is_valid_body(*body_parsed)
        if not is_valid_body:
            return Response(body=msg, status=HTTPBadRequest.status_code)

        [ user_id, post_parent_id, post_type, post_text ] = body_parsed

        userDao:UserDao = UserDao()
        user:User = User.get_by_id(user_id, userDao, db, cache)

        postDao:PostDao = PostDao()
        post:Post = Post(post_text, user_id, post_parent_id, post_type)
        post_id:str = user.post(post, userDao, postDao, db, cache)

        return Response(body=post_id, status=HTTPOk.status_code)

    def _get_body(self, body:dict) -> List[str]:
        body:List = [
            body.get("user_id", ""),
            body.get("parent_id", ""),
            body.get("type", PostType.NORMAL.name),
            body.get("text", "")
        ]
        return body
    
    def _is_valid_body(self, user_id:str, parent_id:str, type:str, text:str) -> Tuple[bool, str]:
        if not user_id:
            return (False, "Missing user id")

        if (type != PostType.NORMAL.name) and (not parent_id):
            return (False, "Quoted posts and Reposted posts should have a post parent id")

        if not text:
            return (False, "Post text should not be empty") #I know it is not in the requirements but it is feel needed

        return (True, "Fine :D")
