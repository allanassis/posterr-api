import json
import typing
from datetime import datetime
from enum import Enum

from posterr.storages.database import DataBase
from posterr.services.base import ServiceBase

class PostType(Enum):
    NORMAL = "normal"
    REPOSTED = "reposted"
    QUOTED = "quoted"


class Post(ServiceBase):
    _id: str
    type: Enum
    text: str
    user_id: str
    parent_id: str
    created_at: datetime

    entity_name:str = "post"

    def __init__(self, text: str = None, user_id: str = None, parent_id: str = None, type:Enum = PostType.NORMAL.name) -> None:
        self.text = text
        self.user_id = user_id
        if parent_id is not None:
            self.parent_id = parent_id
        if type is not None:
            self.type = PostType[type]
        self.created_at = datetime.now().isoformat()
    
    def __str__(self) -> str:
        post_dict:dict = self.__dict__
        type = post_dict.pop("type")
        return json.dumps({**self.__dict__, "type": type})