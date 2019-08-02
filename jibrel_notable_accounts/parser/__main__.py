import click

import mode

from jibrel_notable_accounts.parser.services.parser import ParserService


@click.command()
def main():
    mode.Worker(ParserService()).execute_from_commandline()


if __name__ == '__main__':
    main()
