ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

all: setup

start:
	python manage.py run -h 0.0.0.0 -p 80 -d -r

test:
	py.test --color=yes

debug:
	python manage.py run -d -r -p 5000

prod:
	python manage.py run -p 80

run:
	python manage.py run

setup:
	pip install -Ur requirements.txt

init:
	export PYTHONPATH=$PYTHONPATH:ROOT_DIR

initdb:
	python manage.py init

migratedb:
	python manage.py migrate

babel:
	pybabel extract -F babel.cfg -o onyx/translations/messages.pot onyx

# lazy babel scan
lazybabel:
	pybabel extract -F babel.cfg -k lazy_gettext -o onyx/translations/messages.pot onyx

# run:
# $ LANG=en make addlang
addlang:
	pybabel init -i onyx/translations/messages.pot -d onyx/translations -l $(LANG)

compilelang:
	pybabel compile -d onyx/translations

updlang:
	pybabel update -i onyx/translations/messages.pot -d onyx/translations

celery:
	python celery_run.py worker

# celery in debug state
dcelery:
	 python celery_run.py worker -l info --autoreload
