#!/usr/bin/env bash
TOP=$(cd $(dirname $0) && pwd -L)
VIRTUALENV_ROOT=${VIRTUALENV_ROOT:-"${TOP}/venv"}

case $1 in
	"client") SCRIPT="${TOP}/manage.py run -h 0.0.0.0 -p 8080" ;;
	"service") SCRIPT=${TOP}/onyx/sockyx/service/main.py ;;
	"skills") SCRIPT=${TOP}/onyx/skills/main.py ;;
	"voice") SCRIPT=${TOP}/onyx/client/speech/main.py ;;
	"wifi") SCRIPT=${TOP}/onyx/client/wifisetup/main.py ;;
	"cli") SCRIPT=${TOP}/onyx/client/cli/main.py ;;
	*) echo "Usage: start.sh [service | cli | client | voice | skills | wifi]"; exit ;;
esac

echo "Starting $1"

shift

source ${VIRTUALENV_ROOT}/bin/activate
PYTHONPATH=${TOP} ${VIRTUALENV_ROOT}/bin/python ${SCRIPT} $@
