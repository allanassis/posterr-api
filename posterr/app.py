from vyper import Vyper

from posterr.api import init_api
from posterr.config import init_config

def main():
    config:Vyper = init_config()
    init_api(config)
