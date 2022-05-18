from typeguard import typechecked
from vyper import Vyper

from posterr.api import init_api
from posterr.config import ConfigManager


@typechecked
def main() -> None:
    init_api()
