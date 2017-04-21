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
  echo "usage: $0 [-h] (start [-v|-c]|stop|restart)"
  echo "      -h             this help message"
  echo "      start          starts onyx-client and onyx-voice"
  echo "      stop           stops onyx-client and onyx-voice"
  echo "      restart        restart onyx-client and onyx-voice"
  echo
  echo "screen tips:"
  echo "            run 'screen -list' to see all running screens"
  echo "            run 'screen -r <screen-name>' (e.g. 'screen -r onyx-client') to reatach a screen"
  echo "            press ctrl + a, ctrl + d to detace the screen again"
  echo "            See the screen man page for more details"
  echo
}

mkdir -p $DIR/logs

function verify-start {
    if ! screen -list | grep -q "$1";
    then
      echo "$1 failed to start. The log is below:"
      echo
      tail $DIR/logs/$1.log
    exit 1
    fi
}

function start-onyx {
  screen -mdS onyx-$1$2 -c $SCRIPTS/onyx-$1.screen $DIR/start.sh $1 $2
  sleep 1
  verify-start onyx-$1$2
  echo "Onyx $1$2 started"
}

function debug-start-onyx {
  screen -c $SCRIPTS/onyx-$1.screen $DIR/start.sh $1 $2
  sleep 1
  verify-start onyx-$1$2
  echo "Onyx $1$2 started"
}

function stop-onyx {
    if screen -list | grep -q "$1";
    then
      screen -XS onyx-$1 quit
      echo "Onyx $1 stopped"
    fi
}

function restart-onyx {
    if screen -list | grep -q "quiet";
    then
      $0 stop
      sleep 1
      $0 start
    elif screen -list | grep -q "cli" && ! screen -list | grep -q "quiet";
    then
      $0 stop
      sleep 1
      $0 start -c
    elif screen -list | grep -q "voice" && ! screen -list | grep -q "quiet";
    then
      $0 stop
      sleep 1
      $0 start -v
    else
      echo "An error occurred"
    fi
}

set -e

if [[ -z "$1" || "$1" == "-h" ]]
then
  usage
  exit 1
elif [[ "$1" == "start" && -z "$2" ]]
then
  start-onyx client
  start-onyx voice
  exit 0
elif [[ "$1" == "stop" && -z "$2" ]]
then
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
