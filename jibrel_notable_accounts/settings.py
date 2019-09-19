import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent
PROJECT_DIR = BASE_DIR / 'jibrel_notable_accounts'

PROXY_LIST_PATH = PROJECT_DIR / 'proxy.list'
USER_AGENT_LIST_PATH = PROJECT_DIR / 'useragents.list'

LOG_LEVEL = os.environ['LOG_LEVEL']
NO_JSON_FORMATTER = bool(int(os.environ['NO_JSON_FORMATTER']))
UPDATE_IF_EXISTS = bool(int(os.environ['UPDATE_IF_EXISTS']))

DB_DSN = os.environ['DB_DSN']
SENTRY_DSN = os.environ['SENTRY_DSN']

NOTABLE_ACCOUNTS_PARSE_ONCE_DELAY = int(os.environ['NOTABLE_ACCOUNTS_PARSE_ONCE_DELAY'])
REQUESTS_MAX_WORKERS = int(os.environ['REQUESTS_MAX_WORKERS'])


HTTP_FETCH_MAX_RETRIES = 5


ES_BASE_URL = 'https://etherscan.io'
ES_LABEL_CLOUD_URL = ES_BASE_URL + '/labelcloud'


PROXY_USER = os.environ['PROXY_USER']
PROXY_PASS = os.environ['PROXY_PASS']
PROXY_LIST = [p.strip() for p in open(PROXY_LIST_PATH, 'r').readlines()]

USER_AGENT_LIST = [u.strip() for u in open(USER_AGENT_LIST_PATH, 'r').readlines()]


ADMIN_BASIC_AUTH_FORCE = bool(int(os.environ['ADMIN_BASIC_AUTH_FORCE']))
ADMIN_BASIC_AUTH_USERNAME = os.environ['ADMIN_BASIC_AUTH_USERNAME']
ADMIN_BASIC_AUTH_PASSWORD = os.environ['ADMIN_BASIC_AUTH_PASSWORD']
ADMIN_SECRET_KEY = os.environ['ADMIN_SECRET_KEY']
ADMIN_UI_THEME = os.environ['ADMIN_UI_THEME']


METRIC_API_LOOP_TASKS_TOTAL = 'jibrel_notable_accounts_api_loop_tasks_total'

METRIC_PARSER_LOOP_TASKS_TOTAL = 'jibrel_notable_accounts_parser_loop_tasks_total'
METRIC_PARSER_PROXY_TOTAL = 'jibrel_notable_accounts_parser_proxy_total'
METRIC_PARSER_PROXY_FAULTY_TOTAL = 'jibrel_notable_accounts_parser_proxy_faulty_total'


API_PORT_PARSER = int(os.environ['API_PORT_PARSER'])


HEALTH_THRESHOLD_PROXY = 0.7
HEALTH_THRESHOLD_LOOP_TASKS_COUNT = 10000
