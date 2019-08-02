from typing import NamedTuple, Tuple, Any, Dict


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

    def as_dict(self) -> Dict[str, Any]:
        return {
            'address': self.address,
            'name': self.name,
            'labels': list(self.labels),
        }


class AccountList(NamedTuple):
    url: str
    label: str
