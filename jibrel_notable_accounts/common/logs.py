import logging.config
import sys

from typing import Dict, Any


def get_formatter_class(no_json_formatter: bool) -> str:
    if no_json_formatter:
        return 'logging.Formatter'

    return 'pythonjsonlogger.jsonlogger.JsonFormatter'


def get_config(log_level: str, formatter_class: str) -> Dict[str, Any]:
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'class': formatter_class,
                'format': '%(asctime)-15s %(levelname)-8s %(name)s: %(message)s',
            }
        },
        'handlers': {
            'console': {
                '()': 'logging.StreamHandler',
                'stream': sys.stdout,
                'formatter': 'default'
            },
        },
        'loggers': {
            '': {
                'level': log_level,
                'handlers': ['console']
            }
        }
    }


def configure(log_level: str, no_json_formatter: bool) -> None:
    logging.config.dictConfig(
        get_config(
            log_level=log_level,
            formatter_class=get_formatter_class(no_json_formatter),
        )
    )
