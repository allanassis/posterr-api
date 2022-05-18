from datetime import datetime
import json
from unittest import async_case
from uuid import uuid1
import pytest
from aiohttp import ClientSession

EMPTY = {"count": 0, "list":[]}

@pytest.mark.asyncio
class TestE2EUser(async_case.IsolatedAsyncioTestCase):
    HOST:str = "http://0.0.0.0:8080/user"
    user_expected:dict = {
            "followers": EMPTY.copy(),
            "following": EMPTY.copy(),
            "posts": EMPTY.copy(),
            "_id": None,
            "name": "",
            "created_at": datetime.now().strftime("%b %d, %Y"),
        }

    ## HELPERS ##
    async def _create_user(self, name=None):
        if not name:
            name = f"Malvin{uuid1()}"[:10]
        async with ClientSession() as session:
            async with session.post(self.HOST, json={"name": name}) as resp:
                user_id = await resp.text()
                return (user_id, resp.status)

    async def _get_user(self, id=None):
        host = f"{self.HOST}/"
        if id:
            host = f"{self.HOST}/{id}"

        async with ClientSession() as session:
            async with session.get(host) as resp:
                user = await resp.text()
                return (user, resp.status)
    
    async def _update_user(self, id, body):
        async with ClientSession() as session:
            async with session.put(f"{self.HOST}/{id}", json=body) as resp:
                user_id = await resp.text()
                return (user_id, resp.status)

    ## // ##
    
    # TESTS
    async def test_user_creation(self):
        # arrange / act
        user_id, status = await self._create_user()

        # assert
        self.assertEqual(status, 200)
        self.assertIsInstance(user_id, str)
    

    async def test_user_get_by_id(self):
        # arrange
        user_name = f"Malvin{uuid1()}"[:10]
        user_id, _ = await self._create_user(user_name)
        self.user_expected["name"] = user_name
        self.user_expected["_id"] = user_id
        
        # act
        user, status = await self._get_user(user_id)

        # assert
        self.assertEqual(status, 200)
        self.assertEqual(json.dumps(self.user_expected), user)
    
    async def test_user_get_all(self):
         # arrange
        user_name = f"Malvin{uuid1()}"[:10]
        user_id, _ = await self._create_user()

        self.user_expected["name"] = user_name
        self.user_expected["_id"] = user_id
        
        # act
        users, status = await self._get_user()

        # assert
        self.assertEqual(status, 200)
        self.assertIn(json.dumps(self.user_expected), json.loads(users))
    
    async def test_follow_user(self):
         # arrange
        user_id_root, _ = await self._create_user()
        user_id_following, _ = await self._create_user()
        follow_body = {"following": user_id_following, "action": "FOLLOW"}

        # act
        _, follow_status = await self._update_user(user_id_root, follow_body)

        user_root_updated, _ = await self._get_user(user_id_root)
        user_following_updated, _ = await self._get_user(user_id_following)

        user_root_updated = json.loads(user_root_updated)
        user_following_updated = json.loads(user_following_updated)

        # assert
        self.assertEqual(follow_status, 200)
        self.assertEqual(user_root_updated["following"]["count"],1)
        self.assertEqual(user_root_updated["following"]["list"][0], user_id_following)
        self.assertEqual(user_following_updated["followers"]["count"], 1)
        self.assertEqual(user_following_updated["followers"]["list"][0], user_id_root)

    async def test_unfollow_user(self):
         # arrange
        user_id_root, _ = await self._create_user()
        user_id_following, _ = await self._create_user()

        follow_body = {"following": user_id_following, "action": "FOLLOW"}
        await self._update_user(user_id_root, follow_body)

        unfollow_body = {"following": user_id_following, "action": "UNFOLLOW"}

        # act
        _, unfollow_status = await self._update_user(user_id_root, unfollow_body)
        
        user_root_updated, _ = await self._get_user(user_id_root)
        user_following_updated, _ = await self._get_user(user_id_following)

        user_root_updated = json.loads(user_root_updated)
        user_following_updated = json.loads(user_following_updated)

        # assert
        self.assertEqual(unfollow_status, 200)
        self.assertEqual(user_root_updated["following"]["count"],0)
        self.assertListEqual(user_root_updated["following"]["list"], [])
        self.assertEqual(user_following_updated["followers"]["count"], 0)
        self.assertListEqual(user_following_updated["followers"]["list"], [])

    async def test_update_user_name(self):
        # arrange
        user_name = f"Malvin{uuid1()}"[:10]
        user_id, _ = await self._create_user(user_name)
        update_body = {"name": f"{user_name}new", "action": "UPDATE"}

        # act
        _, status = await self._update_user(user_id, update_body)
        user_updated, _ = await  self._get_user(user_id)

        # assert
        self.assertEqual(status, 200)
        self.assertEqual(f"{user_name}new", json.loads(user_updated)["name"])
    
