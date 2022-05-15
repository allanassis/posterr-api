from typing import List
from datetime import datetime
from posterr.storages.database import DataBase
from posterr.services.post import Post

class PostDao(object):

    def __init__(self, queries:dict = {"limit": 10}):
        self.queries = queries

    #TODO: Adicionar limite maximo
    def get_all(self, db: DataBase) -> List[object]:
        query:dict = {}
        if self.queries["last_post_date"]:
            query["created_at"] = { "$lt": datetime.fromisoformat(self.queries["last_post_date"]) }

        return db.get_all(Post.entity_name, query, [("created_at", -1)], self.queries["limit"])
