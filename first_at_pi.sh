#!/bin/bash

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

echo "Onyx Install"
echo "***"
pip install -U cffi
pip install pip gunicorn

sed -i '/exit 0/d' "/etc/rc.local"
echo "sudo pip install --upgrade onyxproject &" >> "/etc/rc.local"
echo "sudo gunicorn -b 0.0.0.0:80 onyx.wsgi:app &" >> "/etc/rc.local"
echo "exit 0" >> "/etc/rc.local"
