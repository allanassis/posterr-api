from bson.objectid import ObjectId

from posterr.services.user import User
from posterr.storages.database import DataBase

class UserDao(object):
    
    def get_all(self, db: DataBase) -> User:
        items = db.get_all(User.entity_name)
        return items