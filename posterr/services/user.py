from datetime import datetime
import json
import typing

from bson import ObjectId

from posterr.storages.database import DataBase
from posterr.services.post import Post

class User:
    _id: ObjectId
    name: str
    created_at: datetime
    followers: typing.Dict[int, typing.List[ObjectId]]
    following:typing.Dict[int, typing.List[ObjectId]]
    posts: typing.Dict[int, typing.List[ObjectId]]

    def __init__(self, name: str = None) -> None:
        self.name = name
        self.created_at = datetime.now().isoformat()
        self.followers = {"count": 0, "list": []}
        self.following = {"count": 0, "list": []}
        self.posts = {"count": 0, "list": []}

    def save(self, db:DataBase) -> str:
        inserted_id = db.save(self, User.__name__.lower())
        return inserted_id

    @staticmethod
    def get(id: str, db: DataBase) -> object:# type: ignore
        item = db.get(id, User.__name__.lower())
        user = User()
        return user.build(item)

    def build(self, properties:dict) -> User:# type: ignore
        for k,v in enumerate(properties):
            setattr(self, k, v)
        return self

    def __str__(self) -> str:
        return json.dumps({ **self.__dict__, "_id": str(self._id) })