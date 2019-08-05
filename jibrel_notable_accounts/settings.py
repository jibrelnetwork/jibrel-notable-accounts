import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent
PROJECT_DIR = BASE_DIR / 'jibrel_notable_accounts'

PROXY_LIST_PATH = PROJECT_DIR / 'proxy.list'
USER_AGENT_LIST_PATH = PROJECT_DIR / 'useragents.list'


NOTABLE_ACCOUNTS_PARSE_ONCE_DELAY = int(os.environ['NOTABLE_ACCOUNTS_PARSE_ONCE_DELAY'])
REQUESTS_MAX_WORKERS = int(os.environ['REQUESTS_MAX_WORKERS'])


HTTP_FETCH_MAX_RETRIES = 5


ES_BASE_URL = 'https://etherscan.io'
ES_LABEL_CLOUD_URL = ES_BASE_URL + '/labelcloud'


PROXY_USER = os.environ['PROXY_USER']
PROXY_PASS = os.environ['PROXY_PASS']
PROXY_LIST = [p.strip() for p in open(PROXY_LIST_PATH, 'r').readlines()]

USER_AGENT_LIST = [u.strip() for u in open(USER_AGENT_LIST_PATH, 'r').readlines()]
