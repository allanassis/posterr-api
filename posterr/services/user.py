from datetime import datetime
import json
import typing

from typeguard import typechecked
from posterr.storages.dao.post import PostDao

from posterr.storages.database import DataBase
from posterr.services.post import Post
from posterr.services.base import ServiceBase

@typechecked
class User(ServiceBase):
    _id: str
    name: str
    created_at: datetime
    followers: typing.Dict[int, typing.List[str]]
    following:typing.Dict[int, typing.List[str]]
    posts: typing.Dict[int, typing.List[str]]

    entity_name:str = "user"

    def __init__(self, _id:str = None, name: str = None) -> None:
        if _id is not None:
            self._id = _id
        if name is not None:
            self.name = name
        self.created_at = datetime.now()
        self.followers = {"count": 0, "list": []}
        self.following = {"count": 0, "list": []}
        self.posts = {"count": 0, "list": []}

    def post(self, post: Post, userDao: object, postDao:PostDao, db:DataBase) -> str:
        post_id:str = post.save(postDao, db)
        self.posts["list"].append(post_id)
        self.posts["count"] = self.posts["count"] + 1
        self.update(userDao, db)
        return post_id

    # TODO: Fix creating a querying to do just one database call to update the user
    def follow(self, following_id:str, dao:object, db:DataBase) -> str:
        user:User = User.get_by_id(self._id, dao, db)
        user._set_follow("following", following_id)
        user.update(dao, db)

        following:User = User.get_by_id(following_id, dao, db)
        following._set_follow("followers", self._id)
        following.update(dao, db)
        
        return self._id

    def _set_follow(self, type: str, user:str) -> None:
        attr:dict = getattr(self, type)
        if (user is not None) and (user not in attr["list"]):
            attr["list"].append(user)
            attr["count"] = attr["count"] + 1

    # TODO: Fix creating a querying to do just one database call to update the user
    def unfollow(self, following_id:str, dao:object, db: DataBase) -> str:
        user:User = User.get_by_id(self._id, dao, db)
        user._remove_follow("following", following_id)
        user.update(dao, db)

        following:User = User.get_by_id(following_id, dao, db)
        following._remove_follow("followers", self._id)
        following.update(dao, db)
        
        return self._id

    def _remove_follow(self, type: str, user:str) -> None:
        attr:dict = getattr(self, type)
        if (user is not None) and (user in attr["list"]):
            attr["list"].remove(user)
            attr["count"] = attr["count"] - 1

    def update(self, dao: object, db: DataBase) -> object:
        result = dao.update(self, db)
        return result

    def __str__(self) -> str:
        user_dict:dict = self.__dict__
        created_at = user_dict.pop("created_at").isoformat()
        return json.dumps({**user_dict, "created_at": created_at})
    