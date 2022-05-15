import json
from enum import Enum
from datetime import datetime

from typeguard import typechecked

from posterr.config import ConfigManager
from posterr.services.base import ServiceBase

class PostType(Enum):
    NORMAL = "normal"
    REPOSTED = "reposted"
    QUOTED = "quoted"

@typechecked
class Post(ServiceBase):
    _id: str
    type: Enum
    text: str
    user_id: str
    parent_id: str
    created_at: datetime

    entity_name:str = "post"

    def __init__(self, text: str = None, user_id: str = None, parent_id: str = None, type:str = PostType.NORMAL.name) -> None:
        maxium_size:int = ConfigManager().config.get_int("post.maximum_size")

        if text is not None and len(text) > maxium_size:
            raise ValueError(f"Post has a maximum lenght of {maxium_size}")
        if parent_id is not None:
            self.parent_id = parent_id
        if type is not None:
            self.type = PostType[type].value

        self.text = text
        self.user_id = user_id
        self.created_at = datetime.now()
    
    def __str__(self) -> str:
        date_format:int = ConfigManager().config.get_int("post.date_format")
        post_dict:dict = self.__dict__

        type:PostType = post_dict.pop("type")
        created_at:str = post_dict.pop("created_at").strftime(date_format) # ex May 24, 2021

        return json.dumps({ **self.__dict__, "type": type, "created_at": created_at })