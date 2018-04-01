#!/bin/sh
flask db upgrade
flask seed-db
exec gunicorn -b :5000 --access-logfile - --error-logfile - flaskuniversity:app
