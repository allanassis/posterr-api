from typing import List

from typeguard import typechecked
from posterr.storages.cache import Cache

from posterr.storages.database import DataBase

@typechecked
class ServiceBase(object):

    entity_name:str = "base"

    def save(self, dao: object, db: DataBase, cache:Cache) -> str:
        inserted_id:str = dao.save(self, db, cache)
        return inserted_id

    @classmethod
    def get_all(Class: object, dao: object, db: DataBase, cache: Cache) -> List[object]:
        items: List[dict] = dao.get_all(db, cache)
        service_list:List[object] = []

        for item in items:
            service:object = Class()
            service.build(item)
            service_list.append(service)

        return service_list
    
    @classmethod
    def get_by_id(Class:object, id: str, dao:object, db: DataBase, cache: Cache) -> object:
        item:dict = dao.get_by_id(id, db, cache)
        service:object = Class()

        return service.build(item)
    
    def build(self, properties:dict) -> object:
        for k,v in properties.items():
            setattr(self, k, v)

        return self