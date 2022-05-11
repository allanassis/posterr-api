from pymongo.mongo_client import MongoClient

class DataBase:
    def __init__(self):
        self.client = MongoClient("172.19.0.3", 27017)

    def healthcheck(self):
        info = self.client.server_info()
        print("Database Mongodb is working!")
        print(f"Version {info['version']}")

