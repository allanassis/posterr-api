from datetime import datetime
import json
import typing

from posterr.storages.database import DataBase
from posterr.services.post import Post
from posterr.services.base import ServiceBase

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
        self.created_at = datetime.now().isoformat()
        self.followers = {"count": 0, "list": []}
        self.following = {"count": 0, "list": []}
        self.posts = {"count": 0, "list": []}

    def post(self, post: Post, db:DataBase) -> str:
        post_id = post.save(db)
        self.posts["list"].append(post_id)
        self.posts["count"] = self.posts["count"] + 1
        self.update(db)
        return post_id

    # TODO: Fix creating a querying to do just one database call to update the user
    def follow(self, following_id, db:DataBase) -> str:
        user:User = User.get_by_id(self._id, db)
        user._set_follow("following", following_id)
        user.update(db)

        following:User = User.get_by_id(following_id, db)
        following._set_follow("followers", self._id)
        following.update(db)
        
        return self._id

    def _set_follow(self, type: str, user:str) -> None:
        attr = getattr(self, type)
        if (user is not None) and (user not in attr["list"]):
            attr["list"].append(user)
            attr["count"] = attr["count"] + 1

    # TODO: Fix creating a querying to do just one database call to update the user
    def unfollow(self, following_id, db: DataBase) -> str:
        user:User = User.get_by_id(self._id, db)
        user._remove_follow("following", following_id)
        user.update(db)

        following:User = User.get_by_id(following_id, db)
        following._remove_follow("followers", self._id)
        following.update(db)
        
        return self._id

    def _remove_follow(self, type: str, user:str) -> None:
        attr = getattr(self, type)
        if (user is not None) and (user in attr["list"]):
            attr["list"].remove(user)
            attr["count"] = attr["count"] - 1

    def update(self, db: DataBase) -> object:
        result = db.update(self, User.__name__.lower())
        return result

    def __str__(self) -> str:
        return json.dumps(self.__dict__)
    