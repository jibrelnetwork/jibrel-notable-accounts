from typing import List

import jibrel_notable_accounts.parser.__main__
import mode
import pytest
from click.testing import CliRunner
from pytest_mock import MockFixture

CODE_OK = 0
CODE_ERROR = 1
CODE_ERROR_FROM_CLICK = 2


@pytest.fixture()
def _mock_execute(mocker: MockFixture) -> None:
    mocker.patch.object(mode.Worker, 'execute_from_commandline')


@pytest.mark.usefixtures('_mock_execute')
@pytest.mark.parametrize(
    'call_args, exit_code',
    [
        ([], CODE_OK),
        (['invalid', 'set', 'of', 'args'], CODE_ERROR_FROM_CLICK),
        (['--log-level', 'ERROR', '--no-json-formatter', '--update-if-exists'], CODE_OK),
    ],
    ids=[
        "no args",
        "invalid args",
        "all args",
    ]
)
async def test_parser_entrypoint(
        cli_runner: CliRunner,
        call_args: List[str],
        exit_code: int,
) -> None:
    assert cli_runner.invoke(jibrel_notable_accounts.parser.__main__.main, call_args).exit_code == exit_code
