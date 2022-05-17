import logging

from redis import Redis

class Cache(object):
    client: Redis
    def __init__(self, host:str, port:int) -> None:
        self.client:Redis = Redis(host=host, port=port, db=0)
    
    def set(self, key: str, value:str, ttl: int) -> bool:
        return self.client.setex(key, ttl, value)

    def get(self, key:str) -> str:
        return self.client.get(key)
    
    def healthcheck(self):
        self.client.ping()
        logging.info("Cache redis server is working!")
        logging.info(self.client.info()['redis_version'])