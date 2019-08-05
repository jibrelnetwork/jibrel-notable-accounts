from aiohttp.test_utils import TestClient
from aiohttp.web_app import Application
from typing import Callable, Any, Awaitable

AiohttpClient = Callable[[Application], Awaitable[TestClient]]
SettingsOverrider = Callable[[str, Any], None]
ProxiesSetter = Callable[[bool], None]

HtmlGetter = Callable[[str], str]
