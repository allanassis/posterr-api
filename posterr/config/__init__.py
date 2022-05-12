from os import environ, path
from xml.dom import NotFoundErr

from typeguard import typechecked
from vyper import Vyper

@typechecked
def init_config() -> Vyper:
    env:str = environ.get("ENV")
    if env is None:
        raise NotFoundErr()

    config_file_path:str = path.abspath("./config/")

    config:Vyper = Vyper(config_name=env)
    config.add_config_path(config_file_path)
    config.set_config_type("yml")
    config.set_env_prefix("POSTERR")

    config.read_in_config()
    config.automatic_env()
    config.watch_config()
    
    return config
