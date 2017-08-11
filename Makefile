ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VIRTUALENV_ROOT=$(ROOT_DIR)/venv
PYTHON=python

all: setup

start:
	. $(VIRTUALENV_ROOT)/bin/activate; $(PYTHON) manage.py run -h 0.0.0.0 -p 80 -d -r

test:
	. $(VIRTUALENV_ROOT)/bin/activate; py.test tests/ --color=yes

debug:
	. $(VIRTUALENV_ROOT)/bin/activate; $(PYTHON) manage.py run -d -r -p 5000

prod:
	. $(VIRTUALENV_ROOT)/bin/activate; $(PYTHON) manage.py run -p 80

run:
	. $(VIRTUALENV_ROOT)/bin/activate; $(PYTHON) manage.py run -r

setup:
	bash dev_setup.sh

init:
	export PYTHONPATH=$PYTHONPATH:ROOT_DIR

initdb:
	. $(VIRTUALENV_ROOT)/bin/activate; $(PYTHON) manage.py db init

migratedb:
	. $(VIRTUALENV_ROOT)/bin/activate; $(PYTHON) manage.py db migrate

babel:
	pybabel extract -F babel.cfg -o onyx/translations/messages.pot onyx

# run:
# $ LANG=en make addlang
addlang:
	pybabel init -i onyx/translations/messages.pot -d onyx/translations -l $(LANG)

compilelang:
	pybabel compile -d onyx/translations

updlang:
	pybabel update -i onyx/translations/messages.pot -d onyx/translations
