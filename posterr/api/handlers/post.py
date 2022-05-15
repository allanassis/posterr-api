from aiohttp.web import View, Response, HTTPOk

from posterr.services.post import Post, PostType
from posterr.services.user import User
from posterr.api.handlers.base import BaseHandler
from posterr.storages.database import DataBase

class PostHandlers(BaseHandler, View):

    async def get(self) -> Response:
        id:str = self.request.match_info.get('id')
        db:DataBase = self.request.config_dict["db"]

        if id is not None:
            return await self.get_by_id(id, db)
        return await self.get_all(db)

    async def post(self) -> Response:
        body:dict = await self.request.json()
        db: DataBase = self.request.config_dict["db"]

        user_id:str = body.get("user_id")
        type:str = body.get("type", PostType.NORMAL.name)
        parent_id:str = body.get("parent_id")
        text:str = body.get("text")

        user:User = User.get_by_id(user_id, db)
        post:Post = Post(text, user_id, parent_id, type)
        post_id:str = user.post(post, db)

        return Response(body=post_id, status=HTTPOk.status_code)