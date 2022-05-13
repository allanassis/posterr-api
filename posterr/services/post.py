from datetime import date, datetime
from enum import Enum

from bson import ObjectId

from posterr.storages.database import DataBase

class PostType(Enum):
    NORMAL = "normal"
    REPOSTED = "reposted"
    QUOTED = "quoted"


class Post(object):
    id: str
    type: Enum
    text: str
    user_id: str
    parent_id: str
    created_at: datetime

    def __init__(self, text: str, user_id: str, parent_id: str = None, type:Enum = PostType.NORMAL) -> None:
        self.type = type
        self.text = text
        self.user_id = user_id
        self.parent_id = parent_id
        self.created_at = datetime.now().isoformat()
    
    def save(self, db: DataBase) -> ObjectId:
        inserted_id:str = db.save(self, self, Post.__name__.lower())
        return ObjectId(inserted_id)
    
    @staticmethod
    def get(id: str, db: DataBase) -> Post:# type: ignore
        item = db.get(id, Post.__name__.lower())
        post = Post()
        return post.build(item)

    def build(self, properties:dict) -> Post:# type: ignore
        for k,v in enumerate(properties):
            setattr(self, k, v)
        return self