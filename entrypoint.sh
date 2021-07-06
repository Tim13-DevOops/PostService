#!/bin/sh
# wait-for-postgres.sh
  

if [ "$DATABASE" = "postgres" ]
then
  echo "Waiting for postgres..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 2
  done

  echo "PostgreSQL started"
fi

if [ "$COMMAND" = "test" ]
then
  coverage run setup.py test
  coverage xml --include="app/*" -o coverage_reports/coverage.xml
elif [ "$COMMAND" = "run_server" ]
then
  python setup.py install
  flask_migrate
  start_server
fi

exec "$@"

