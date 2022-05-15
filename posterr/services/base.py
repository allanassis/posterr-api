import typing

from typeguard import typechecked

from posterr.storages.database import DataBase

@typechecked
class ServiceBase(object):

    entity_name:str = "base"

    def save(self, db: DataBase) -> str:
        inserted_id:str = db.save(self, self.entity_name)
        return inserted_id

    @classmethod
    def get_all(Class: object, dao: object, db: DataBase) -> typing.List[object]:
        items: typing.List[dict] = dao.get_all(db)
        service_list:typing.List[object] = []

        for item in items:
            service:object = Class()
            service.build(item)
            service_list.append(service)

        return service_list
    
    @classmethod
    def get_by_id(Class:object, id: str, dao:object, db: DataBase) -> object:
        item:dict = dao.get_by_id(id, db)
        service:object = Class()

        return service.build(item)
    
    def build(self, properties:dict) -> object:
        for k,v in properties.items():
            setattr(self, k, v)

        return self