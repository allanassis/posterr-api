from pymongo.mongo_client import MongoClient

class DataBase:
    def __init__(self, host, port):
        self.client = MongoClient(host, port)

    def healthcheck(self):
        info = self.client.server_info()
        print("Database Mongodb is working!")
        print(f"Version {info['version']}")

