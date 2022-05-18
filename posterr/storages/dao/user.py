import json

from posterr.config import ConfigManager
from posterr.services.user import User
from posterr.storages.cache import Cache
from posterr.storages.database import DataBase

class UserDao(object):

    def get_all(self, db: DataBase, cache: Cache) -> User:
        items = db.get_all(User.entity_name)
        return items

    def get_by_id(self, id:str, db: DataBase, cache: Cache) -> dict:
        item = cache.get(id)
        if item:
            dict_item = json.loads(item)
            return dict_item

        item:dict = db.get_by_id(id, User.entity_name)
        
        cache_ttl = ConfigManager().config.get_int("storages.cache.ttl")
        instance:User = User()
        user:User = User.build(instance, item)
        cache.set(id, str(user), cache_ttl)

        return item

    def update(self, user:User, db: DataBase, cache: Cache) -> object:
        result = db.update(user, User.entity_name)
        cache.delete(user._id)
        return result
    
    def save(self, user:User, db:DataBase, cache: Cache) -> str:
        result = db.save(user, User.entity_name)
        return result
    