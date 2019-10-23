#!/bin/bash

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

echo "Onyx Install"
echo "Dependencies Install"
echo "***"
apt-get -y update
apt-get -y install build-essential python3 python3-software-properties python3-pip python3-setuptools python3-dev python3-virtualenv openssl libssl-dev memcached python3-memcache libmemcached-dev zlib1g-dev libffi-dev

TOP=$(cd $(dirname $0) && pwd -L)

if [ ! -f ${TOP}/onyx/app_config.py ]; then
    echo "App Config not found!"
    echo "Create App Config"
    cp ${TOP}/onyx/config_example.py ${TOP}/onyx/app_config.py
fi

if [ ! -f ${TOP}/onyx/config/onyx.cfg ]; then
    echo "Config not found!"
    echo "Create Config"
    cp ${TOP}/onyx/config/onyx_example.cfg ${TOP}/onyx/config/onyx.cfg
fi

make compilelang

arch=$(arch)
os=$(uname -s)

cd ${TOP}/onyx/client/speech/assets

if [ ! -f ${TOP}/onyx/client/speech/assets/_snowboydetect.so ] || [ ! -f ${TOP}/onyx/client/speech/assets/snowboydetect.py ]; then
    echo "Snowboy not found not found!"
    echo "Download Snowboy"
    wget http://download.onyxlabs.fr/snowboy/snowboy_${os}_${arch}.tar.gz
    tar zxvf snowboy_${os}_${arch}.tar.gz
    rm snowboy_${os}_${arch}.tar.gz
fi

mkdir $HOME/skills
