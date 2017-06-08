# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import socket
import subprocess
import tempfile

import os
import os.path
import psutil
from os.path import dirname
from onyx.util.log import getLogger
from onyx.config import get_config

LOG = getLogger(__name__)
config = get_config('onyx')

def record(file_path, duration, rate, channels):
    if duration > 0:
        return subprocess.Popen(
            ["arecord", "-r", str(rate), "-c", str(channels), "-d",
             str(duration), file_path])
    else:
        return subprocess.Popen(
            ["arecord", "-r", str(rate), "-c", str(channels), file_path])

def play_wav(uri):
    play_cmd = config.get("Sound", "wav")
    play_wav_cmd = str(play_cmd).split(" ")
    for index, cmd in enumerate(play_wav_cmd):
        if cmd == "#1":
            play_wav_cmd[index] = (get_http(uri))
    return subprocess.Popen(play_wav_cmd)


def play_mp3(uri):
    play_cmd = config.get("Sound", "mp3")
    play_mp3_cmd = str(play_cmd).split(" ")
    for index, cmd in enumerate(play_mp3_cmd):
        if cmd == "#1":
            play_mp3_cmd[index] = (get_http(uri))
    return subprocess.Popen(play_mp3_cmd)

def get_http(uri):
    return uri.replace("https://", "http://")

def connected(host="8.8.8.8", port=53, timeout=3):
    """
    Thanks to 7h3rAm on
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except IOError:
        try:
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
                ("8.8.4.4", port))
            return True
        except IOError:
            return False

def create_signal(signal_name):
    try:
        with open(tempfile.gettempdir() + '/' + signal_name, 'w'):
            return True
    except IOError:
        return False


def check_for_signal(signal_name):
    filename = tempfile.gettempdir() + '/' + signal_name
    if os.path.isfile(filename):
        os.remove(filename)
        return True
    return False


def validate_param(value, name):
    if not value:
        raise ValueError("Missing or empty %s in onyx.cfg " % name)
