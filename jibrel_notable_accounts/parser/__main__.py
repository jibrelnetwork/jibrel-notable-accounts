import click
import mode
import sentry_sdk

from jibrel_notable_accounts import settings
from jibrel_notable_accounts.common import logs
from jibrel_notable_accounts.parser.app import make_app
from jibrel_notable_accounts.common.api import ApiService
from jibrel_notable_accounts.monitoring.stats import setup_parser_metrics
from jibrel_notable_accounts.parser.service import ParserService


@click.command()
@click.option('--log-level', default=settings.LOG_LEVEL, help="Log level")
@click.option('--no-json-formatter', is_flag=True, default=settings.NO_JSON_FORMATTER, help='Use default formatter')
@click.option('--update-if-exists', is_flag=True, default=settings.UPDATE_IF_EXISTS, help='Update account if exists')
def main(log_level: str, update_if_exists: bool, no_json_formatter: bool) -> None:
    sentry_sdk.init(settings.RAVEN_DSN)
    setup_parser_metrics()

    mode.Worker(
        ParserService(db_dsn=settings.DB_DSN, update_if_exists=update_if_exists),
        ApiService(port=settings.API_PORT_PARSER, app_maker=make_app),
        loglevel=log_level,
        logging_config=logs.get_config(
            log_level=log_level,
            formatter_class=logs.get_formatter_class(no_json_formatter),
        )
    ).execute_from_commandline()


if __name__ == '__main__':
    main()
