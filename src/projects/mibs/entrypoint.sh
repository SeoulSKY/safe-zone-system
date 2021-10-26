#!/bin/sh

export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.8/site-packages:/usr/lib/python3.8/site-packages:/app:/app/lib/mibs/python/openapi
uwsgi --ini /app/uwsgi.ini &
source /docker-entrypoint.sh