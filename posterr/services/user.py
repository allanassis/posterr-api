from datetime import datetime
import json
import typing

from posterr.storages.database import DataBase
from posterr.services.post import Post

class User:
    _id: str
    name: str
    created_at: datetime
    followers: typing.Dict[int, typing.List[str]]
    following:typing.Dict[int, typing.List[str]]
    posts: typing.Dict[int, typing.List[str]]

    def __init__(self, _id:str = None, name: str = None) -> None:
        self._id = _id
        self.name = name
        self.created_at = datetime.now().isoformat()
        self.followers = {"count": 0, "list": []}
        self.following = {"count": 0, "list": []}
        self.posts = {"count": 0, "list": []}

    def save(self, db:DataBase) -> str:
        inserted_id = db.save(self, User.__name__.lower())
        return inserted_id

    @staticmethod
    def get_by_id(id: str, db: DataBase) -> object:# type: ignore
        item = db.get_by_id(id, User.__name__.lower())
        user = User()
        return user.build(item)

    @staticmethod
    def get_all(db: DataBase) -> typing.List[object]:
        items = db.get_all(User.__name__.lower())
        users = []
        for item in items:
            user = User()
            user.build(item)
            users.append(user)
        return users

    def build(self, properties:dict) -> object:# type: ignore
        for k,v in properties.items():
            setattr(self, k, v)
        return self

    # TODO: Fix creating a querying to do just one database call to update the user
    def follow(self, following_id, db:DataBase) -> str:
        user:User = User.get_by_id(self._id, db)
        user.set_following(following_id)
        user.update(db)

        following:User = User.get_by_id(following_id, db)
        following.set_follower(self._id)
        following.update(db)
        
        return self._id
    
    # TODO: Fix creating a querying to do just one database call to update the user
    def unfollow(self, following_id, db: DataBase) -> str:
        user:User = User.get_by_id(self._id, db)
        user.remove_following(following_id)
        user.update(db)

        following:User = User.get_by_id(following_id, db)
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
    