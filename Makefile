all: setup

venv/bin/activate:
	if which virtualenv-3.5 >/dev/null; then virtualenv-3.5 venv; else virtualenv -p python3 venv; fi

start : python3 manage.py runserver -h 0.0.0.0 -p 80 -d -r

startdebug : venv/bin/activate requirements.txt
	. venv/bin/activate; python3 manage.py runserver -h 0.0.0.0 -p 80 -d -r

startprod : venv/bin/activate requirements.txt
	. venv/bin/activate; python3 manage.py runserver -h 0.0.0.0 -p 80

run: venv/bin/activate requirements.txt
	. venv/bin/activate; python3 manage.py runserver -h 0.0.0.0 -p 80 -d -r

setup: venv/bin/activate requirements.txt
	. venv/bin/activate; pip3 install -Ur requirements.txt

init: venv/bin/activate requirements.txt

initdb: venv/bin/activate
	. venv/bin/activate; python3 manage.py initdb

migratedb: venv/bin/activate
	. venv/bin/activate; python3 manage.py migratedb

babel: venv/bin/activate
	. venv/bin/activate; pybabel extract -F babel.cfg -o onyx/translations/messages.pot onyx

# lazy babel scan
lazybabel: venv/bin/activate
	. venv/bin/activate; pybabel extract -F babel.cfg -k lazy_gettext -o onyx/translations/messages.pot onyx

# run: 
# $ LANG=en make addlang
addlang: venv/bin/activate
	. venv/bin/activate; pybabel init -i onyx/translations/messages.pot -d onyx/translations -l $(LANG)

compilelang: venv/bin/activate
	. venv/bin/activate; pybabel compile -d onyx/translations

updlang: venv/bin/activate
	. venv/bin/activate; pybabel update -i onyx/translations/messages.pot -d onyx/translations

celery:
	. venv/bin/activate; python3 celery_run.py worker

# celery in debug state
dcelery:
	. venv/bin/activate; python3 celery_run.py worker -l info --autoreload
