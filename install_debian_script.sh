#!/bin/bash

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

echo "Onyx Install"
echo "Dependencies Install"
echo "***"
apt-get -y update
apt-get -y install git jq dnsmasq build-essential python3 screen python3-babel python3-software-properties python3-pip python3-setuptools python3-dev python3-virtualenv openssl libssl-dev memcached python3-memcache libmemcached-dev zlib1g-dev libffi-dev swig3.0 swig python3-pygame sox python3-pyaudio libatlas-base-dev libportaudio2 libportaudiocpp0 portaudio19-dev flac mplayer mpg321

apt-get -y install nodejs npm
ln -s /usr/bin/nodejs /usr/bin/node
npm install -g pm2
