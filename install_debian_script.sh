#!/bin/bash

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

echo "Onyx Install"
echo "Dependencies Install"
echo "***"
apt-get -y update
apt-get -y install git jq dnsmasq build-essential python screen python-babel python-software-properties python-pip python-setuptools python-dev python-virtualenv openssl libssl-dev memcached python-memcache libmemcached-dev zlib1g-dev libffi-dev swig3.0 swig python-pygame sox python3-pyaudio libatlas-base-dev libportaudio2 libportaudiocpp0 portaudio19-dev flac mplayer mpg321

apt-get -y install nodejs npm
ln -s /usr/bin/nodejs /usr/bin/node
npm install -g pm2

#sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
#echo "deb http://repo.mongodb.org/apt/debian jessie/mongodb-org/3.4 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
#apt-get -y update
#apt-get install -y mongodb-org
