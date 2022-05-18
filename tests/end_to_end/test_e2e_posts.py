from datetime import datetime
import json
from unittest import async_case
from uuid import uuid1
import pytest
from aiohttp import ClientSession


@pytest.mark.asyncio
class TestE2EPosts(async_case.IsolatedAsyncioTestCase):
    HOST:str = "http://0.0.0.0:8080/post"


    ## HELPERS ##
    async def _create_user(self):
        # empty = {"count": 0, "list":[]}

        # user_expected:dict = {
        #     "followers": empty.copy(),
        #     "following": empty.copy(),
        #     "posts": empty.copy(),
        #     "_id": None,
        #     "name": "",
        #     "created_at": datetime.now().strftime("%b %d, %Y"),
        # }

        async with ClientSession() as session:
            async with session.post("http://0.0.0.0:8080/user", json={"name": f"Malvin{uuid1()}"[:10]}) as resp:
                user_id = await resp.text()
                return (user_id, resp.status)

    async def _create_post(self, body):
        async with ClientSession() as session:
            async with session.post(self.HOST, json=body) as resp:
                post_id = await resp.text()
                return (post_id, resp.status)

    async def _get_post(self, id=None, query=None):
        host = f"{self.HOST}"
        if id:
            host = f"{self.HOST}/{id}"
        if query:
            host = f"{host}/{query}"
        async with ClientSession() as session:
            async with session.get(host) as resp:
                post = await resp.text()
                return (post, resp.status)


    ## // ##
    
    # TESTS
    async def test_post_creation(self):
        # arrange / act
        user_id, _ = await self._create_user()
        post_body = { "user_id": user_id, "text": "Gomu Gomu no Thor"}

        # act
        post_id, status = await self._create_post(post_body)

        # assert
        self.assertEqual(status, 200)
        self.assertIsInstance(post_id, str)
    

    async def test_user_post_by_id(self):
        # arrange
        user_id, _ = await self._create_user()
        post_body = { "user_id": user_id, "text": "Gomu Gomu no Thor"}
        post_id, _ = await self._create_post(post_body)

        expected_post = {
            "text": "Gomu Gomu no Thor", 
            "user_id": user_id,
            "_id": post_id,
            "type": "normal", 
            "created_at": datetime.now().strftime("%b %d, %Y")
        }

        # act
        post, status = await self._get_post(post_id)

        # assert
        self.assertEqual(status, 200)
        self.assertEqual(json.dumps(expected_post), post)
    
    async def test_post_get_all(self):
        # arrange
        user_id, _ = await self._create_user()
        post_body = { "user_id": user_id, "text": "Gomu Gomu no Thor"}
        post_id, _ = await self._create_post(post_body)

        expected_post = {
            "text": "Gomu Gomu no Thor", 
            "user_id": user_id,
            "_id": post_id,
            "type": "normal", 
            "created_at": datetime.now().strftime("%b %d, %Y")
        }

        # act
        posts, status = await self._get_post()

        # assert
        self.assertEqual(status, 200)
        self.assertIn(json.dumps(expected_post), json.loads(posts))

    async def test_post_get_all_limited(self):
        # arrange
        user_id, _ = await self._create_user()
        post_body = { "user_id": user_id, "text": "Gomu Gomu no Thor"}
        await self._create_post(post_body)
        await self._create_post(post_body)
        await self._create_post(post_body)

        # act
        posts, status = await self._get_post(query="?limit=2")

        # assert
        self.assertEqual(status, 200)
        self.assertEqual(len(json.loads(posts)), 2)

    async def test_post_get_all_limited_after_post_id(self):
        # arrange
        user_id, _ = await self._create_user()
        post_body = { "user_id": user_id, "text": "Gomu Gomu no Thor"}
        post_id, _ = await self._create_post(post_body)
        expected_post = {
            "text": "Gomu Gomu no Thor", 
            "user_id": user_id,
            "_id": post_id,
            "type": "normal", 
            "created_at": datetime.now().strftime("%b %d, %Y")
        }
        await self._create_post(post_body)
        await self._create_post(post_body)

        # act
        posts, status = await self._get_post(query=f"?limit=2&last_post_id={post_id}")

        # assert
        self.assertEqual(status, 200)
        self.assertEqual(len(json.loads(posts)), 2)
        self.assertNotIn(json.dumps(expected_post), json.loads(posts))

    async def test_post_get_all_from_users_following(self):
        # arrange
        user_id_root, _ = await self._create_user()
        user_id_following, _ = await self._create_user()
        post_body_1 = { "user_id": user_id, "text": "Gomu Gomu no Thor"}
        post_id, _ = await self._create_post(post_body_1)
        post_body_1 = { "user_id": user_id, "text": "Gomu Gomu no Thor"}
        post_id, _ = await self._create_post(post_body_1)
        expected_post = {
            "text": "Gomu Gomu no Thor", 
            "user_id": user_id,
            "_id": post_id,
            "type": "normal", 
            "created_at": datetime.now().strftime("%b %d, %Y")
        }
        await self._create_post(post_body)
        await self._create_post(post_body)

        # act
        posts, status = await self._get_post(query=f"?limit=2&last_post_id={post_id}")

        # assert
        self.assertEqual(status, 200)
        self.assertEqual(len(json.loads(posts)), 2)
        self.assertNotIn(json.dumps(expected_post), json.loads(posts))

