from typing import Union, List

from bson import ObjectId
from typeguard import typechecked

from pymongo.mongo_client import MongoClient
from pymongo.database import Database as MongoDb
from pymongo.results import InsertOneResult, UpdateResult
from pymongo import ASCENDING

@typechecked
class DataBase:
    client: MongoClient
    db: MongoDb

    def __init__(self, name:str, host:str, port:int) -> None:
        self.client:MongoClient = MongoClient(host, port)
        self.db = self.client[name]

    def save(self, item:object, collection: str) -> str:
        item_dict:dict = item.__dict__
        result:InsertOneResult = self.db[collection].insert_one(item_dict)
        return str(result.inserted_id)

    def update(self, item: object, collection:str) -> str:
        item_dict:dict = item.__dict__.copy()
        id = item_dict.pop("_id")
        result:UpdateResult = self.db[collection].update_one({"_id": ObjectId(id)}, {"$set" :item_dict})
        return id

    def get_by_id(self, id: str, collection: str) -> Union[dict, None]:
        item = self.db[collection].find_one({ "_id": ObjectId(id) })
        item["_id"] = str(item["_id"])
        return item

    def get_all(self, collection: str, filters: dict = {}, sort:list = [("$natural", ASCENDING)], limit:int = 1000) ->  List[Union[dict, None]]:
        items = self.db[collection].find(filters).sort(sort).limit(limit)
        item_list = list(items)
        for item in item_list:
            item["_id"] = str(item["_id"])
        return item_list

    def healthcheck(self) -> None:
        info:dict = self.client.server_info()
        print("Database Mongodb is working!")
        print(f"Version {info['version']}")
