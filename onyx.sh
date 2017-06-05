#!/usr/bin/env bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
SCRIPTS="$DIR/scripts"

function usage {
  echo
  echo "Quickly start, stop or restart Onyx' essential services in detached screens"
  echo
  echo "usage: $0 [-h] (start |stop|restart)"
  echo "      -h             this help message"
  echo "      start          starts onyx-service, onyx-skills, onyx-client and onyx-voice"
  echo "      stop           stops onyx-service, onyx-skills, onyx-client and onyx-voice"
  echo "      restart        restart onyx-service, onyx-skills, onyx-client and onyx-voice"
  echo
  echo "screen tips:"
  echo "            run 'screen -list' to see all running screens"
  echo "            run 'screen -r <screen-name>' (e.g. 'screen -r onyx-client') to reatach a screen"
  echo "            press ctrl + a, ctrl + d to detace the screen again"
  echo "            See the screen man page for more details"
  echo
}


function start-onyx {
  pm2 start $DIR/start.sh --name onyx-$1$2 -x -- $1 $2
  sleep 1
  echo "Onyx $1$2 started"
}

function debug-start-onyx {
  screen -c $SCRIPTS/onyx-$1.screen $DIR/start.sh $1 $2
  sleep 1
  verify-start onyx-$1$2
  echo "Onyx $1$2 started"
}

function stop-onyx {
    if pm2 list | grep -q "$1";
    then
      pm2 stop onyx-$1
      echo "Onyx $1 stopped"
    fi
}

function restart-onyx {
    pm2 restart all
}

set -e

if [[ -z "$1" || "$1" == "-h" ]]
then
  usage
  exit 1
elif [[ "$1" == "start" && -z "$2" ]]
then
  start-onyx service
  start-onyx skills
  start-onyx client
  start-onyx voice

  exit 0
elif [[ "$1" == "stop" && -z "$2" ]]
then
  stop-onyx service
  stop-onyx skills
  stop-onyx client
  stop-onyx voice
  exit 0
elif [[ "$1" == "restart" && -z "$2" ]]
then
  restart-onyx
  exit 0
else
  usage
  exit 1
fi
