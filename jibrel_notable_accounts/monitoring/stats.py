import asyncio
import logging
import prometheus_client

from typing import Callable, Awaitable, Any, List

from jibrel_notable_accounts import settings
from jibrel_notable_accounts.parser.utils.proxy import Proxy, proxies

logger = logging.getLogger(__name__)


HealthChecker = Callable[..., Awaitable[bool]]


def _safe_health(func: HealthChecker) -> HealthChecker:
    """Returns 'False' if exception has been encountered."""
    async def wrapped(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.warning(f"Cannot fetch stats for '{func.__name__}'.", exc_info=True)

        return False

    return wrapped


@_safe_health
async def is_proxy_healthy() -> bool:
    proxies_count = len(proxies)
    proxies_faulty_count = get_proxies_faulty_count()
    proxy_health = round(1 - proxies_faulty_count / proxies_count, 2)

    return proxy_health >= settings.HEALTH_THRESHOLD_PROXY


@_safe_health
async def is_loop_healthy() -> bool:
    return len(asyncio.all_tasks()) < settings.HEALTH_THRESHOLD_LOOP_TASKS_COUNT


def get_proxies_faulty_count() -> int:
    proxies_faulty = [p for p in proxies if p.err > 0]
    proxies_faulty_count = len(proxies_faulty)

    return proxies_faulty_count


def setup_parser_metrics() -> None:
    _setup_loop_tasks_total_metric(settings.METRIC_PARSER_LOOP_TASKS_TOTAL)
    _setup_proxy_total_metric(settings.METRIC_PARSER_PROXY_TOTAL)
    _setup_proxy_faulty_total_metrics(settings.METRIC_PARSER_PROXY_FAULTY_TOTAL)


def _setup_loop_tasks_total_metric(name: str) -> None:
    loop_tasks_total = prometheus_client.Gauge(name, 'Total amount of tasks in the event loop.')
    loop_tasks_total.set_function(lambda: len(asyncio.all_tasks()))


def _setup_proxy_total_metric(name: str) -> None:
    proxy_total = prometheus_client.Gauge(name, 'Total amount of proxies.')
    proxy_total.set(len(proxies))


def _setup_proxy_faulty_total_metrics(name: str) -> None:
    proxy_faulty_total = prometheus_client.Gauge(name, 'Total amount of faulty proxies.')
    proxy_faulty_total.set_function(get_proxies_faulty_count)
