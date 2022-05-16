from typing import List
from datetime import datetime
from posterr.config import ConfigManager
from posterr.storages.database import DataBase
from posterr.services.post import Post

class PostDao(object):

    def __init__(self, queries:dict = {"limit": 10}):
        self.queries = queries

    #TODO: Adicionar limite maximo
    def get_all(self, db: DataBase) -> List[dict]:
        maximum_page_size:int = ConfigManager().config.get_int("post.maximum_page_size") #I know it is not on requiments of project, but i think is really needed because of DOS or DDOS
        query:dict = {}

        page_size = self.queries["limit"]
        last_post_id = self.queries.get("last_post_id")

        if page_size > maximum_page_size:
            raise ValueError(f"The limit for each page of posts is {maximum_page_size}")
        if last_post_id:
            last_post:object = Post.get_by_id(last_post_id, PostDao(), db)
            query["created_at"] = { "$lt": last_post.created_at }

        if self.queries.get("following_list"):
            query["user_id"] = {"$in": self.queries["following_list"] }

        return db.get_all(Post.entity_name, query, [("created_at", -1)], self.queries["limit"])

    def get_by_id(self, id:str, db: DataBase) -> dict:
        return db.get_by_id(id, Post.entity_name)
    
    def save(self, post:Post, db:DataBase) -> str:
        result = db.save(post, Post.entity_name)
        return result