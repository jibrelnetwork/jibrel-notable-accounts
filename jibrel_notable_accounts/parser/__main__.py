import click
import mode

from jibrel_notable_accounts import settings
from jibrel_notable_accounts.monitoring.app import make_app
from jibrel_notable_accounts.monitoring.service import ApiService
from jibrel_notable_accounts.parser.service import ParserService


@click.command()
def main():
    mode.Worker(
        ParserService(),
        ApiService(port=settings.API_PORT_PARSER, app_maker=make_app),
    ).execute_from_commandline()


if __name__ == '__main__':
    main()
