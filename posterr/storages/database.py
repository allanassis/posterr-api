from typing import Union, List

from bson import ObjectId
from typeguard import typechecked

from pymongo.mongo_client import MongoClient
from pymongo.database import Database as MongoDb
from pymongo.results import InsertOneResult
from pymongo.cursor import Cursor

@typechecked
class DataBase:
    client: MongoClient
    db: MongoDb

    def __init__(self, name:str, host:str, port:int) -> None:
        self.client:MongoClient = MongoClient(host, port)
        self.db = self.client[name]

    def save(self, item:object, entity_name) -> str:
        item_dict:dict = item.__dict__
        result:InsertOneResult = self.db[entity_name].insert_one(item_dict)
        return str(result.inserted_id)

    def get_by_id(self, id: str, entity_name: str) -> Union[dict, None]:
        item = self.db[entity_name].find_one({ "_id": ObjectId(id) })
        return item

    def get_all(self, entity_name: str) ->  List[Union[dict, None]]:
        items:Cursor = self.db[entity_name].find({})
        return list(items)

    def healthcheck(self) -> None:
        info:dict = self.client.server_info()
        print("Database Mongodb is working!")
        print(f"Version {info['version']}")

