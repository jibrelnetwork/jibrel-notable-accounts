import pytest
from aiohttp.test_utils import TestClient


@pytest.mark.parametrize(
    ('name', 'expected'),
    (
            ('Access-Control-Allow-Headers', '*'),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Request-Method', 'POST, GET, OPTIONS, HEAD'),
    )
)
async def test_cors_headers_are_present_for_parser(parser_cli: TestClient, name: str, expected: str) -> None:
    response = await parser_cli.get('/healthcheck')
    response_header = response.headers[name]

    assert response_header == expected
