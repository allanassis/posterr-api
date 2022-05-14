import json
from datetime import datetime
from enum import Enum

from posterr.storages.database import DataBase

class PostType(Enum):
    NORMAL = "normal"
    REPOSTED = "reposted"
    QUOTED = "quoted"


class Post(object):
    _id: str
    type: Enum
    text: str
    user_id: str
    parent_id: str
    created_at: datetime

    def __init__(self, text: str, user_id: str, parent_id: str = None, type:Enum = PostType.NORMAL) -> None:
        self.text = text
        self.user_id = user_id
        if parent_id is not None:
            self.parent_id = parent_id
        if type is not None:
            self.type = PostType[type]
        self.created_at = datetime.now().isoformat()
    
    def save(self, db: DataBase) -> str:
        inserted_id:str = db.save(self, Post.__name__.lower())
        return inserted_id
    
    @staticmethod
    def get_all(db: DataBase) -> object:# type: ignore
        items = db.get_all(Post.__name__.lower())
        posts = []
        for item in items:
            post = Post(item["text"], item["user_id"])
            post.build(item)
            posts.append(post)
        return posts

    @staticmethod
    def get_by_id(id: str, db: DataBase) -> object:
        item:dict= db.get_by_id(id, Post.__name__.lower())
        post = Post(item.get("text"), item.get("user_id"))
        return post.build(item)

    def build(self, properties:dict) -> object:# type: ignore
        for k,v in enumerate(properties):
            setattr(self, k, v)
        return self
    
    def __str__(self) -> str:
        post_dict:dict = self.__dict__
        type = post_dict.pop("type")
        return json.dumps({**self.__dict__, "type": type})