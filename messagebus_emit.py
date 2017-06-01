import sys
import os
sys.path.append("/home/pi/Onyx")
from onyx.messagebus.client.ws import WebsocketClient
from onyx.messagebus.message import Message

messageToSend = sys.argv



def onConnected(event=None):
    print ("Sending message...'" + messageToSend + "'")
    messagebusClient.emit(Message(messageToSend))
    messagebusClient.close()
    exit()


# Establish a connection with the messagebus
messagebusClient = WebsocketClient()
messagebusClient.on('connected', onConnected)


# This will block until the client gets closed
messagebusClient.run_forever()
