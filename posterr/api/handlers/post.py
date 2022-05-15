from aiohttp.web import View, Response, HTTPOk
from typeguard import typechecked

from posterr.services.post import Post, PostType
from posterr.services.user import User
from posterr.api.handlers.base import BaseHandler
from posterr.storages.dao.user import UserDao
from posterr.storages.database import DataBase
from posterr.storages.dao.post import PostDao

@typechecked
class PostHandlers(BaseHandler, View):

    async def get(self) -> Response:
        id:str = self.request.match_info.get('id')
        db:DataBase = self.request.config_dict["db"]
        last_post_date = self.request.query.get("last_post_date", "")
        limit_per_page = int(self.request.query.get("limit", 10))
        dao = PostDao({
            "limit": limit_per_page,
            "last_post_date": last_post_date
        })

        if id is not None:
            return await self.get_by_id(id, Post, dao, db)

        return await self.get_all(Post, dao, db)

    async def post(self) -> Response:
        body:dict = await self.request.json()
        db: DataBase = self.request.config_dict["db"]

        user_id:str = body.get("user_id")
        type:str = body.get("type", PostType.NORMAL.name)
        parent_id:str = body.get("parent_id")
        text:str = body.get("text")

        userDao = UserDao()
        user:User = User.get_by_id(user_id, userDao, db)

        postDao = PostDao()
        post:Post = Post(text, user_id, parent_id, type)
        post_id:str = user.post(post, userDao, postDao, db)

        return Response(body=post_id, status=HTTPOk.status_code)