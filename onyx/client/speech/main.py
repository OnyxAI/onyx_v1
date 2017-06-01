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
from onyx.client.speech.assets import snowboydecoder
import onyx, importlib, wave, pyaudio, sys, os
from onyx.config import get_config
from onyxbabel import gettext
from onyx.util import play_wav, play_mp3
from onyx.skills.core import OnyxSkill
from onyx.client.stt import STTFactory
from onyx.messagebus.client.ws import WebsocketClient
from onyx.messagebus.message import Message
skills = OnyxSkill(name="speech")
stt = STTFactory.create()
json = Json()
import speech_recognition as sr


from onyx.config import get_config
config = get_config('onyx')

from onyx.client.tts import TTSFactory

from onyx.util.log import getLogger

from threading import Thread, Lock
import threading

logger = getLogger("SpeechClient")
ws = None
tts = TTSFactory.create()
lock = Lock()


class Detector():

	def __init__(self):
		super(Detector, self).__init__()
		self.lang = config.get('Base', 'lang')
		self.can_run = threading.Event()
		self.thing_done = threading.Event()
		self.thing_done.set()
		self.can_run.set()

	def detected_callback(self):
		play_wav(onyx.__path__[0] + "/client/speech/resources/ding.wav")
		self.pause()

	def speak(self):

		r = sr.Recognizer()
		with sr.Microphone() as source:
			print("Say something!")
			audio = r.listen(source)

		try:
			result = stt.execute(audio, language=self.lang)
			print("You said: " + result)
		except sr.UnknownValueError:
			print("Speech Recognition could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Speech Recognition service; {0}".format(e))

		def create_ws():
			def onConnected(event=None):
				print ("Sending message...")
				payload = {
					'utterances': [result]
				}
				ws.emit(Message('recognizer_loop:utterance', payload))
				self.resume()
				t.close()

				# Establish a connection with the messagebus

			ws = WebsocketClient()
			ws.on('connected', onConnected)
			# This will block until the client gets closed
			ws.run_forever()

		c = threading.Thread(target=create_ws)
		c.start()



	def run(self):
		while True:
			self.can_run.wait()
			try:
				self.thing_done.clear()
				detector = snowboydecoder.HotwordDetector(onyx.__path__[0] + "/client/speech/Onyx.pmdl", sensitivity=0.5, audio_gain=1)
				detector.start(self.detected_callback)
			finally:
				self.thing_done.set()

	def pause(self):
		self.can_run.clear()
		self.speak()
		#self.thing_done.wait()
		self.resume()

	def resume(self):
		self.can_run.set()


def connect():
    ws.run_forever()

def main():
    global ws
    global loop
    ws = WebsocketClient()
    tts.init(ws)
    loop = Detector()

    event_thread = Thread(target=connect)
    event_thread.setDaemon(True)
    event_thread.start()

    try:
        loop.run()
    except KeyboardInterrupt as e:
        logger.exception(e)
        event_thread.exit()
        sys.exit()

if __name__ == "__main__":
    main()
