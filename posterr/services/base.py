import typing

from posterr.storages.database import DataBase

class ServiceBase(object):

    entity_name:str = "base"

    def save(self, db: DataBase) -> str:
        inserted_id:str = db.save(self, self.entity_name)
        return inserted_id

    @staticmethod
    def get_all(Service: object, db: DataBase) -> typing.List[object]:
        items: typing.List[dict] = db.get_all(Service.entity_name)
        service_list:typing.List[object] = []
        for item in items:
            service:object = Service()
            service.build(item)
            service_list.append(service)
        return service_list
    
    @staticmethod
    def get_by_id(id: str, Service:object, db: DataBase) -> object:
        item:dict = db.get_by_id(id, Service.entity_name)
        service:object = Service()
        return service.build(item)
    
    def build(self, properties:dict) -> object:
        for k,v in properties.items():
            setattr(self, k, v)
        return self