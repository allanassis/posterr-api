from typeguard import typechecked

from pymongo.mongo_client import MongoClient

@typechecked
class DataBase:
    client: MongoClient

    def __init__(self, host:str, port:int):
        self.client:MongoClient = MongoClient(host, port)

    def healthcheck(self):
        info:dict = self.client.server_info()
        print("Database Mongodb is working!")
        print(f"Version {info['version']}")

