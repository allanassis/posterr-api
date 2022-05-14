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

    def __str__(self) -> str:
        return json.dumps({ **self.__dict__, "_id": str(self._id) })