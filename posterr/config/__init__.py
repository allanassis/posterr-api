from os import environ, path
from xml.dom import NotFoundErr

from typeguard import typechecked
from vyper import Vyper

@typechecked
class ConfigManager:
    _instances = {}
    config:Vyper = None

    def __init__(self) -> None:
        self.config = ConfigManager.init_config()

    # Singleton logic
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    @staticmethod
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
