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

    # TODO: Fix creating a querying to do just one database call to update the user
    def follow(self, following_id, db:DataBase) -> str:
        user:User = User.get_by_id(self._id, User, db)
        user.set_following(following_id)
        user.update(db)

        following:User = User.get_by_id(following_id, User, db)
        following.set_follower(self._id)
        following.update(db)
        
        return self._id
    
    # TODO: Fix creating a querying to do just one database call to update the user
    def unfollow(self, following_id, db: DataBase) -> str:
        user:User = User.get_by_id(self._id, User, db)
        user.remove_following(following_id)
        user.update(db)

        following:User = User.get_by_id(following_id, User, db)
        following.remove_follower(self._id)
        following.update(db)
        
        return self._id

    def post(self, post: Post, db:DataBase) -> str:
        post_id = post.save(db)
        self.posts["list"].append(post_id)
        self.posts["count"] = self.posts["count"] + 1
        self.update(db)
        return post_id

    def update(self, db: DataBase) -> object:
        result = db.update(self, User.__name__.lower())
        return result

    # TODO: Remove duplicated code
    def set_follower(self, follower) -> None:
        if (follower is not None) and (follower not in self.followers["list"]):
            self.followers["list"].append(follower)
            self.followers["count"] = self.followers["count"] + 1

    def set_following(self, following) -> None:
        if (following is not None) and (following not in self.following["list"]):
            self.following["list"].append(following)
            self.following["count"] = self.following["count"] + 1
    
    def remove_follower(self, follower) -> None:
        if (follower is not None) and (follower in self.followers["list"]):
            self.followers["list"].remove(follower)
            self.followers["count"] = self.followers["count"] - 1

    def remove_following(self, following) -> None:
        if (following is not None) and (following in self.following["list"]):
            self.following["list"].remove(following)
            self.following["count"] = self.following["count"] - 1

    def __str__(self) -> str:
        return json.dumps(self.__dict__)
    