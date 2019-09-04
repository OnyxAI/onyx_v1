# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from onyx.api.assets import Json
import onyx, sys, os, time
from onyx.config import get_config
from onyxbabel import gettext
from onyx.util.log import getLogger
from onyx.skills.core import OnyxSkill

config = get_config('onyx')

global ws

import threading
from threading import Thread

from onyx.messagebus.client.ws import WebsocketClient
from onyx.messagebus.message import Message

skills = OnyxSkill(name="cli")

json = Json()
LOG = getLogger('Client')

def handle_speak(event):
    utterance = event.data.get('utterance')
    print(">> " + utterance)

def handle_finish(event):
    print("Finish")

def connect():
    # Once the websocket has connected, just watch it for speak events
    ws.run_forever()

ws = WebsocketClient()
ws.on('speak', handle_speak)
ws.on('finish', handle_finish)
event_thread = Thread(target=connect)
event_thread.setDaemon(True)
event_thread.start()


def cli():
    while True:
        try:
            time.sleep(1.5)
            result = input('You: ')

            print ("Sending message...")
            payload = {
                'utterances': [result]
            }
            ws.emit(Message('recognizer_loop:utterance', payload))

        except (KeyboardInterrupt, EOFError, SystemExit):
            break

cli()
