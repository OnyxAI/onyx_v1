# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from onyx.api.assets import Json
from onyx.client.speech.assets import snowboydecoder
import onyx, importlib, wave, pyaudio, sys, os, time
from onyx.config import get_config
from onyxbabel import gettext
from onyx.util import play_wav, play_mp3
from onyx.util.log import getLogger
from onyx.skills.core import OnyxSkill
from onyx.client.stt import STTFactory
from onyx.client.tts import TTSFactory

config = get_config('onyx')

import threading
from threading import Thread

from onyx.sockyx.client.ws import WebsocketClient
from onyx.sockyx.message import Message

skills = OnyxSkill(name="speech")

stt = STTFactory.create()
tts = TTSFactory.create()

json = Json()
LOG = getLogger('SpeechClient')
import speech_recognition as sr


class Detector:

	def __init__(self):
		self.lang = config.get('Base', 'lang')

	def detected_callback(self):

		def create_ws_detect():
				def onConnected(event=None):
					ws.emit(Message('onyx_detect'))
					t.close()

				ws = WebsocketClient()
				ws.on('connected', onConnected)
				# This will block until the client gets closed
				ws.run_forever()

		t = threading.Thread(target=create_ws_detect)
		t.start()

		self.detector.terminate()
		play_wav(onyx.__path__[0] + "/client/speech/resources/ding.wav")

		r = sr.Recognizer()

		with sr.Microphone() as source:
			print("Say something!")
			audio = r.listen(source, timeout=1, phrase_time_limit=5)

		try:

			result = stt.execute(audio, language=self.lang)
			print("You said: " + result)

			def create_ws_send():
				def onConnected(event=None):
					print ("Sending message...")
					payload = {
					        'utterances': [result]
					}
					ws.emit(Message('onyx_recognizer:utterance', payload))
					ws.emit(Message('onyx_detect_finish'))
					t.close()


				ws = WebsocketClient()
				ws.on('connected', onConnected)
				# This will block until the client gets closed
				ws.run_forever()

			t = threading.Thread(target=create_ws_send)
			t.start()
			time.sleep(2)
			self.detector.start(self.detected_callback)


		except sr.UnknownValueError:
			print("Speech Recognition could not understand audio")
			self.detector.start(self.detected_callback)
		except sr.RequestError as e:
			print("Could not request results from Speech Recognition service; {0}".format(e))
			self.detector.start(self.detected_callback)

	def start(self):
		self.detector = snowboydecoder.HotwordDetector(onyx.__path__[0] + "/client/speech/resources/Onyx.pmdl", sensitivity=0.6, audio_gain=1)
		print('Starting...')
		self.detector.start(self.detected_callback)


if __name__ == "__main__":
    detector = Detector()
    detector.start()
