from pickle import NONE
from typeguard import typechecked

from pymongo.mongo_client import MongoClient
from pymongo.database import Database

@typechecked
class DataBase:
    client: MongoClient
    db: Database

    def __init__(self, name:str, host:str, port:int):
        self.client:MongoClient = MongoClient(host, port)
        self.db = self.client[name]

    def save(self, item:object):
        item_dict:dict = dict(item)
        collection_name:str = format(item)
        result = self.db[collection_name].insert_one(item_dict)
        return str(result.inserted_id)

    def healthcheck(self):
        info:dict = self.client.server_info()
        print("Database Mongodb is working!")
        print(f"Version {info['version']}")

