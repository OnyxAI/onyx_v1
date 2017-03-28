ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VIRTUALENV_ROOT=$(HOME)/.virtualenvs/onyx

all: setup

start:
	. $(VIRTUALENV_ROOT)/bin/activate; python manage.py run -h 0.0.0.0 -p 80 -d -r

test:
	. $(VIRTUALENV_ROOT)/bin/activate; py.test --color=yes

debug:
	. $(VIRTUALENV_ROOT)/bin/activate; python manage.py run -d -r -p 5000

prod:
	. $(VIRTUALENV_ROOT)/bin/activate; python manage.py run -p 80

run:
	. $(VIRTUALENV_ROOT)/bin/activate; python manage.py run -r

setup:
	. $(VIRTUALENV_ROOT)/bin/activate; pip install -Ur requirements.txt

init:
	export PYTHONPATH=$PYTHONPATH:ROOT_DIR

initdb:
	. $(VIRTUALENV_ROOT)/bin/activate; python manage.py init

migratedb:
	. $(VIRTUALENV_ROOT)/bin/activate; python manage.py migrate

babel:
	pybabel extract -F babel.cfg -o onyx/translations/messages.pot onyx

# run:
# $ LANG=en make addlang
addlang:
	. $(VIRTUALENV_ROOT)/bin/activate; pybabel init -i onyx/translations/messages.pot -d onyx/translations -l $(LANG)

compilelang:
	. $(VIRTUALENV_ROOT)/bin/activate; pybabel compile -d onyx/translations

updlang:
	. $(VIRTUALENV_ROOT)/bin/activate; pybabel update -i onyx/translations/messages.pot -d onyx/translations
