# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import sys
import traceback

import tornado.websocket
from pyee import EventEmitter

from onyx.util.log import getLogger
from onyx.api.assets import Json
from onyx.messagebus.message import Message

logger = getLogger(__name__)
json = Json()

EventBusEmitter = EventEmitter()

client_connections = []


class WebsocketEventHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        tornado.websocket.WebSocketHandler.__init__(
            self, application, request, **kwargs)
        self.emitter = EventBusEmitter

    def on(self, event_name, handler):
        self.emitter.on(event_name, handler)

    def on_message(self, message):
        logger.debug(message)
        try:
            deserialized_message = Message.deserialize(message)
        except:
            return

        try:
            self.emitter.emit(deserialized_message.type, deserialized_message)
        except Exception as e:
            logger.exception(e)
            traceback.print_exc(file=sys.stdout)
            pass

        for client in client_connections:
            client.write_message(message)

    def open(self):
        self.write_message(Message("connected").serialize())
        client_connections.append(self)

    def on_close(self):
        client_connections.remove(self)

    def emit(self, channel_message):
        if (hasattr(channel_message, 'serialize') and
                callable(getattr(channel_message, 'serialize'))):
            self.write_message(channel_message.serialize())
        else:
            self.write_message(json.encode(channel_message))

    def check_origin(self, origin):
        return True
