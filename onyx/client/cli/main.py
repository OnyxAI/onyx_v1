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

import threading

from onyx.messagebus.client.ws import WebsocketClient
from onyx.messagebus.message import Message

skills = OnyxSkill(name="cli")

json = Json()
LOG = getLogger('CliClient')

def ws():
    def speak_cli(self, message):
        print("Onyx:" + str(message))
    
    ws = WebsocketClient()
    ws.on('speak', speak_cli)
    ws.run_forever()
        
th = threading.Thread(target=ws)
th.start()    

while True:
    try:
        result = raw_input('You: ')
        print("You said: " + str(result))
        
        def create_ws():
			def onConnected(event=None):
			    print ("Sending message...")
			    payload = {
			        'utterances': [result]
			       
			    }
			    ws.emit(Message('recognizer_loop:utterance', payload))
			    t.close()
			    
			ws = WebsocketClient()
			ws.on('connected', onConnected)
			ws.run_forever()
        
        t = threading.Thread(target=create_ws)
        t.start()
        time.sleep(2)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break