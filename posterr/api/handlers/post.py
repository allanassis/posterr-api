from aiohttp import web

from posterr.services.post import Post, PostType
from posterr.services.user import User

class PostHandlers(web.View):

    async def get(self):
        id = self.request.match_info.get('id')
        db = self.request.config_dict["db"]

        if id is not None:
            return await self.get_by_id(id, db)

        return await self.get_all(db)

    async def get_by_id(self, id, db):
        post = Post.get_by_id(id, db)
        if post is None:
            return web.Response(text="Not found", status=web.HTTPNotFound.status_code)
        return web.Response(body=str(post), status=web.HTTPOk.status_code)

    async def get_all(self, db):
        posts = Post.get_all(db)
        json_posts = [str(post) for post in posts]
        return web.Response(body=str(json_posts), status=web.HTTPOk.status_code)

    async def post(self):
        body:dict = await self.request.json()
        db = self.request.config_dict["db"]

        user_id = body.get("user_id")
        type = body.get("type", PostType.NORMAL.name)
        parent_id = body.get("parent_id")
        text = body.get("text")

        user:User = User.get_by_id(user_id, db)
        post:Post = Post(text, user_id, parent_id, type)
        post_id = user.post(post, db)

        return web.Response(body=post_id, status=web.HTTPOk.status_code)