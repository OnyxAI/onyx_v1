#!/usr/bin/env bash
python manage.py runserver -h 0.0.0.0 -p 8080 -d -r > /dev/null &
nosetests --with-coverage