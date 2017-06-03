#!/usr/bin/env bash
TOP=$(cd $(dirname $0) && pwd -L)
VIRTUALENV_ROOT=${VIRTUALENV_ROOT:-"${TOP}/venv-$1"}

case $2 in
	"client") SCRIPT=${TOP}/run.py ;;
	"service") SCRIPT=${TOP}/onyx/messagebus/service/main.py ;;
	"skills") SCRIPT=${TOP}/onyx/skills/main.py ;;
	"skill_container") SCRIPT=${TOP}/onyx/skills/container.py ;;
	"kernel") SCRIPT=${TOP}/onyx/api/kernel/__init__.py ;;
	"voice") SCRIPT=${TOP}/onyx/client/speech/main.py ;;
	"skills") SCRIPT=${TOP}/onyx/skills/main.py ;;
	"wifi") SCRIPT=${TOP}/onyx/client/wifisetup/main.py ;;
	*) echo "Usage: start.sh [prod | dev] [service | kernel | client | voice | skills | wifi]"; exit ;;
esac

echo "Starting $@"

shift

source ${VIRTUALENV_ROOT}/bin/activate
PYTHONPATH=${TOP} python ${SCRIPT} $@
