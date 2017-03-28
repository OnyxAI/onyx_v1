#!/usr/bin/env bash
TOP=$(cd $(dirname $0) && pwd -L)
VIRTUALENV_ROOT=${VIRTUALENV_ROOT:-"${HOME}/.virtualenvs/onyx"}

case $1 in
	"client") SCRIPT=${TOP}/run.py ;;
	"voice") SCRIPT=${TOP}/onyx/client/speech/main.py ;;
	"skills") SCRIPT=${TOP}/onyx/skills/main.py ;;
	*) echo "Usage: start.sh [client | voice | skills]"; exit ;;
esac

echo "Starting $@"

shift

source ${VIRTUALENV_ROOT}/bin/activate
PYTHONPATH=${TOP} python ${SCRIPT} $@
