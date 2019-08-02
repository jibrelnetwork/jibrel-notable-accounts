import dataclasses
import itertools
import logging

from jibrel_notable_accounts import settings

logger = logging.getLogger(__name__)


@dataclasses.dataclass()
class Proxy:
    host: str
    host_loggable: str
    err: int = 0
    cool: int = 0

    @classmethod
    def from_host(cls, host: str) -> "Proxy":
        return cls(
            host=f"https://{settings.PROXY_USER}:{settings.PROXY_PASS}@{host}",
            host_loggable=f"https://{settings.PROXY_USER}:{'*' * len(settings.PROXY_PASS)}@{host}",
        )

    def write_success(self) -> None:
        self.err = 0
        self.cool = 0

    def write_failure(self) -> None:
        self.err = self.cool = self.err + 1


proxies = [Proxy.from_host(host) for host in settings.PROXY_LIST]
proxies_cycle = itertools.cycle(proxies)


def next_proxy() -> Proxy:
    return next(proxies_cycle)


def get_cooled_proxy() -> Proxy:
    proxy = next_proxy()

    while proxy.err > 1 and proxy.cool > 0:
        proxy.cool -= 1
        proxy = next_proxy()

    logger.info("New proxy", extra={"host": proxy.host_loggable})

    return proxy
