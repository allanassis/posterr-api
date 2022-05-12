from posterr.api import init_api
from posterr.config import init_config

def main():
    config = init_config()
    init_api(config)

main()