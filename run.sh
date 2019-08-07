#!/bin/sh -e

echo "Starting Jibrel Notable Accounts service, mode '$1' version: $(cat /app/version.txt) on node $(hostname)"

wait_db_ready () {
    dockerize -wait tcp://"$(python -c 'import dsnparse; p = dsnparse.parse_environ("DB_DSN"); print(p.hostloc)')"
}

if [ "$1" = "jibrel-notable-accounts-parser" ]; then
    wait_db_ready
fi

exec "$@"
