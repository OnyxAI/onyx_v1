import sys
from onyx.messagebus.client.ws import WebsocketClient
from onyx.messagebus.message import Message

if len(sys.argv) == 2:
    messageToSend = sys.argv[1]
elif len(sys.argv) > 2:
    messageToSend = " ".join(sys.argv[2:])
else:
    filename = os.path.basename(__file__)
    print (filename)
    print ("Simple command line interface to the messagebus.")
    print ("Usage:   messagebus_emit <utterance>\n")
    print ("         where <utterance> is treated as if spoken to Onyx.")
    print ("Example: " + filename + " onyx.wifi.start")
    exit()

def onConnected(event=None):
    print ("Sending message...")
    payload = {
            'utterances': [messageToSend]
    }
    messagebusClient.emit(Message('recognizer_loop:utterance', payload))
    messagebusClient.close()
    exit()


# Establish a connection with the messagebus
messagebusClient = WebsocketClient()
messagebusClient.on('connected', onConnected)


# This will block until the client gets closed
messagebusClient.run_forever()
