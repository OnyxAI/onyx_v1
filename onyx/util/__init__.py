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

LOGGER = getLogger(__name__)
config = get_config('onyx')


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
