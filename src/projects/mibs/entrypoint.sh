#!/bin/sh

export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.8/site-packages:/usr/lib/python3.8/site-packages:/app:/app/lib/mibs/python/openapi:/app/lib/auth:/app/lib/logger

if [ "$1" == "test" ]; then
    export PYTHONPATH=$PYTHONPATH:/app/src
    python3 -m unittest discover
    python3 -m unittest discover -s lib/auth
else
    uwsgi --ini /app/uwsgi.ini &
    source /docker-entrypoint.sh
fi