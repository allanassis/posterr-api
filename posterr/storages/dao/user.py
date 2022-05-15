from posterr.services.user import User
from posterr.storages.database import DataBase

class UserDao(object):

    def get_all(self, db: DataBase) -> User:
        items = db.get_all(User.entity_name)
        return items

    def get_by_id(self, id:str, db: DataBase) -> dict:
        return db.get_by_id(id, User.entity_name)
    