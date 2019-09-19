#!/bin/sh -e

echo "Starting Jibrel Notable Accounts service, mode '$1' version: $(cat /app/version.txt) on node $(hostname)"

wait_db_ready () {
    dockerize -wait tcp://"$(python -c 'import dsnparse; p = dsnparse.parse_environ("DB_DSN"); print(p.hostloc)')"
}

migrate_db () {
    alembic upgrade head
}


if [ "$1" = "jibrel-notable-accounts-parser" ]; then
    wait_db_ready
    migrate_db
elif [ "$1" = "app" ]; then
    wait_db_ready
    migrate_db
elif [ "$1" = "admin" ]; then
    wait_db_ready
    migrate_db
fi


if [ "$1" = "app" ]; then
    gunicorn -c gunicorn-conf.py jibrel_notable_accounts.api.app:make_app
elif [ "$1" = "admin" ]; then
    gunicorn -c gunicorn-conf-admin.py jibrel_notable_accounts.admin.app:app
else
    exec "$@"
fi
