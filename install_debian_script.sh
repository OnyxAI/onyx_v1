#!/bin/bash

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

echo "Onyx Install"
echo "Dependencies Install"
echo "***"
apt-get --assume-yes update
apt-get --assume-yes install build-essential python python-software-properties python-pip python-setuptools python-dev python-virtualenv openssl libssl-dev memcached python-memcache libmemcached-dev zlib1g-dev libffi-dev swig3.0 swig python-pygame python-pyaudio python3-pyaudio sox libatlas-base-dev libportaudio2 libportaudiocpp0 portaudio19-dev flac mplayer
