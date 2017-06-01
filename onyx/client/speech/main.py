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
import onyx, importlib, wave, pyaudio, sys, os, time
from onyx.config import get_config
from onyxbabel import gettext
from onyx.util import play_wav, play_mp3
from onyx.util.log import getLogger
from onyx.skills.core import OnyxSkill
from onyx.client.stt import STTFactory

config = get_config('onyx')

import threading

from onyx.messagebus.client.ws import WebsocketClient
from onyx.messagebus.message import Message

skills = OnyxSkill(name="speech")

stt = STTFactory.create()

json = Json()
LOG = getLogger('SpeechClient')
import speech_recognition as sr


class Detector:

	def __init__(self):
		self.lang = config.get('Base', 'lang')

	def detected_callback(self):
		self.detector.terminate()
		play_wav(onyx.__path__[0] + "/client/speech/resources/ding.wav")

		r = sr.Recognizer()
		with sr.Microphone() as source:
			print("Say something!")
			audio = r.listen(source)

		try:
			result = stt.execute(audio, language=self.lang)
			print("You said: " + result)

			def create_ws():
				def onConnected(event=None):
					print ("Sending message...")
					payload = {
					        'utterances': [result]
					}
					ws.emit(Message('recognizer_loop:utterance', payload))
					t.close()
					#self.detector.start(self.detected_callback)


				ws = WebsocketClient()
				ws.on('connected', onConnected)
					# This will block until the client gets closed
				ws.run_forever()

			t = threading.Thread(target=create_ws)
			t.start()
			time.sleep(2)
			self.detector.start(self.detected_callback)




		except sr.UnknownValueError:
			print("Speech Recognition could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Speech Recognition service; {0}".format(e))

	def start(self):
		self.detector = snowboydecoder.HotwordDetector(onyx.__path__[0] + "/client/speech/Onyx.pmdl", sensitivity=0.5, audio_gain=1)
		print('Starting...')
		self.detector.start(self.detected_callback)


if __name__ == "__main__":
	detector = Detector()
	detector.start()
