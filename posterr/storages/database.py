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

    def healthcheck(self):
        info:dict = self.client.server_info()
        print("Database Mongodb is working!")
        print(f"Version {info['version']}")

