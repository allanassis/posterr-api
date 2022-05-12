import os


from os import environ
import os
from xml.dom import NotFoundErr

from vyper import Vyper

def init_config():
    env = environ.get("ENV")
    if env is None:
        raise NotFoundErr()

    config_file_path = os.path.abspath("./config/")

    config = Vyper(config_name=env)
    config.add_config_path(config_file_path)
    config.set_config_type("yml")
    config.set_env_prefix("POSTERR")

    config.read_in_config()
    config.automatic_env()
    config.watch_config()
    
    return config
