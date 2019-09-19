from typing import NamedTuple, Callable, Awaitable


class Healthchecker(NamedTuple):
    key: str
    func: Callable[[], Awaitable[bool]]
