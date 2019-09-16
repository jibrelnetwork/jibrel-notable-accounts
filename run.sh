#!/bin/sh -e

echo "Starting Jibrel Notable Accounts service, mode '$1' version: $(cat /app/version.txt) on node $(hostname)"

wait_db_ready () {
    dockerize -wait tcp://"$(python -c 'import dsnparse; p = dsnparse.parse_environ("DB_DSN"); print(p.hostloc)')"
}

if [ "$1" = "jibrel-notable-accounts-parser" ]; then
    wait_db_ready
elif [ "$1" = "app" ]; then
    wait_db_ready
fi


if [ "$1" = "app" ]; then
    gunicorn -c gunicorn-conf.py jibrel_notable_accounts.api.app:make_app
else
    exec "$@"
fi
