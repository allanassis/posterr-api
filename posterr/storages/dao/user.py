from posterr.services.user import User
from posterr.storages.database import DataBase

class UserDao(object):

    def get_all(self, db: DataBase) -> User:
        items = db.get_all(User.entity_name)
        return items

    def get_by_id(self, id:str, db: DataBase) -> dict:
        return db.get_by_id(id, User.entity_name)

    def update(self, user:User, db: DataBase) -> object:
        result = db.update(user, User.entity_name)
        return result
    
    def save(self, user:User, db:DataBase) -> str:
        result = db.save(user, User.entity_name)
        return result
    