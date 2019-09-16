from typing import NamedTuple, Tuple


class RawNotableAccount(NamedTuple):
    """Account, parsed from a single page."""
    address: str
    name: str
    label: str


class NotableAccount(NamedTuple):
    """Account, with data, aggregated from multiple pages."""
    address: str
    name: str
    labels: Tuple[str, ...]


class AccountList(NamedTuple):
    url: str
    label: str
